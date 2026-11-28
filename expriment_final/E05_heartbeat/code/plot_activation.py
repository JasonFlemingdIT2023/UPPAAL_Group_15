"""Plot E05 verdicts alongside the fixed-budget BFS measurements."""
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


IDS = ('P01', 'P03', 'P08', 'P24')


def plot_activation(rows, destination, followup=None):
    lookup = {(r['N'], r['heartbeat_mode'], r['property_id']): r for r in rows}
    configurations = [(n, hb) for n in (1, 2, 3) for hb in ('inactive', 'active')]
    labels = [f"N={n} / HB {'on' if hb == 'active' else 'off'}" for n, hb in configurations]
    finals = followup['properties'] if followup else {}
    verdicts, cell_labels = [], []
    for n, hb in configurations:
        row, text = [], []
        for pid in IDS:
            result = lookup[n, hb, pid]['result']
            final = finals.get(pid) if (n, hb) == (3, 'active') else None
            if final:
                result = final['final']['result']
            value = {'not_satisfied': 0, 'satisfied': 1}.get(result, 2)
            row.append(value)
            text.append(['FALSE', 'TRUE', 'LIMIT'][value] + ('*' if final else ''))
        verdicts.append(row)
        cell_labels.append(text)

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    ax = axes[0, 0]
    ax.imshow(verdicts, cmap=ListedColormap(['#e7b87b', '#82b7aa', '#bfc5cd']),
              vmin=0, vmax=2, aspect='auto')
    ax.set_xticks(range(4), IDS)
    ax.set_yticks(range(6), labels)
    for i, row in enumerate(cell_labels):
        for j, label in enumerate(row):
            ax.text(j, i, label, ha='center', va='center', fontsize=10)
    ax.set_title('Property verdicts after follow-up' if followup else 'BFS property verdicts')

    values = [lookup[n, hb, 'P03'] for n, hb in configurations]
    metrics = (
        (axes[0, 1], 'explored_states', 'P03: completed BFS search states', 1),
        (axes[1, 0], 'wall_seconds', 'P03: BFS wall time (s), log scale', 1),
        (axes[1, 1], 'sampled_peak_rss_bytes', 'P03: BFS sampled peak RSS (MiB)', 1024**2),
    )
    for ax, key, title, scale in metrics:
        for i, record in enumerate(values):
            limited = record['result'] in ('timeout', 'memory_limit')
            value = record[key]
            if value is None:
                ax.text(i, .08, 'No final count', transform=ax.get_xaxis_transform(),
                        ha='center', va='bottom', fontsize=8)
                continue
            height = value / scale
            ax.bar(i, height, color='#3979ad' if i % 2 == 0 else '#a95731',
                   hatch='//' if limited else None)
            label = f'{height:,.0f}' if key == 'explored_states' else f'{height:,.2f}'
            if limited:
                label = '120 s cutoff' if key == 'wall_seconds' else f'{label} at cutoff'
            ax.text(i, height, label, ha='center', va='bottom', fontsize=8)
        ax.set_xlim(-.6, 5.6)
        ax.set_xticks(range(6), [label.replace(' / ', '\n') for label in labels], fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.spines[['top', 'right']].set_visible(False)
        if key in ('wall_seconds', 'explored_states'):
            ax.set_yscale('log')
        ax.margins(y=.3)

    notes = ['P01: success reachable | P03: START implies ARM | P08: client 0 failure reachable | P24: all heartbeats seen']
    if followup:
        methods = ', '.join(f"{pid} {finals[pid]['final']['short_method']}"
                            for pid in IDS if pid in finals)
        notes.append(f'* Verdict obtained by follow-up: {methods}.')
    notes.append('Cost panels use the original exact BFS runs (120 s, 8 GiB). Hatching marks a time cutoff.')
    fig.suptitle('E05: heartbeat activation, property verdicts and verification cost',
                 fontsize=15, fontweight='bold')
    fig.text(.5, .02, '\n'.join(notes), ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .11, 1, .95))
    for extension in ('png', 'svg'):
        fig.savefig(destination/f'E05_activation.{extension}', dpi=180)
    plt.close(fig)
