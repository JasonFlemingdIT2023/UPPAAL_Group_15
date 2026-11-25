"""Regenerate the experiment figures from the included result data."""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT/'results/analysis'/name).read_text(encoding='utf-8'))


def main():
    with (ROOT/'results/records.csv').open(encoding='utf-8', newline='') as stream:
        lookup = {(r['loss_mode'], r['property']): {'result': r['outcome']}
                  for r in csv.DictReader(stream)
                  if r['trace'] == 'False' and r['loss_mode'] != 'legacy_both'}
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
    for ext in ['png','svg']:fig.savefig((ROOT/'results/figs') /f'E03_outcomes.{ext}',dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
