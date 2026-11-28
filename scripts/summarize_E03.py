"""Audit the selected E03 study and derive its figure and trace event tables."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import re
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/coordination'
RUNS = ['20261125T125634385990Z_E03', '20261125T125747351623Z_E03',
        '20261125T125752125349Z_E03', '20261125T125832488306Z_E03', '20261125T125833850233Z_E03']
OUT = BASE / 'analysis_E03'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def trace_events(path):
    time, event = 0., None
    events = []
    for block in re.split(r'(?m)(?=^Delay:|^Transition:|^State:)', path.read_text(encoding='utf-8')):
        if block.startswith('Delay:'):
            value = block.splitlines()[0].split(':', 1)[1].strip()
            assert re.fullmatch(r'\d+(\.\d+)?', value), value
            time += float(value)
        elif block.startswith('Transition:'):
            event = {'time': time, 'transition': block.removeprefix('Transition:').strip()}
            events.append(event)
        elif block.startswith('State:') and event is not None:
            event['locations'] = block.splitlines()[1]
            event['after'] = {k: float(v) for k, v in re.findall(r'([A-Za-z0-9_().\[\]]+)=(-?\d+(?:\.\d+)?)', block)}
            event = None
    return events

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    records = []
    for run in RUNS:
        for p in sorted((BASE / run).glob('*/P*/result.json')):
            r = json.loads(p.read_text(encoding='utf-8'))
            assert sha(p.parent.parent / 'model.xml') == r['model_sha256']
            assert sha(p.parent / 'query.q') == r['query_sha256']
            assert sha(BASE / run / 'runner_snapshot.py') == r['runner_sha256']
            assert sha(ROOT / 'models/08_final_version.xml') == r['source_model_sha256']
            assert r['returncode'] == 0
            log = (p.parent / 'stdout.log').read_text(encoding='utf-8')
            expected = 'Formula is satisfied.' if r['result'] == 'satisfied' else 'Formula is NOT satisfied.'
            assert expected in log
            records.append(r)
    assert len(records) == 113
    main_rows = [r for r in records if not r['trace_enabled'] and r['loss_mode'] != 'legacy_both']
    assert len(main_rows) == 88
    lookup = {(r['loss_mode'], r['property_id']): r for r in main_rows}
    assert len(lookup) == 88
    for r in records:
        if r['loss_mode'] == 'legacy_both':
            assert r['result'] == lookup['both', r['property_id']]['result']
    baseline = BASE / '20261124T073157336815Z_baseline/dmax3_timeout14'
    for p in baseline.glob('P*/result.json'):
        r = json.loads(p.read_text(encoding='utf-8'))
        assert r['result'] == lookup['reliable', r['property_id']]['result']
    for mode, expected_req, expected_ack in [('reliable', False, False), ('request', True, False), ('reply', False, True), ('both', True, True)]:
        assert (lookup[mode, 'P19']['result'] == 'satisfied') == expected_req
        assert (lookup[mode, 'P20']['result'] == 'satisfied') == expected_ack
        assert lookup[mode, 'P21']['result'] == 'satisfied'
    save(OUT / 'audited_records.json', records)
    save(OUT / 'evidence_index.json', {'runs': RUNS, 'main_queries':88,'control_queries':21,'trace_queries':4})
    modes = ['reliable','request','reply','both']
    ids = ['P01','P08','P10','P11','P18','P19','P20']
    labels = ['P01: success possible','P08: confirmation failure possible',
              'P10: failed confirmation, already armed','P11: failed confirmation, not armed yet',
              'P18: settled abort, still not armed','P19: request loss possible','P20: ACK loss possible']
    matrix = [[int(lookup[m,p]['result']=='satisfied') for m in modes] for p in ids]
    fig, ax = plt.subplots(figsize=(11.5,6.2))
    ax.imshow(matrix, cmap=ListedColormap(['#e6ebef','#395b81']), vmin=0,vmax=1,aspect='auto')
    for i,row in enumerate(matrix):
        for j,value in enumerate(row):
            ax.text(j,i,'YES' if value else 'NO',ha='center',va='center',color='white' if value else '#293847',fontweight='bold')
    ax.set_xticks(range(4),['Reliable','Request loss only','ACK loss only','Both may be lost'])
    ax.set_yticks(range(7),labels)
    ax.set_title('E03: the same confirmation failure can hide different drone states',fontsize=13,pad=20,fontweight='bold')
    fig.text(.5,.025,'N=3 | delay=1..3 | ACK timeout=14 | 2 retransmissions | no heartbeat\nYES means reachable, not a probability. P18 requires an idle link and settled command processes.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.10,1,1))
    for ext in ['png','svg']:fig.savefig(OUT/f'E03_outcomes.{ext}',dpi=180)
    plt.close(fig)
    lines = ['# E03 diagnostic witness events','', 'Times below are concrete model times relative to drone 0 first command admission. They are witness values, not bounds.','']
    for r in records:
        if not r['trace_enabled']:continue
        folder = ROOT / r['log_path']
        events = trace_events(folder/'stdout.log')
        origin = next(e['time'] for e in events if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition'])
        name = r['loss_mode']+'_'+r['property_id']
        save(OUT/f'{name}_events.json',events)
        lines += [f'## {name}', '', f'Raw log: `{r["log_path"]}/stdout.log`', '', '| Relative time | Event |','|---:|---|']
        selected = []
        for e in events:
            t=e['transition'];a=e['after']; label=None
            if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in t:label='CMD0 admitted / ACK timer reset'
            elif 'CommandClient(0).WaitAck->CommandClient(0).Sending' in t:label='Timeout; retry pending'
            elif 'CommandClient(0).WaitAck->CommandClient(0).Failed' in t:label='Confirmation FAILED'
            elif 'CommandServer(0).Decide->CommandServer(0).Idle' in t and 'execute(current)' in t:label='ARM0 executes; ACK0 admitted'
            elif 'Link.Transmitting->Link.Lost' in t and a['Link.packet.peer']==0:label=('CMD0' if a['Link.packet.kind']==4 else 'ACK0')+' lost'
            elif 'Supervisor.Arming->Supervisor.Aborted' in t:label='Supervisor aborts coordination'
            if label and e['time']>=origin:
                lines.append(f'| {e["time"]-origin:g} | {label} |')
                selected.append((e['time']-origin,label))
        final=events[-1]
        lines += ['',f'Final locations: `{final["locations"]}`',f'Final armed[0]={final["after"]["armed[0]"]:g}, cmdFailed[0][ARM]={final["after"]["cmdFailed[0][0]"]:g}.','']
        print(name,selected,'FINAL armed0=',final['after']['armed[0]'])
    (OUT/'trace_events.md').write_text('\n'.join(lines),encoding='utf-8')
    print('AUDIT PASSED: 88 main + 21 control + 4 diagnostic checks; legacy-both and reliable controls agree.')

if __name__=='__main__':main()
