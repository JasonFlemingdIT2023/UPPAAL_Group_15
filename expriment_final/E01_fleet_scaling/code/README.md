# Code

| File or directory | Purpose |
| --- | --- |
| [run_coordination_experiments.py](run_coordination_experiments.py) | Generate model variants, select P queries and call verifyta. |
| [models](models/) | Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL property queries. |
| [cases.csv](cases.csv) | Model, options and limits for each check. |
| [replay.py](replay.py) | Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | Regenerate the figures from the result data. |
| [configurations.json](configurations.json) | Experiment parameter grid. |

Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T131521932777Z_E01 --property P17
python code/plot_results.py
```

These commands generate fresh variants from the reference and verify them.

```powershell
1..3 | ForEach-Object { python code/run_coordination_experiments.py --suite E01 --repetition $_ }
```
