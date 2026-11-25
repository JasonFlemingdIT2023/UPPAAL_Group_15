"""Audit the fixed E04 study, derive its outcome matrix and explain actual traces."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import statistics
from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from run_coordination_experiments import make_model, property_for
from summarize_E03 import trace_events

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'results/coordination'
OUT = BASE/'analysis_E04'
IDS = [f'P{i:02d}' for i in range(1, 9)] + ['P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P21', 'P25', 'P27', 'P28']

@lru_cache(None)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data): p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def audit(path):
    r = json.loads(path.read_text(encoding='utf-8'))
    assert r['returncode'] == 0 and r['result'] in ['satisfied', 'not_satisfied']
    for f, key in [(path.parent.parent/'model.xml', 'model_sha256'), (path.parent/'query.q', 'query_sha256'),
                   (path.parents[2]/'runner_snapshot.py', 'runner_sha256'), (ROOT/'models/08_final_version.xml', 'source_model_sha256'), (Path(r['verifyta_path']), 'verifyta_sha256')]:
        assert sha(f) == r[key], f
    raw = (path.parent/'stdout.log').read_text(encoding='utf-8')
    assert ('Formula is satisfied.' if r['result'] == 'satisfied' else 'Formula is NOT satisfied.') in raw
    assert r['query'] == property_for(r['property_id'], r['N'])[1]
    mode = 'legacy_both' if r['loss_mode'] in ['bounded_both', 'legacy_both'] else None
    expected = make_model(r['d_max'], r['ack_timeout'], mode, r['N'], max_retry=r['max_retry'], loss_budget=r['loss_budget'])
    assert (path.parent.parent/'model.xml').read_bytes() == expected.encode('utf-8')
    command = [r['verifyta_path'], *r['search_options']] + (['-t', '0'] if r['trace_enabled'] else []) + ['model.xml', 'query.q']
    assert json.loads((path.parent/'command.json').read_text(encoding='utf-8')) == command
    assert r['time_limit_seconds'] == 120 and r['memory_limit_bytes'] == 8*1024**3
    assert r['search_options'] == ['-s', '-u', '-o', '0', '--state-representation', '1', '-S', '1', '-n', '0', '-r', '1']
    return r

def audit_extension(r):
    model = ET.parse(ROOT/Path(r['log_path']).parent/'model.xml').getroot()
    reference = ET.fromstring(make_model(3, 24, 'legacy_both', r['N'], max_retry=r['max_retry']))
    assert model.findtext('system') == reference.findtext('system')
    assert model.findtext('declaration').replace(f"const int LOSS_BUDGET = {r['loss_budget']};\n", '') == reference.findtext('declaration')
    for template, original in zip(model.findall('template'), reference.findall('template')):
        if template.findtext('name') != 'PacketNetwork':
            assert ET.tostring(template) == ET.tostring(original)
            assert 'lossCount' not in ET.tostring(template, encoding='unicode')
            continue
        assert template.findtext('declaration').replace('\nint[0, LOSS_BUDGET] lossCount = 0;', '') == original.findtext('declaration')
        transitions = template.findall('transition')
        counted = [t for t in transitions if any('lossCount' in (label.text or '') for label in t.findall('label'))]
        assert len(counted) == 1
        edge = counted[0]
        assert edge.find('source').get('ref') == 'id1' and edge.find('target').get('ref') == 'id3'
        labels = {label.get('kind'): label.text for label in edge.findall('label')}
        assert labels['assignment'] == 'lossCount++'
        assert labels['guard'] == 'lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND || packet.kind == PK_ACCEPTED || packet.kind == PK_DENIED)'
        for t, orig in zip(transitions, original.findall('transition')):
            if t is not edge: assert ET.tostring(t) == ET.tostring(orig)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    index = json.loads((ROOT/'experiments/E04_bounded_loss/evidence.json').read_text(encoding='utf-8'))
    groups = {}
    for category, runs in index['runs'].items():
        rows = [audit(p) for run in runs for p in sorted((BASE/run).glob('*/P*/result.json'))]
        assert len(rows) == index['expected_counts'][category]
        groups[category] = rows
        save(OUT/f'{category}_records.json', rows)
    rows = groups['matrix']
    lookup = {(r['N'], r['loss_budget'], r['max_retry'], r['property_id']): r for r in rows}
    assert set(lookup) == {(n, k, retry, pid) for n in [1, 3] for k in range(3) for retry in range(3) for pid in IDS}
    outcomes = []
    for n in [1, 3]:
        for k in range(3):
            for retry in range(3):
                audit_extension(lookup[n, k, retry, 'P01'])
                truths = {pid: lookup[n, k, retry, pid]['result'] == 'satisfied' for pid in IDS}
                assert all(truths[pid] for pid in ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P13', 'P14', 'P16', 'P21', 'P27'])
                assert truths['P25'] == (retry >= k)
                assert all(truths[pid] == (retry < k) for pid in ['P08', 'P10', 'P11', 'P15'])
                assert truths['P12'] == (k > 0)
                outcomes.append(dict(N=n, loss_budget=k, max_retry=retry, outcomes=truths))
    for r in groups['reliable_control']:
        assert r['result'] == lookup[r['N'], 0, r['max_retry'], r['property_id']]['result']
    for r in groups['unrestricted']:
        assert r['result'] == ('not_satisfied' if r['property_id'] == 'P25' else 'satisfied')
    for r in groups['timing_control']:
        assert r['result'] == ('not_satisfied' if r['property_id'] == 'P25' else 'satisfied')
    save(OUT/'outcome_matrix.json', outcomes)
    save(OUT/'evidence_index.json', index)
    summary = {'invocations': sum(len(v) for v in groups.values()), 'matrix_invocations': len(rows), 'completed': True,
               'matrix_wall_seconds_sum': sum(r['wall_seconds'] for r in rows), 'matrix_wall_seconds_median': statistics.median(r['wall_seconds'] for r in rows),
               'matrix_wall_seconds_max': max(r['wall_seconds'] for r in rows), 'matrix_sampled_rss_mib_max': max(r['sampled_peak_rss_bytes'] for r in rows)/1024**2,
               'measurement_note': 'Single invocation per configuration/query. Wall time includes launch/license overhead; sampled RSS is a peak lower bound. Liveness state/CPU statistics not used.'}
    save(OUT/'execution_summary.json', summary)
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.5))
    for i, n in enumerate([1, 3]):
        for j, (pid, title) in enumerate([('P25', 'Prepared inevitably reaches Done'), ('P15', 'Any drone confirmation failure reachable'), ('P28', 'Success after all K losses reachable')]):
            ax = axes[i, j]
            grid = [[int(lookup[n, k, retry, pid]['result'] == 'satisfied') for retry in range(3)] for k in range(3)]
            ax.imshow(grid, vmin=0, vmax=1, cmap=ListedColormap(['#e8c39b', '#8db7ad']))
            for k in range(3):
                for retry in range(3): ax.text(retry, k, 'TRUE' if grid[k][retry] else 'FALSE', ha='center', va='center', fontsize=12)
            ax.set_xticks(range(3)); ax.set_yticks(range(3)); ax.set_xlabel('MAX_RETRY (after first attempt)'); ax.set_ylabel(f'N={n} | global loss budget K')
            ax.set_title(f'{pid}: {title}', fontsize=10)
    fig.suptitle('E04: bounded loss changes what retries can guarantee', fontsize=16, fontweight='bold')
    fig.text(.5, .02, 'D=1..3, ACK_TIMEOUT=24, no heartbeat; K is shared across all command requests and replies.\nTRUE denotes formula truth, not always a desirable outcome. P01 (some success) is true in every cell.\nResults apply to the tested configurations and success after Prepared, not unconditional startup or arbitrary fleets.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .13, 1, .94))
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E04_outcome_matrix.{ext}', dpi=180)
    plt.close(fig)
    trace_data = []
    lines = ['# E04 diagnostic traces', '', 'Finite traces use time relative to drone 0 first ARM admission. They are witnesses, not timing bounds.', '']
    for r in groups['diagnostics']:
        path = ROOT/r['log_path']/'stdout.log'
        lines += [f"## {r['configuration_id']} / {r['property_id']}", '', f"Raw log: `{r['log_path']}/stdout.log`", '']
        if r['property_id'] == 'P26':
            raw = path.read_text(encoding='utf-8')
            assert r['result'] == 'not_satisfied' and 'Supervisor.Idle' in raw and 'Transition:' not in raw
            lines += ['The counterexample consists of the initial symbolic state. Supervisor.Idle has no invariant/urgent outgoing edge, so time can elapse indefinitely without beginning uploads.', '']
            continue
        assert r['result'] == 'satisfied'
        events = trace_events(path)
        start = next(e['time'] for e in events if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition'])
        packets, active, last_count = [], None, 0
        for e in events:
            t = e['transition']; count = int(e['after']['Link.lossCount'])
            lost = 'Link.Transmitting->Link.Lost' in t
            assert count == last_count + int(lost); last_count = count
            if 'Link.Idle->Link.Transmitting' in t:
                assert active is None
                active = dict(start=e['time']-start, kind=int(e['after']['Link.packet.kind']), peer=int(e['after']['Link.packet.peer']), cmd=int(e['after']['Link.packet.cmd']))
            if lost or 'Link.Transmitting->Link.Delivered' in t:
                assert active is not None
                packets.append(dict(**active, end=e['time']-start, outcome='lost' if lost else 'delivered')); active = None
        if active: packets.append(dict(**active, end=events[-1]['time']-start, outcome='in_transit'))
        packets = [p for p in packets if p['start'] >= 0 and p['kind'] in [4, 5, 6]]
        data = dict(configuration_id=r['configuration_id'], property_id=r['property_id'], loss_budget=r['loss_budget'], max_retry=r['max_retry'],
                    N=r['N'], ack_timeout=r['ack_timeout'], first_command_absolute=start, end_relative=events[-1]['time']-start,
                    packets=packets, final_locations=events[-1]['locations'], final_variables=events[-1]['after'], events=events)
        trace_data.append(data)
        save(OUT/(r['configuration_id']+'_'+r['property_id']+'_events.json'), data)
        lines += ['| Relative time | Event | lossCount |', '|---:|---|---:|']
        for e in events:
            t = e['transition']
            if e['time'] >= start and any(x in t for x in ['CommandClient(0)', '->Link.Lost', 'CommandServer(0).Decide->CommandServer(0).Idle', '->Supervisor.Done']):
                lines.append(f"| {e['time']-start:g} | " + t.replace('\n', '; ').replace('|', '&#124;') + f" | {int(e['after']['Link.lossCount'])} |")
        lines += ['', 'Final locations: `'+events[-1]['locations']+'`', '']
    (OUT/'trace_events.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
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
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E04_recovery_traces.{ext}', dpi=180)
    plt.close(fig)
    print('AUDIT PASSED:', {k: len(v) for k, v in groups.items()})
    print(json.dumps(summary, indent=2))
    print('All tested R>=K cells satisfy P25; other cells permit any-drone failure. Reliable controls agree; unrestricted and timing controls fail P25.')

if __name__ == '__main__': main()
