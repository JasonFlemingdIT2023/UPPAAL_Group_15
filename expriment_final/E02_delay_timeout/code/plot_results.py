"""Regenerate the experiment figures from the included result data."""
from pathlib import Path
import collections
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'results/analysis'/name).read_text(encoding='utf-8'))


def draw_trace(data, name, title):
    admissions = [e for e in data['events'] if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition']]
    assert admissions
    origin = admissions[0]['time']
    end = data['final_time'] - origin
    fig, ax = plt.subplots(figsize=(12, 4.2))
    colors = {4: '#377eb8', 5: '#2d9964', 6: '#c34a54'}
    for interval in data['network_intervals']:
        if interval['start'] < origin:
            continue
        left, width = interval['start'] - origin, interval['end'] - interval['start']
        label = ('CMD' if interval['kind'] == 4 else 'ACK') + str(interval['peer'])
        ax.barh(1, width, left=left, height=.42, color=colors.get(interval['kind'], '#777777'),
                edgecolor='white', hatch='///' if not interval['delivered'] else None)
        ax.text(left + width / 2, 1, label, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
    annotations = collections.defaultdict(list)
    for e in data['events']:
        x = e['time'] - origin
        if x < 0:
            continue
        transition = e['transition']
        label = None
        if 'CommandClient(0).WaitAck->CommandClient(0).Sending' in transition:
            label = 'timeout / retry pending'
        elif 'CommandClient(0).WaitAck->CommandClient(0).Failed' in transition:
            label = 'FAILED'
        elif 'CommandClient(0).Sending->CommandClient(0).Idle' in transition:
            label = 'late ACK accepted'
        if label:
            annotations[x].append(label)
    for x, labels in annotations.items():
        ax.vlines(x, -.12, 1.38, color='#a73548', linestyle='--', linewidth=1)
        ax.scatter([x], [0], color='#a73548', zorder=5)
        label = '\nthen '.join(labels)
        ax.annotate(f'{label}\nt={x:g}', (x, 0), xytext=(0, -18), textcoords='offset points',
                    ha='right' if x == end else 'center', va='top', fontsize=9)
    ax.set_yticks([0, 1], ['Client 0 events', 'Shared link'])
    ax.set_xlim(-.5, end + 1)
    ax.set_ylim(-.7, 1.55)
    ax.set_xlabel('Model time since first ARM admission for drone 0')
    ax.set_title(title, loc='left', fontsize=13, pad=18, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    fig.text(.02, .015, 'CMD/ACK number = drone ID. Hatched packet is still in flight at witness endpoint. One witness, not a worst-case bound.', fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, 1))
    for ext in ['png', 'svg']:
        fig.savefig((ROOT/'results/figs') / f'{name}.{ext}', dpi=180)
    plt.close(fig)


def main():
    cells = load('E02_matrix.json')
    lookup = {(r['d_max'], r['ack_timeout']): r for r in cells}
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, pid, title in zip(axes, ['P09', 'P08'], ['Retry counter increment reachable (P09)', 'Retry exhaustion reachable (P08)']):
        matrix = [[{'not_satisfied': 0, 'satisfied': 1}.get(lookup[d, t][pid], 2) for t in [6, 14, 24]] for d in [2, 3, 5]]
        ax.imshow(matrix, cmap=ListedColormap(['#dcebf3', '#bd533b', '#b8bdc4']), vmin=0, vmax=2, aspect='auto')
        for i in range(3):
            for j in range(3):
                ax.text(j, i, ['Unreachable', 'Reachable', 'Inconclusive'][matrix[i][j]], ha='center', va='center', color='white' if matrix[i][j] == 1 else '#183043', fontsize=11)
        ax.set_xticks(range(3), [6, 14, 24]); ax.set_yticks(range(3), [2, 3, 5])
        ax.set_xlabel('ACK_TIMEOUT (model units)'); ax.set_ylabel('D_MAX (model units)')
        ax.set_title(title, fontsize=12, pad=12)
    fig.suptitle('Reliable communication can still permit retries and failure', fontsize=15, fontweight='bold')
    fig.text(.5, .025, 'N=3 | D_MIN=1 | MAX_RETRY=2 | no loss | no heartbeat | three runs agree in every cell\nP01 success reachable and P02-P05 satisfied in all nine configurations. P15 any-drone failure agrees with P08.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .12, 1, .92))
    for ext in ['png', 'svg']:
        fig.savefig((ROOT/'results/figs') / f'E02_heatmaps.{ext}', dpi=180)
    plt.close(fig)
    draw_trace(load('baseline_late_ack_events.json'), 'baseline_late_ack', 'Baseline witness: a late ACK ends the exchange after timeout')
    draw_trace(load('reliable_failure_events.json'), 'reliable_failure', 'Reliable-link witness: ARM executes but confirmation times out')


if __name__ == '__main__':
    main()
