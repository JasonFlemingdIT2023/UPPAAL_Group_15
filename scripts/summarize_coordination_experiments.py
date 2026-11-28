"""Audit raw records and regenerate E02 figures and concrete trace event tables."""
from pathlib import Path
import collections
import hashlib
import json
import re
import statistics
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/coordination/analysis'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def parse_trace(path):
    """Read printed concrete diagnostic delays, preserving transition source text."""
    events, intervals = [], []
    t, pending, packet = 0.0, None, None
    last_state = {}
    for part in re.split(r'(?m)(?=^Delay:|^Transition:|^State:)', path.read_text(encoding='utf-8')):
        if part.startswith('Delay:'):
            delay = part.splitlines()[0].split(':', 1)[1].strip()
            if not re.fullmatch(r'\d+(\.\d+)?', delay):
                raise ValueError(f'Cannot treat symbolic delay as concrete: {delay}')
            t += float(delay)
        elif part.startswith('Transition:'):
            pending = {'time': t, 'transition': part.strip().removeprefix('Transition:').strip()}
            events.append(pending)
        elif part.startswith('State:'):
            state = {k: float(v) for k, v in re.findall(r'([A-Za-z0-9_().\[\]]+)=(-?\d+(?:\.\d+)?)', part)}
            last_state = state
            if pending:
                pending['after'] = {k: v for k, v in state.items() if k.startswith(('armed[', 'cmdFailed[', 'cmdAccepted[', 'CommandClient(0).', 'Link.packet.'))}
                if 'Link.Idle->Link.Transmitting' in pending['transition']:
                    assert packet is None
                    packet = {'start': t, 'peer': int(state['Link.packet.peer']), 'kind': int(state['Link.packet.kind']), 'command': int(state['Link.packet.cmd'])}
                elif 'Link.Transmitting->Link.Delivered' in pending['transition']:
                    assert packet is not None
                    packet.update(end=t, delivered=True)
                    intervals.append(packet)
                    packet = None
                pending = None
    if packet:
        packet.update(end=t, delivered=False)
        intervals.append(packet)
    return {'events': events, 'network_intervals': intervals, 'final_time': t, 'final_state': last_state,
            'raw_trace': str(path.relative_to(ROOT)), 'raw_trace_sha256': sha(path)}

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
        fig.savefig(OUT / f'{name}.{ext}', dpi=180)
    plt.close(fig)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    records = []
    for path in sorted((ROOT / 'results/coordination').glob('*_*/*/P*/result.json')):
        row = json.loads(path.read_text(encoding='utf-8'))
        if row['experiment_id'] not in ['baseline', 'E02'] or row['trace_enabled']:
            continue
        model = path.parent.parent / 'model.xml'
        assert sha(model) == row['model_sha256']
        assert sha(path.parent / 'query.q') == row['query_sha256']
        assert sha(path.parents[2] / 'runner_snapshot.py') == row['runner_sha256']
        assert row['result'] in ['satisfied', 'not_satisfied', 'timeout', 'memory_limit']
        text = (path.parent / 'stdout.log').read_text(encoding='utf-8')
        expected = 'Formula is satisfied' if row['result'] == 'satisfied' else 'Formula is NOT satisfied'
        if row['result'] in ['satisfied', 'not_satisfied']:
            assert expected in text and row['returncode'] == 0
        for name, value in [('D_MAX', row['d_max']), ('ACK_TIMEOUT', row['ack_timeout'])]:
            assert f'const int {name} = {value};' in model.read_text(encoding='utf-8')
        for key, pattern in [('cpu_user_ms', r'CPU user time used\s*:\s*(\d+) ms'), ('reported_resident_kib', r'Resident memory used\s*:\s*(\d+) KiB')]:
            found = re.search(pattern, text)
            row[key] = int(found.group(1)) if found and '-->' not in row['query'] else None
        records.append(row)
    assert records
    assert len({r['source_model_sha256'] for r in records}) == 1
    assert sha(ROOT / 'models/08_final_version.xml') == records[0]['source_model_sha256']
    groups = collections.defaultdict(list)
    for row in records:
        if row['experiment_id'] == 'E02':
            groups[(row['d_max'], row['ack_timeout'], row['property_id'])].append(row)
    assert len(groups) == 72
    for group in groups.values():
        assert len(group) == 3 and {r['repetition'] for r in group} == {1, 2, 3}
        assert len({r['result'] for r in group}) == 1
        assert len({r['model_sha256'] for r in group}) == 1
        assert len({r['query_sha256'] for r in group}) == 1
    save_json(OUT / 'audited_records.json', records)
    cells = []
    for d in [2, 3, 5]:
        for timeout in [6, 14, 24]:
            cell = {'d_max': d, 'ack_timeout': timeout}
            for pid in ['P01', 'P02', 'P03', 'P04', 'P05', 'P08', 'P09', 'P15']:
                group = groups[d, timeout, pid]
                cell[pid] = group[0]['result']
                cell[pid + '_median_wall_seconds'] = statistics.median(r['wall_seconds'] for r in group)
            cells.append(cell)
    save_json(OUT / 'E02_matrix.json', cells)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, pid, title in zip(axes, ['P09', 'P08'], ['Retry counter increment reachable (P09)', 'Retry exhaustion reachable (P08)']):
        matrix = [[{'not_satisfied': 0, 'satisfied': 1}.get(groups[d, t, pid][0]['result'], 2) for t in [6, 14, 24]] for d in [2, 3, 5]]
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
        fig.savefig(OUT / f'E02_heatmaps.{ext}', dpi=180)
    plt.close(fig)
    traces = {
        'baseline_late_ack': ('20261124T073644478957Z_pilot/dmax3_timeout14/P17/stdout.log', 'Baseline witness: a late ACK ends the exchange after timeout'),
        'reliable_failure': ('20261124T073421895292Z_pilot/dmax5_timeout14/P08/stdout.log', 'Reliable-link witness: ARM executes but confirmation times out'),
    }
    for name, (relative, title) in traces.items():
        data = parse_trace(ROOT / 'results/coordination' / relative)
        save_json(OUT / f'{name}_events.json', data)
        draw_trace(data, name, title)
        print(name, 'end=', data['final_time'], 'armed0=', data['final_state'].get('armed[0]'), 'failed0=', data['final_state'].get('cmdFailed[0][0]'))
    print('AUDIT PASSED:', len(records), 'baseline/E02 records; 72 configuration-property groups, 3 matching repetitions each.')

if __name__ == '__main__':
    main()
