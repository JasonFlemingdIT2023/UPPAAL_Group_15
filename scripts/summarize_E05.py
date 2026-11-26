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
from summarize_E03 import trace_events
from run_coordination_experiments import make_model, property_for

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/coordination'
OUT = BASE / 'analysis_E05'
IDS = ['P01', 'P03', 'P08', 'P24']
sys.path.insert(0, str(ROOT/'expriment_final/E05_heartbeat/code'))
from plot_activation import plot_activation

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


def summarize_followup(index, baseline_rows):
    """Keep the original cost observations and resolve verdicts from matched inputs."""
    baseline = {r['property_id']: r for r in baseline_rows if r['N'] == 3 and r['heartbeat_mode'] == 'active'}
    properties = {}
    for pid, retry_path in index['extended_bfs'].items():
        first = baseline[pid]
        retry = audit(BASE/retry_path/'result.json')
        prior_path = index['prior_decisive'][pid]
        prior = audit(BASE/prior_path/'result.json')
        assert first['result'] == 'timeout' and prior['result'] == 'satisfied'
        assert all((r['model_sha256'], r['query_sha256']) == (first['model_sha256'], first['query_sha256'])
                   for r in (retry, prior))
        assert retry['search_options'] == first['search_options'] and not retry['trace_enabled']
        assert retry['time_limit_seconds'] == index['time_limit_seconds']
        assert retry['memory_limit_bytes'] == index['memory_limit_bytes']
        opts = prior['search_options']
        if pid == 'P03':
            assert opts[opts.index('--state-representation') + 1] == '3'
        else:
            assert opts[opts.index('-o') + 1] == '1' and prior['trace_enabled']

        def measurement(record, run=None):
            return dict(run=run or record['log_path'].replace('\\', '/').split('/')[2],
                        result=record['result'], wall_seconds=record['wall_seconds'],
                        time_limit_seconds=record['time_limit_seconds'],
                        memory_limit_bytes=record['memory_limit_bytes'],
                        sampled_peak_rss_bytes=record['sampled_peak_rss_bytes'],
                        explored_states=record['explored_states'], stored_states=record['stored_states'])

        retry_measurement = measurement(retry, retry_path.split('/')[0])
        if retry['result'] == 'satisfied':
            final = dict(retry_measurement, short_method='extended BFS')
        else:
            assert retry['result'] in ('timeout', 'memory_limit')
            final = dict(measurement(prior, prior_path.split('/')[0]),
                         short_method='E06 conservative proof' if pid == 'P03' else 'DFS witness')
        properties[pid] = dict(initial_bfs=measurement(first), extended_bfs=retry_measurement, final=final)
    assert set(properties) == {'P01', 'P03', 'P08'}
    return dict(configuration='n3_dmax3_timeout14_hb_active_period20',
                parallel_jobs=index['parallel_jobs'], properties=properties)

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
    followup_path = ROOT/'experiments/E05_heartbeat/activation_followup.json'
    followup = None
    if followup_path.exists():
        followup = summarize_followup(json.loads(followup_path.read_text(encoding='utf-8')), rows)
        save(OUT/'activation_followup.json', followup)
    plot_activation(rows, OUT, followup)
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
