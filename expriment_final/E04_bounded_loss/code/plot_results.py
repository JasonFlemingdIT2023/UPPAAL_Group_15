"""Regenerate the experiment figures from the included result data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'results/analysis'/name).read_text(encoding='utf-8'))


def main():
    outcomes = load('outcome_matrix.json')
    lookup = {(r['N'], r['loss_budget'], r['max_retry']): r['outcomes'] for r in outcomes}
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.5))
    for i, n in enumerate([1, 3]):
        for j, (pid, title) in enumerate([('P25', 'Prepared inevitably reaches Done'), ('P15', 'Any drone confirmation failure reachable'), ('P28', 'Success after all K losses reachable')]):
            ax = axes[i, j]
            grid = [[int(lookup[n, k, retry][pid]) for retry in range(3)] for k in range(3)]
            ax.imshow(grid, vmin=0, vmax=1, cmap=ListedColormap(['#e8c39b', '#8db7ad']))
            for k in range(3):
                for retry in range(3): ax.text(retry, k, 'TRUE' if grid[k][retry] else 'FALSE', ha='center', va='center', fontsize=12)
            ax.set_xticks(range(3)); ax.set_yticks(range(3)); ax.set_xlabel('MAX_RETRY (after first attempt)'); ax.set_ylabel(f'N={n} | global loss budget K')
            ax.set_title(f'{pid}: {title}', fontsize=10)
    fig.suptitle('E04: bounded loss changes what retries can guarantee', fontsize=16, fontweight='bold')
    fig.text(.5, .02, 'D=1..3, ACK_TIMEOUT=24, no heartbeat; K is shared across all command requests and replies.\nTRUE denotes formula truth, not always a desirable outcome. P01 (some success) is true in every cell.\nResults apply to the tested configurations and success after Prepared, not unconditional startup or arbitrary fleets.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .13, 1, .94))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E04_outcome_matrix.{ext}', dpi=180)
    plt.close(fig)
    trace_data = [
        load('n1_dmax3_timeout24_legacy_both_budget2_retry2_P28_events.json'),
        load('n1_dmax3_timeout24_legacy_both_budget2_retry1_P11_events.json'),
        load('n1_dmax3_timeout24_legacy_both_budget1_retry0_P10_events.json'),
    ]
    short = [t for t in trace_data if t['N'] == 1]
    assert len(short) == 3
    fig, axes = plt.subplots(3, 1, figsize=(12, 7.8))
    for ax, tr in zip(axes, short):
        for p in tr['packets']:
            ax.barh(0, p['end']-p['start'], left=p['start'], height=.35, color='#3979ad' if p['kind'] == 4 else '#4e8469')
            if p['outcome'] == 'lost': ax.plot(p['end'], 0, 'x', color='#b42b2b', markersize=11, markeredgewidth=2)
        terminal = 'DONE' if tr['property_id'] == 'P28' else 'FAILED, armed=0' if tr['property_id'] == 'P11' else 'FAILED, armed=1'
        ax.axvline(tr['end_relative'], color='#555555', linestyle='--', linewidth=1)
        ax.text(tr['end_relative']+.6, .12, terminal, fontsize=9)
        for e in tr['events']:
            if 'CommandClient(0).WaitAck->CommandClient(0).Sending' in e['transition']:
                t = e['time']-tr['first_command_absolute']; ax.annotate('retry', (t, -.18), (t, -.5), ha='center', arrowprops={'arrowstyle': '->'}, fontsize=9)
        ax.set_title(f"N=1, K={tr['loss_budget']}, MAX_RETRY={tr['max_retry']} ({tr['property_id']})", loc='left', fontsize=11)
        ax.set_yticks([]); ax.set_ylim(-.65, .65); ax.set_xlim(-1, 69); ax.set_xticks([0, 4, 12, 24, 36, 48, 52, 60])
        ax.grid(axis='x', alpha=.16); ax.spines[['top', 'right', 'left']].set_visible(False)
    axes[-1].set_xlabel('Model time relative to first ARM request admission')
    fig.suptitle('E04: recovering after two lost requests, or exhausting retries', fontsize=15, fontweight='bold')
    fig.text(.5, .02, 'Blue: command request | Green: accepted ACK | Red cross: packet loss | Blank intervals: waiting for ACK timeout\nK=2,R=2: requests lost at t=1,25, retry at t=48 succeeds, Done at t=52.\nK=2,R=1: both attempts lost, failure at t=48. K=1,R=0: ARM executes at t=3, ACK lost at t=4, failure at t=24.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .13, 1, .94))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E04_recovery_traces.{ext}', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
