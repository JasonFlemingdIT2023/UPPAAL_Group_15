"""Audit fixed E01 evidence and plot per-query scaling, without pooling old runs."""
import sys
sys.dont_write_bytecode = True
import json
import hashlib
import statistics
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from summarize_E03 import trace_events

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/coordination'
RUNS = ['20261125T131340771891Z_E01','20261125T131410593895Z_E01','20261125T131448881664Z_E01']
TRACE = '20261125T131521932777Z_E01/n4_dmax3_timeout14/P17'
OUT = BASE / 'analysis_E01'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')

def audit(p):
    row=json.loads(p.read_text(encoding='utf-8'))
    assert row['returncode']==0 and row['result'] in ['satisfied','not_satisfied']
    for file,key in [(p.parent.parent/'model.xml','model_sha256'),(p.parent/'query.q','query_sha256'),(p.parents[2]/'runner_snapshot.py','runner_sha256'),(ROOT/'models/08_final_version.xml','source_model_sha256')]:
        assert sha(file)==row[key]
    text=(p.parent/'stdout.log').read_text(encoding='utf-8')
    assert ('Formula is satisfied.' if row['result']=='satisfied' else 'Formula is NOT satisfied.') in text
    model=ET.parse(p.parent.parent/'model.xml').getroot()
    n=row['N'];system=model.findtext('system')
    assert f'const int N = {n};' in model.findtext('declaration')
    assert system.count('= MissionSender(')==n and system.count('= MissionReceiver(')==n
    if row['property_id']=='P14':assert row['query'].count('.receivedCount')==n
    if row['property_id']=='P23':assert row['query'].count('.retries')==n
    return row

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    rows=[audit(p) for run in RUNS for p in sorted((BASE/run).glob('*/P*/result.json'))]
    assert len(rows)==168
    groups=defaultdict(list)
    for r in rows:groups[r['N'],r['property_id']].append(r)
    assert len(groups)==56
    summary=[]
    for (n,pid),g in sorted(groups.items()):
        assert {r['repetition'] for r in g}=={1,2,3} and len(g)==3
        for key in ['result','model_sha256','query_sha256','search_options','tool_version','explored_states','stored_states']:
            assert all(r[key]==g[0][key] for r in g)
        if n==3 and pid!='P23':
            old=BASE/f'20261124T073157336815Z_baseline/dmax3_timeout14/{pid}/result.json'
            assert json.loads(old.read_text(encoding='utf-8'))['result']==g[0]['result']
        s=dict(N=n,property_id=pid,result=g[0]['result'],query=g[0]['query'],explored_states=g[0]['explored_states'],stored_states=g[0]['stored_states'])
        for key in ['wall_seconds','cpu_user_ms','sampled_peak_rss_bytes','reported_resident_kib']:
            values=[r[key] for r in g if r[key] is not None]
            s[key+'_median']=statistics.median(values) if values else None
            s[key+'_min']=min(values) if values else None
            s[key+'_max']=max(values) if values else None
        summary.append(s)
    save(OUT/'audited_records.json',rows)
    save(OUT/'scaling_summary.json',summary)
    save(OUT/'evidence_index.json',{'formal_runs':RUNS,'trace':TRACE,'formal_queries':168,'trace_queries':1})
    lookup={(s['N'],s['property_id']):s for s in summary}
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for pid,color in [('P01','#3979ad'),('P05','#a95731'),('P08','#4e8469')]:
        values=[lookup[n,pid] for n in range(1,5)]
        for ax,key,title in [(axes[0,0],'wall_seconds','Wall time (s), log scale'),(axes[1,1],'sampled_peak_rss_bytes','Sampled peak RSS (MiB)')]:
            scale=1024**2 if key.endswith('bytes') else 1
            med=[s[key+'_median']/scale for s in values]
            lo=[s[key+'_min']/scale for s in values];hi=[s[key+'_max']/scale for s in values]
            ax.plot(range(1,5),med,'o-',label=pid,color=color)
            ax.fill_between(range(1,5),lo,hi,color=color,alpha=.15)
            ax.set_title(title,fontsize=11)
        for ax,key,title in [(axes[0,1],'explored_states','Explored symbolic states (log scale)'),(axes[1,0],'stored_states','Stored symbolic states (log scale)')]:
            ax.plot(range(1,5),[s[key] for s in values],'o-',label=pid,color=color)
            ax.set_yscale('log');ax.set_title(title,fontsize=11)
    axes[0,0].set_yscale('log')
    for ax in axes.flat:
        ax.set_xticks([1,2,3,4]);ax.set_xlabel('Number of drones N')
        ax.grid(alpha=.18);ax.legend(frameon=False);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('E01: verification cost grows with fleet size',fontsize=16,fontweight='bold')
    fig.text(.5,.025,'P01: success reachability | P05: pre-outcome deadlock exclusion | P08: client 0 failure reachability\nMedian and min-max over 3 runs. Wall time includes startup/license overhead (notably N=1 P01).\nSampled RSS is a lower bound on peak. State counts are query-specific, not a fleet-size-independent full state-space measure.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.13,1,.95))
    for ext in ['png','svg']:fig.savefig(OUT/f'E01_scaling.{ext}',dpi=180)
    plt.close(fig)
    # Actual diagnostic trace; kept separate from benchmark measurements.
    tr=audit(BASE/TRACE/'result.json')
    assert tr['trace_enabled']
    events=trace_events(BASE/TRACE/'stdout.log');save(OUT/'n4_retry_trace_events.json',events)
    start=next(e['time'] for e in events if 'CommandClient(0).Sending->CommandClient(0).WaitAck' in e['transition'])
    lines=['# N=4 retry and late-ACK witness','',f'Raw log: `{TRACE}/stdout.log`','', 'Times are relative to client 0 first command admission; one witness, not a timing bound.','', '| Relative time | Transition |','|---:|---|']
    for e in events:
        t=e['transition']
        if e['time']>=start and ('CommandClient(0)' in t or 'CommandServer(0).Decide->CommandServer(0).Idle' in t):
            lines.append(f'| {e["time"]-start:g} | '+t.replace('\n','; ').replace('|','&#124;')+' |')
    (OUT/'n4_retry_trace.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('AUDIT PASSED: 168 formal checks; all 56 groups agree across three repetitions; N=3 agrees with baseline; 1 witness.')
    for n in range(1,5):
        s=lookup[n,'P05']
        print(n,'P05',s['wall_seconds_median'],'s',s['explored_states'],'explored',s['stored_states'],'stored',s['sampled_peak_rss_bytes_median']/1024**2,'MiB',s['cpu_user_ms_median'],'CPU ms')
    print('\n'.join(lines))

if __name__=='__main__':main()
