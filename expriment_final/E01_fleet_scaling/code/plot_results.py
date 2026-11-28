"""Regenerate the experiment figures from the included result data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'results/analysis'/name).read_text(encoding='utf-8'))


def main():
    summary = load('scaling_summary.json')
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
    for ext in ['png','svg']:fig.savefig((ROOT/'results/figs') /f'E01_scaling.{ext}',dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
