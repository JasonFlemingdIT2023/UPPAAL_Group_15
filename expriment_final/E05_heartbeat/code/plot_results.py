"""Regenerate the experiment figures from the included result data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plot_activation import plot_activation

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'results/analysis'/name).read_text(encoding='utf-8'))


def main():
    rows = load('activation_records.json')
    categories = {'settings': load('settings_records.json')}
    IDS = ['P01', 'P03', 'P08', 'P24']
    lookup = {(r['N'], r['heartbeat_mode'], r['property_id']): r for r in rows}
    followup_path = ROOT/'results/analysis/activation_followup.json'
    followup = load(followup_path.name) if followup_path.exists() else None
    plot_activation(rows, ROOT/'results/figs', followup)
    settings = [lookup[2, 'active', 'P03']] + [r for r in categories['settings'] if r['property_id'] == 'P03']
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    names = ['Period 20\nfirst: 20,20', 'Period 40\nfirst: 40,40', 'Period 20\nfirst: 20,30']
    for ax, key, title in [(axes[0], 'explored_states', 'P03 explored states'), (axes[1], 'wall_seconds', 'P03 wall time (s)')]:
        for i, r in enumerate(settings):
            v = r[key]
            if v is not None:
                ax.bar(i, v, color=['#a95731', '#3979ad', '#4e8469'][i]); ax.text(i, v, f'{v:,}', ha='center', va='bottom')
        ax.set_xticks(range(3), names); ax.set_title(title); ax.margins(y=.2); ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('E05: period and first-release settings, N=2', fontweight='bold')
    fig.text(.5, .02, 'One measurement each; subsequent release is self-timed from network admission.\nThese are verifier costs, not message latency, throughput or failure probability.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .12, 1, .94))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E05_settings.{ext}', dpi=180)
    plt.close(fig)
    failure = load('failure_trace_summary.json')
    packets = failure['packets']
    first = failure['first_start_command']
    end = failure['failure_time']
    timeout_events = [{'time': time} for time in failure['timeout_times']]
    fig, ax = plt.subplots(figsize=(13, 5))
    styles = {4: ('CMD', '#3979ad'), 5: ('ACK', '#4e8469'), 7: ('HB', '#d9a24b')}
    for p in packets:
        name, color = styles[p['kind']]
        ax.barh(p['peer'], p['end']-p['start'], left=p['start'], height=.5, color=color, hatch='///' if not p['complete'] else None, edgecolor='white')
        ax.text((p['start']+p['end'])/2, p['peer'], name, ha='center', va='center', fontsize=8)
    for i, e in enumerate(timeout_events):
        ax.axvline(e['time'], color='#ae3c36', linestyle='--', linewidth=1)
        ax.text(e['time'], 2.65, ['retry 1', 'retry 2', 'FAILED'][i]+'\n'+f"t={e['time']:g}", ha='center', color='#92332d', fontsize=9)
    ax.set_yticks([0, 1, 2], ['Drone 0', 'Drone 1', 'Drone 2']); ax.set_ylim(-.65, 3.25)
    ax.set_xlim(first-4, end+2); ax.set_xticks(sorted({107, 110, 113, 121, 124, 130, 138, 144, 150, 152}))
    ax.set_xlabel('Absolute model time; rows identify packet peer, all packets share ONE link')
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='x', alpha=.15)
    fig.suptitle('E05 failure witness: heartbeat and retransmissions delay ACK 0', fontsize=15, fontweight='bold')
    fig.text(.5, .03, 'N=3, HB_PERIOD=20, ACK_TIMEOUT=14, MAX_RETRY=2, no packet loss. One possible DFS witness.\nSTART 0 is executed when its ACK enters the link at t=150. Client 0 fails at t=152 while ACK 0 is still in transit (hatched).\nThis trace demonstrates reachability, not a probability or worst-case latency bound.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .94))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E05_failure_timeline.{ext}', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
