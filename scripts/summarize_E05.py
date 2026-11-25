"""Audit explicitly indexed E05 evidence and plot completed/limited checks separately."""
import sys
sys.dont_write_bytecode = True
import json
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from summarize_E03 import trace_events
from run_coordination_experiments import make_model, property_for

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/coordination'
OUT = BASE / 'analysis_E05'
IDS = ['P01', 'P03', 'P08', 'P24']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj): p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding='utf-8')

def audit(p):
    r = json.loads(p.read_text(encoding='utf-8'))
    assert r['result'] in ['satisfied', 'not_satisfied', 'timeout', 'memory_limit']
    for f, key in [(p.parent.parent/'model.xml', 'model_sha256'), (p.parent/'query.q', 'query_sha256'),
                   (p.parents[2]/'runner_snapshot.py', 'runner_sha256'), (ROOT/'models/08_final_version.xml', 'source_model_sha256')]:
        assert sha(f) == r[key], f
    text = (p.parent/'stdout.log').read_text(encoding='utf-8')
    if r['result'] in ['satisfied', 'not_satisfied']:
        assert r['returncode'] == 0
        assert ('Formula is satisfied.' if r['result'] == 'satisfied' else 'Formula is NOT satisfied.') in text
    elif r['result'] == 'timeout':
        assert r['wall_seconds'] >= r['time_limit_seconds']
    elif r['result'] == 'memory_limit':
        assert r['sampled_peak_rss_bytes'] >= r['memory_limit_bytes']
    command = json.loads((p.parent/'command.json').read_text(encoding='utf-8'))
    expected = [r['verifyta_path'], *r['search_options']]
    if r['trace_enabled']: expected += ['-t', '0']
    assert command == expected + ['model.xml', 'query.q']
    model = ET.parse(p.parent.parent/'model.xml').getroot()
    assert f"const int N = {r['N']};" in model.findtext('declaration')
    assert f"const int HB_PERIOD = {r['heartbeat_period']};" in model.findtext('declaration')
    assert ('CommandServer, HBSender, ConnectionMonitor;' in model.findtext('system')) == (r['heartbeat_mode'] == 'active')
    offsets = 'staggered' if r['heartbeat_offsets'].startswith('first eligible') else 'synchronous'
    expected_model = make_model(r['d_max'], r['ack_timeout'], n=r['N'], heartbeat=r['heartbeat_mode'], hb_period=r['heartbeat_period'], hb_offsets=offsets)
    assert (p.parent.parent/'model.xml').read_bytes() == expected_model.encode('utf-8')
    assert r['query'] == property_for(r['property_id'], r['N'])[1]
    return r

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    index = json.loads((ROOT/'experiments/E05_heartbeat/evidence.json').read_text(encoding='utf-8'))
    categories = {}
    for kind, runs in index['runs'].items():
        categories[kind] = [audit(p) for run in runs for p in sorted((BASE/run).glob('*/P*/result.json'))]
        assert len(categories[kind]) == index['expected_counts'][kind], kind
    rows = categories['activation']
    assert {(r['heartbeat_period'], r['heartbeat_offsets'], r['property_id']) for r in categories['settings']} == {
        (period, offset, pid) for period, offset in [(40, 'all clocks initially zero'), (20, 'first eligible at HB_PERIOD + floor(id * HB_PERIOD / N); subsequent period measured from admission')] for pid in IDS}
    assert len(rows) == 24 and {(r['N'], r['heartbeat_mode'], r['property_id']) for r in rows} == {
        (n, hb, pid) for n in [1, 2, 3] for hb in ['inactive', 'active'] for pid in IDS}
    for r in rows + categories['settings']:
        assert r['time_limit_seconds'] == 120 and r['memory_limit_bytes'] == 8 * 1024**3
        assert not r['trace_enabled'] and r['search_options'] == rows[0]['search_options']
    # Exact pairing: same model bytes except the system composition switch.
    run = BASE/index['runs']['activation'][0]
    for n in [1, 2, 3]:
        prefix = f'n{n}_dmax3_timeout14_hb_'
        off = (run/(prefix+'inactive_period20')/'model.xml').read_bytes()
        on = (run/(prefix+'active_period20')/'model.xml').read_bytes()
        assert on.replace(b'CommandServer, HBSender, ConnectionMonitor;', b'CommandServer;') == off
        old = BASE/f'20261125T131340771891Z_E01/n{n}_dmax3_timeout14'
        assert off == (old/'model.xml').read_bytes()
        for r in rows:
            if r['N'] == n and r['heartbeat_mode'] == 'inactive' and r['property_id'] != 'P24':
                assert r['result'] == json.loads((old/r['property_id']/'result.json').read_text(encoding='utf-8'))['result']
    # Supplement settings alter only the HB constant or the sender's first-release mechanism.
    original = ET.parse(ROOT/'models/08_final_version.xml').getroot()
    for r in categories['settings']:
        model = ET.parse(ROOT/Path(r['log_path']).parent/'model.xml').getroot()
        for a, b in zip(original.findall('template'), model.findall('template')):
            if a.findtext('name') != 'HBSender': assert ET.tostring(a) == ET.tostring(b)
    for kind, values in categories.items(): save(OUT/f'{kind}_records.json', values)
    save(OUT/'evidence_index.json', index)
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
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E05_activation.{ext}', dpi=180)
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
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E05_settings.{ext}', dpi=180)
    plt.close(fig)
    lines = ['# E05 diagnostic traffic witnesses', '', 'Model time is absolute from initialization. Each trace is one possible execution, not a bound or average.', '']
    for r in categories['diagnostics']:
        folder = ROOT/r['log_path']
        assert r['trace_enabled']
        if r['result'] != 'satisfied': continue
        events = trace_events(folder/'stdout.log')
        save(OUT/(folder.parent.name+'_'+r['property_id']+'_events.json'), events)
        lines += [f"## {r['configuration_id']} / {r['property_id']}", '', f"Raw log: `{r['log_path']}/stdout.log`", '', '| Time | Transition |', '|---:|---|']
        for e in events:
            t = e['transition']
            if any(x in t for x in ['HBSender(', 'heartbeat_rx[', 'CommandClient(', 'CommandServer(']):
                lines.append(f"| {e['time']:g} | " + t.replace('\n', '; ').replace('|', '&#124;') + ' |')
        lines.append('')
    (OUT/'traffic_traces.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    failure = next(r for r in categories['diagnostics'] if r['N'] == 3 and r['property_id'] == 'P08')
    assert failure['result'] == 'satisfied'
    events = trace_events(ROOT/failure['log_path']/'stdout.log')
    end = events[-1]['time']
    assert events[-1]['after']['cmdFailed[0][1]'] == 1
    assert events[-1]['after']['started[0]'] == 1
    assert not any('->Link.Lost' in e['transition'] for e in events)
    admissions = [e for e in events if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition'] and e['after']['Link.packet.cmd'] == 1]
    assert len(admissions) == 3
    first = admissions[0]['time']
    packets, active = [], None
    for e in events:
        t = e['transition']
        if 'Link.Idle->Link.Transmitting' in t:
            assert active is None
            active = dict(start=e['time'], peer=int(e['after']['Link.packet.peer']), kind=int(e['after']['Link.packet.kind']))
        if 'Link.Transmitting->Link.Delivered' in t:
            assert active is not None
            packets.append(dict(**active, end=e['time'], complete=True)); active = None
    if active: packets.append(dict(**active, end=end, complete=False))
    packets = [p for p in packets if p['start'] >= first - 3]
    timeout_events = [e for e in events if e['time'] >= first and ('CommandClient(0).WaitAck->CommandClient(0).Sending' in e['transition'] or 'CommandClient(0).WaitAck->CommandClient(0).Failed' in e['transition'])]
    execution = next(e['time'] for e in events if e['time'] >= first and 'CommandServer(0).Decide->CommandServer(0).Idle' in e['transition'])
    save(OUT/'failure_trace_summary.json', dict(raw_log=failure['log_path']+'/stdout.log', first_start_command=first,
        command_admission_times=[e['time'] for e in admissions], timeout_times=[e['time'] for e in timeout_events],
        abstract_start_execution=execution, failure_time=end, packets=packets, final_variables=events[-1]['after']))
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
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E05_failure_timeline.{ext}', dpi=180)
    plt.close(fig)
    print('AUDIT PASSED:', {k: len(v) for k, v in categories.items()})
    for r in [item for values in categories.values() for item in values]:
        print(r['configuration_id'], r['property_id'], r['result'], r['wall_seconds'], r['explored_states'], round(r['sampled_peak_rss_bytes']/1024**2, 2))

if __name__ == '__main__': main()
