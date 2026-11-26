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
    outcomes = load('outcome_summary.json')
    truth = {(r['N'], r['scheduler'], r['property']): r['result'] for r in outcomes}
    original_progress = truth[3, 'original', 'HB_PROGRESS'] == 'satisfied'
    selected = ['P35', 'P36', 'P37', 'HB_PROGRESS', 'P25']
    completion = load('completion_proof.json')['conclusion'] == 'satisfied_by_compositional_proof'
    fig, ax = plt.subplots(figsize=(12, 6.6))
    configurations = [(n, p) for n in [1, 2, 3] for p in ['original', 'ack_priority']]
    code = {'not_satisfied': 0, 'satisfied': 1, 'maybe': 2, 'timeout': 2}
    grid = [[code[truth[n, p, pid]] for pid in selected] for n, p in configurations]
    ax.imshow(grid, cmap=ListedColormap(['#dfb28b', '#89b7a5', '#c4cbd3']), vmin=0, vmax=2, aspect='auto')
    for i in range(6):
        for j in range(5):
            label = 'TRUE*' if completion and (i, j) == (5, 4) else ['FALSE', 'TRUE', 'UNKNOWN'][grid[i][j]]
            if original_progress and (i, j) == (4, 3):
                label = 'TRUE†'
            ax.text(j, i, label, ha='center', va='center', fontsize=11)
    ax.set_yticks(range(6), [f'N={n} / '+('original' if p == 'original' else 'ACK priority') for n, p in configurations])
    ax.set_xticks(range(5), ['No retry\nexhaustion', 'No retry\ntrigger', 'Reply wait\nat most 6', 'Each pending HB\neventually sent', 'Prepared\nevitably Done'])
    ax.set_title('E06: ACK priority removes timeout exhaustion in the tested model', fontsize=15, fontweight='bold', pad=18)
    note = 'D=1..3, ACK_TIMEOUT=14, MAX_RETRY=2, HB_PERIOD=20, no loss.\nN=1,2: exact checks. N=3: concrete counterexamples plus decisive over-approximation proofs.\n'
    note += '* N=3 completion: verified Prepared boundary + exact universal continuation proof.\n' if completion else ''
    note += '† N=3 original heartbeat progress: P06 plus finite competing traffic.' if original_progress else 'UNKNOWN: unresolved. Heartbeat progress checks every active drone.'
    fig.text(.5, .025, note, ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .98))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E06_outcomes.{ext}', dpi=180)
    plt.close(fig)
    traces = load('reply_comparison_traces.json')
    fig, axes = plt.subplots(2, 1, figsize=(13, 5.8))
    colors = {4: '#3979ad', 5: '#4e8469', 7: '#d8a148'}
    for ax, tr in zip(axes, traces):
        for p in tr['packets']:
            name = {4: 'CMD', 5: 'ACK', 7: 'HB'}[p['kind']] + str(p['peer'])
            ax.barh(0, p['relative_end']-p['relative_start'], left=p['relative_start'], height=.45, color=colors[p['kind']], hatch='///' if not p['complete'] else None, edgecolor='white')
            if p['relative_end']-p['relative_start'] >= 2: ax.text((p['relative_end']+p['relative_start'])/2, 0, name, ha='center', va='center', fontsize=8)
        for e in tr['events']:
            if e['time'] >= tr['start'] and 'CommandClient(0).WaitAck->CommandClient(0).Sending' in e['transition']:
                at = e['time']-tr['start']; ax.axvline(at, linestyle=':', color='#9c3d36'); ax.text(at, .4, 'retry', ha='center', fontsize=9)
        end = tr['end']-tr['start']
        ax.axvline(end, linestyle='--', color='#9c3d36' if tr['policy'] == 'original' else '#4e8469')
        ax.text(end+.4, -.45, 'FAILED at 42' if tr['policy'] == 'original' else 'ACK received at 6', fontsize=9)
        ax.set_title('Original: ACK0 is still in transit at retry exhaustion' if tr['policy'] == 'original' else 'ACK priority: command service 3 + ACK service 3', loc='left', fontsize=11)
        ax.set_xlim(-.5, 46); ax.set_ylim(-.8, .85); ax.set_yticks([]); ax.set_xticks([0, 3, 6, 14, 28, 40, 42]); ax.grid(axis='x', alpha=.15)
        ax.spines[['left', 'right', 'top']].set_visible(False)
    axes[-1].set_xlabel('Model time relative to START0 admission')
    fig.suptitle('E06: why giving ACKs the next link slot helps', fontsize=16, fontweight='bold')
    fig.text(.5, .025, 'Blue: requests | Green: replies | Gold: heartbeats | Hatched: packet still in transit at trace end\nTwo concrete executions with identical N=3, heartbeat, service, timeout and retry settings.\nPriority delay 6 attains the verified bound; the original 42 is the failure time in its displayed witness.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .94))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E06_reply_comparison.{ext}', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
