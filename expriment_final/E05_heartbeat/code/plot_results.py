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
    rows = load('activation_records.json')
    categories = {'settings': load('settings_records.json')}
    IDS = ['P01', 'P03', 'P08', 'P24']
    lookup = {(r['N'], r['heartbeat_mode'], r['property_id']): r for r in rows}
    labels = [f'N={n} / HB {hb}' for n in [1, 2, 3] for hb in ['off', 'on']]
    configs = [(n, hb) for n in [1, 2, 3] for hb in ['inactive', 'active']]
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    mapping = {'not_satisfied': 0, 'satisfied': 1, 'timeout': 2, 'memory_limit': 2}
    grid = [[mapping[lookup[n, hb, p]['result']] for p in IDS] for n, hb in configs]
    ax = axes[0, 0]
    ax.imshow(grid, cmap=ListedColormap(['#e7b87b', '#82b7aa', '#bfc5cd']), vmin=0, vmax=2, aspect='auto')
    ax.set_xticks(range(4), IDS); ax.set_yticks(range(6), labels)
    for i in range(6):
        for j in range(4): ax.text(j, i, ['FALSE', 'TRUE', 'LIMIT'][grid[i][j]], ha='center', va='center', fontsize=10)
    ax.set_title('BFS query truth (P08 FALSE: failure excluded)')
    values = [lookup[n, hb, 'P03'] for n, hb in configs]
    for ax, key, title, scale in [(axes[0, 1], 'explored_states', 'P03: explored states (completed checks)', 1),
                                  (axes[1, 0], 'wall_seconds', 'P03: wall time (s), log scale', 1),
                                  (axes[1, 1], 'sampled_peak_rss_bytes', 'P03: sampled peak RSS (MiB)', 1024**2)]:
        for i, r in enumerate(values):
            limited = r['result'] in ['timeout', 'memory_limit']
            v = r[key]
            if v is not None:
                ax.bar(i, v/scale, color='#3979ad' if i % 2 == 0 else '#a95731', hatch='//' if limited else None)
            label = 'LIMIT' if limited else f'{v/scale:,.2f}' if scale != 1 or key == 'wall_seconds' else f'{v:,}'
            if v is None:
                ax.text(i, .08, label, transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=8)
            else:
                ax.text(i, v/scale, label, ha='center', va='bottom', fontsize=8)
        ax.set_xlim(-.6, 5.6)
        ax.set_xticks(range(6), [s.replace(' / ', '\n') for s in labels], fontsize=9)
        ax.set_title(title, fontsize=11); ax.spines[['top', 'right']].set_visible(False)
        if key in ['wall_seconds', 'explored_states']: ax.set_yscale('log'); ax.margins(y=.3)
        else: ax.margins(y=.2)
    fig.suptitle('E05: heartbeat activation and verification cost (BFS)', fontsize=16, fontweight='bold')
    fig.text(.5, .015, 'P01: success reachable | P03: START implies armed | P08: client 0 failure reachable | P24: all heartbeats seen\nSingle run per configuration/query; 120 s and 8 GiB limits. LIMIT is unknown, not false.\nWall time includes startup; sampled RSS is a lower bound on peak. No complete state count is claimed for limited checks.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .11, 1, .95))
    for ext in ['png', 'svg']: fig.savefig((ROOT/'results/figs') /f'E05_activation.{ext}', dpi=180)
    plt.close(fig)
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
