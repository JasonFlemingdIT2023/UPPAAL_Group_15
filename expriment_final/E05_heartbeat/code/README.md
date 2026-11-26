# Code

| File or directory | Purpose |
| --- | --- |
| [run_coordination_experiments.py](run_coordination_experiments.py) | Generate model variants, select P queries and call verifyta. |
| [models](models/) | Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL property queries. |
| [cases.csv](cases.csv) | Model, options and limits for each check. |
| [replay.py](replay.py) | Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | Regenerate the figures from the result data. |
| [plot_activation.py](plot_activation.py) | Draw the activation figure from property verdicts and cost data. |

Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T132904048744Z_E05 --property P08
python code/plot_results.py
```

These commands generate fresh variants from the reference and verify them.

```powershell
python code/run_coordination_experiments.py --suite E05
python code/run_coordination_experiments.py --suite E05 --drones 2 --heartbeat active --hb-period 40
python code/run_coordination_experiments.py --suite E05 --drones 2 --heartbeat active --hb-offsets staggered
```

The extended BFS checks for three drones with heartbeat enabled can be replayed one query at a time. The recorded follow-up ran the three searches concurrently, with a 600 s timeout and a 2 GiB sampled RSS cap per query.

```powershell
python code/run_coordination_experiments.py --suite E05 --drones 3 --heartbeat active --properties P01 P03 P08 --limit 600 --memory-gib 2
```
