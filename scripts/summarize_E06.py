"""Audit ACK-priority evidence, export the GUI candidate and draw paired results."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from run_coordination_experiments import make_model, property_for
from summarize_E03 import trace_events

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'results/coordination'
OUT = BASE/'analysis_E06'
EXPERIMENT = ROOT/'experiments/E06_ack_priority'

@lru_cache(None)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')

def semantic(node):
    return (node.tag, tuple(sorted((k, v) for k, v in node.attrib.items() if k not in ['x', 'y'])),
            (node.text or '').strip(), tuple(semantic(c) for c in node if c.tag not in ['nail', 'queries']))

def audit(path):
    r = json.loads(path.read_text(encoding='utf-8'))
    assert r['result'] in ['satisfied', 'not_satisfied', 'maybe', 'timeout']
    for f, key in [(path.parent.parent/'model.xml', 'model_sha256'), (path.parent/'query.q', 'query_sha256'),
                   (path.parents[2]/'runner_snapshot.py', 'runner_sha256'), (ROOT/'models/08_final_version.xml', 'source_model_sha256'), (Path(r['verifyta_path']), 'verifyta_sha256')]:
        assert sha(f) == r[key], f
    raw = (path.parent/'stdout.log').read_text(encoding='utf-8')
    representation = r['search_options'][r['search_options'].index('--state-representation')+1]
    if r['result'] == 'timeout': assert r['wall_seconds'] >= r['time_limit_seconds']
    else:
        assert r['returncode'] == 0
        if r['result'] == 'maybe': assert representation == '3' and re.search(r'Formula.*\bMAY\b', raw)
        else: assert ('Formula is satisfied.' if r['result'] == 'satisfied' else 'Formula is NOT satisfied.') in raw
    assert r['query'] == property_for(r['property_id'], r['N'])[1]
    assert r['heartbeat_mode'] == 'active' and r['loss_mode'] == 'reliable'
    assert r['ack_timeout'] == 14 and r['d_max'] == 3 and r['max_retry'] == 2 and r['heartbeat_period'] == 20
    expected = make_model(3, 14, n=r['N'], heartbeat='active', scheduler=r['scheduler'])
    assert (path.parent.parent/'model.xml').read_bytes() == expected.encode('utf-8')
    cmd = [r['verifyta_path'], *r['search_options']] + (['-t', '0'] if r['trace_enabled'] else []) + ['model.xml', 'query.q']
    assert json.loads((path.parent/'command.json').read_text(encoding='utf-8')) == cmd
    assert r['time_limit_seconds'] == 120 and r['memory_limit_bytes'] == 8*1024**3
    return r

def audit_scheduler(n):
    original = ET.fromstring(make_model(3, 14, n=n, heartbeat='active'))
    priority = ET.fromstring(make_model(3, 14, n=n, heartbeat='active', scheduler='ack_priority'))
    observed = ET.fromstring(make_model(3, 14, n=n, heartbeat='active', scheduler='observed'))
    assert semantic(original.find('system')) == semantic(priority.find('system'))
    for model, guarded in [(copy.deepcopy(priority), True), (copy.deepcopy(observed), False)]:
        declaration = model.find('declaration')
        assert declaration.text.count('bool ackPending[N];\n') == 1
        declaration.text = declaration.text.replace('bool ackPending[N];\n', '')
        changed_admissions = []
        for t in model.findall('template'):
            name = t.findtext('name')
            if name == 'PacketNetwork':
                for edge in t.findall('transition'):
                    for label in list(edge.findall('label')):
                        if 'ackPending' in (label.text or ''):
                            assert guarded and label.get('kind') == 'guard' and label.text == 'forall (i : drone_id) !ackPending[i]'
                            assert edge.find('source').get('ref') == 'id0' and edge.find('target').get('ref') == 'id1'
                            sync = next(l.text for l in edge.findall('label') if l.get('kind') == 'synchronisation')
                            assert not sync.startswith(('accepted_tx[', 'denied_tx['))
                            changed_admissions.append(edge.get('id')); edge.remove(label)
            elif name == 'CommandServer':
                for edge in t.findall('transition'):
                    for label in list(edge.findall('label')):
                        if label.get('kind') != 'assignment': continue
                        eid = edge.get('id')
                        if eid == 'id92':
                            assert label.text == 'current = c, ackPending[id] = true'; label.text = 'current = c'
                        elif eid == 'id93':
                            assert label.text == 'execute(current), ackPending[id] = false'; label.text = 'execute(current)'
                        elif eid == 'id94':
                            assert label.text == 'ackPending[id] = false'; edge.remove(label)
            else: assert 'ackPending' not in ET.tostring(t, encoding='unicode')
        assert set(changed_admissions) == ({'id5', 'id8', 'id9', 'id11', 'id13', 'id14'} if guarded else set())
        assert semantic(model) == semantic(original)
    # Same flags in the passive control; the policy adds only six admission guards.
    for a, b in zip(priority.findall('template'), observed.findall('template')):
        if a.findtext('name') != 'PacketNetwork': assert semantic(a) == semantic(b)

def packets(events, start, end):
    out, active = [], None
    for e in events:
        t = e['transition']
        if 'Link.Idle->Link.Transmitting' in t:
            assert active is None
            active = dict(start=e['time'], kind=int(e['after']['Link.packet.kind']), peer=int(e['after']['Link.packet.peer']), cmd=int(e['after']['Link.packet.cmd']))
        if 'Link.Transmitting->Link.Delivered' in t or 'Link.Transmitting->Link.Lost' in t:
            assert active is not None
            out.append(dict(**active, end=e['time'], complete=True)); active = None
    if active: out.append(dict(**active, end=end, complete=False))
    return [dict(**p, relative_start=p['start']-start, relative_end=p['end']-start) for p in out if p['start'] >= start and p['start'] <= end]

def export_model():
    text = make_model(3, 14, n=3, heartbeat='active', scheduler='ack_priority')
    raw = ET.fromstring(text)
    # Place new guards in the existing empty row above each admission's sync label.
    def layout(m):
        edge = m.group(0)
        parsed = ET.fromstring(edge)
        if '<label kind="guard" x="420" y="0">forall' in edge:
            sync = next(l for l in parsed.findall('label') if l.get('kind') == 'synchronisation')
            edge = edge.replace('<label kind="guard" x="420" y="0">', f'<label kind="guard" x="420" y="{int(sync.get("y"))-19}">')
        return edge
    text = re.sub(r'<transition\b.*?</transition>', layout, text, flags=re.S)
    ids = ['P34', 'P35', 'P36', 'P37', 'P03', 'P05', 'P06', 'P29', 'P30', 'P31', 'P32', 'P25']
    queries = '<queries>\n' + '\n'.join('<query><formula>'+escape(property_for(pid, 3)[1])+'</formula><comment>'+escape(pid+': '+property_for(pid, 3)[0])+'</comment></query>' for pid in ids) + '\n</queries>'
    text = re.sub(r'<queries>.*?</queries>', queries, text, flags=re.S)
    assert semantic(ET.fromstring(text)) == semantic(raw)
    model = ROOT/'models/09_ack_priority.xml'
    model.write_text(text, encoding='utf-8', newline='')
    (EXPERIMENT/'queries_n3.q').write_text('\n\n'.join('// '+pid+': '+property_for(pid, 3)[0]+'\n'+property_for(pid, 3)[1] for pid in ids)+'\n', encoding='utf-8')
    save(OUT/'gui_model_audit.json', {'file': str(model.relative_to(ROOT)), 'sha256': sha(model), 'equivalence': 'Exact generated N=3 priority model except query list and guard label coordinates.'})

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    index = json.loads((EXPERIMENT/'evidence.json').read_text(encoding='utf-8'))
    groups = {}
    for category, runs in index['runs'].items():
        values = [audit(p) for run in runs for p in sorted((BASE/run).glob('*/P*/result.json'))]
        assert len(values) == index['expected_counts'][category], category
        groups[category] = values; save(OUT/(category+'_records.json'), values)
    all_rows = [r for values in groups.values() for r in values]
    assert len(all_rows) == 100
    for n in [1, 2, 3]:
        audit_scheduler(n)
        old = BASE/f'20261125T132211639271Z_E05/n{n}_dmax3_timeout14_hb_active_period20/model.xml'
        assert old.read_bytes() == make_model(3, 14, n=n, heartbeat='active').encode('utf-8')
    small = {(r['N'], r['scheduler'], r['property_id']): r for r in groups['small_exact']}
    for r in groups['instrumentation_control']:
        if r['property_id'] != 'P29': assert r['result'] == small[2, 'original', r['property_id']]['result']
        else: assert r['result'] == 'satisfied'
    proofs = {r['property_id']: r for r in groups['priority_overapprox_safety'] + groups['priority_overapprox_core']}
    for pid in ['P35', 'P36', 'P37', 'P29', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P13', 'P14', 'P30', 'P31', 'P32']:
        assert proofs[pid]['result'] == 'satisfied'
    assert proofs['P25']['result'] == 'maybe'
    for r in groups['small_exact']:
        if r['scheduler'] == 'ack_priority' and r['property_id'] != 'P15': assert r['result'] == 'satisfied'
    truth = {}
    selected = ['P35', 'P36', 'P37', 'HB_PROGRESS', 'P25']
    for n in [1, 2]:
        for policy in ['original', 'ack_priority']:
            for pid in selected:
                r = small[n, policy, 'P30' if pid == 'HB_PROGRESS' else pid]
                truth[n, policy, pid] = r['result']
                if pid == 'HB_PROGRESS': assert all(small[n, policy, f'P{30+i}']['result'] == 'satisfied' for i in range(n))
    original = {r['property_id']: r for r in groups['original_overapprox'] + groups['original_counterexamples'] + [r for r in groups['diagnostics'] if r['scheduler'] == 'original']}
    for pid in selected:
        truth[3, 'ack_priority', pid] = proofs['P30' if pid == 'HB_PROGRESS' else pid]['result']
        truth[3, 'original', pid] = original['P30' if pid == 'HB_PROGRESS' else pid]['result']
    completion = None
    if (EXPERIMENT/'completion_evidence.json').exists():
        from summarize_E06_completion_proof import main as audit_completion
        audit_completion()
        completion = json.loads((OUT/'completion_proof.json').read_text(encoding='utf-8'))
        assert completion['conclusion'] == 'satisfied_by_compositional_proof'
        truth[3, 'ack_priority', 'P25'] = 'satisfied'
    save(OUT/'outcome_summary.json', [dict(N=n, scheduler=policy, property=pid, result=value,
         basis='Prepared boundary plus exact continuation proof' if completion and (n, policy, pid) == (3, 'ack_priority', 'P25') else 'Original 100-record study')
         for (n, policy, pid), value in truth.items()])
    summary = dict(invocations=len(all_rows), results=dict(Counter(r['result'] for r in all_rows)),
                   categories={k: len(v) for k, v in groups.items()}, source_model_sha256=sha(ROOT/'models/08_final_version.xml'))
    if completion:
        summary['supplementary_completion_proof'] = 'completion_proof.json (separate from the historical 100 invocations)'
    save(OUT/'execution_summary.json', summary); save(OUT/'evidence_index.json', index)
    fig, ax = plt.subplots(figsize=(12, 6.6))
    configurations = [(n, p) for n in [1, 2, 3] for p in ['original', 'ack_priority']]
    code = {'not_satisfied': 0, 'satisfied': 1, 'maybe': 2, 'timeout': 2}
    grid = [[code[truth[n, p, pid]] for pid in selected] for n, p in configurations]
    ax.imshow(grid, cmap=ListedColormap(['#dfb28b', '#89b7a5', '#c4cbd3']), vmin=0, vmax=2, aspect='auto')
    for i in range(6):
        for j in range(5):
            label = 'TRUE*' if completion and (i, j) == (5, 4) else ['FALSE', 'TRUE', 'UNKNOWN'][grid[i][j]]
            ax.text(j, i, label, ha='center', va='center', fontsize=11)
    ax.set_yticks(range(6), [f'N={n} / '+('original' if p == 'original' else 'ACK priority') for n, p in configurations])
    ax.set_xticks(range(5), ['No retry\nexhaustion', 'No retry\ntrigger', 'Reply wait\nat most 6', 'Each pending HB\neventually sent', 'Prepared\nevitably Done'])
    ax.set_title('E06: ACK priority removes timeout exhaustion in the tested model', fontsize=15, fontweight='bold', pad=18)
    note = 'D=1..3, ACK_TIMEOUT=14, MAX_RETRY=2, HB_PERIOD=20, no loss.\nN=1,2: exact checks. N=3: concrete counterexamples plus decisive over-approximation proofs.\n'
    note += '* N=3 completion: verified Prepared boundary + exact universal continuation proof.\n' if completion else ''
    note += 'UNKNOWN: unresolved. Heartbeat progress checks every active drone.'
    fig.text(.5, .025, note, ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .17, 1, .98))
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E06_outcomes.{ext}', dpi=180)
    plt.close(fig)
    # Compare the E05 START0 failure with a concrete tight-bound START0 ACK witness.
    old_folder = BASE/index['historical_failure_trace']
    old_row = json.loads((old_folder/'result.json').read_text(encoding='utf-8'))
    assert old_row['result'] == 'satisfied' and old_row['model_sha256'] == sha(old_folder.parent/'model.xml')
    assert (old_folder.parent/'model.xml').read_bytes() == make_model(3, 14, n=3, heartbeat='active').encode('utf-8')
    old_events = trace_events(old_folder/'stdout.log')
    new_row = next(r for r in groups['diagnostics'] if r['property_id'] == 'P38')
    new_events = trace_events(ROOT/new_row['log_path']/'stdout.log')
    def start_time(events):
        return next(e['time'] for e in events if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition'] and e['after']['Link.packet.cmd'] == 1)
    first_old, first_new = start_time(old_events), start_time(new_events)
    assert old_events[-1]['after']['cmdFailed[0][1]'] == 1
    assert new_events[-1]['after']['cmdAccepted[0][1]'] == 1 and new_events[-1]['time']-first_new == 6
    traces = [dict(policy='original', start=first_old, end=old_events[-1]['time'], events=old_events, raw_log=str(old_folder.relative_to(ROOT)/'stdout.log')),
              dict(policy='ack_priority', start=first_new, end=new_events[-1]['time'], events=new_events, raw_log=str(Path(new_row['log_path'])/'stdout.log'))]
    for tr in traces: tr['packets'] = packets(tr['events'], tr['start'], tr['end'])
    save(OUT/'reply_comparison_traces.json', traces)
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
    for ext in ['png', 'svg']: fig.savefig(OUT/f'E06_reply_comparison.{ext}', dpi=180)
    plt.close(fig)
    lines = ['# E06 diagnostic events', '', 'Absolute model times are parsed from the original trace delays.', '']
    for r in groups['diagnostics']:
        events = trace_events(ROOT/r['log_path']/'stdout.log')
        save(OUT/(r['configuration_id']+'_'+r['property_id']+'_events.json'), events)
        lines += [f"## {r['scheduler']} / {r['property_id']}", '', f"Raw log: `{r['log_path']}/stdout.log`", '', '| Time | Event |', '|---:|---|']
        for e in events:
            if any(s in e['transition'] for s in ['CommandClient(0)', 'CommandServer(0).Decide->CommandServer(0).Idle', 'heartbeat_tx[', 'heartbeat_rx[']):
                lines.append(f"| {e['time']:g} | "+e['transition'].replace('\n', '; ').replace('|', '&#124;')+' |')
        lines.append('')
    (OUT/'trace_events.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    export_model()
    print('AUDIT PASSED:', json.dumps(summary, ensure_ascii=False))
    print('Exported models/09_ack_priority.xml with audited semantic equivalence to the tested N=3 candidate.')

if __name__ == '__main__': main()
