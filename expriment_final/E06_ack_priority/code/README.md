# Code

| File or directory | Purpose |
| --- | --- |
| [run_coordination_experiments.py](run_coordination_experiments.py) | Generate model variants, select P queries and call verifyta. |
| [run_E06_completion_bound.py](run_E06_completion_bound.py) | Check a candidate time bound after Prepared with a passive timer. |
| [run_E06_followups.py](run_E06_followups.py) | Run the small-fleet, passive-flag and selected diagnostic controls. |
| [run_E06_prepared_abstraction.py](run_E06_prepared_abstraction.py) | Generate and run the full-model boundary and continuation checks. |
| [models](models/) | Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL property queries. |
| [cases.csv](cases.csv) | Model, options and limits for each check. |
| [replay.py](replay.py) | Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | Regenerate the figures from the result data. |

Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T171822124561Z_E06_prepared_progress --property ContinuationDone
python code/plot_results.py
```

These commands generate fresh variants from the reference and verify them.

```powershell
python code/run_E06_followups.py
python code/run_coordination_experiments.py --suite E06 --scheduler ack_priority --drones 3 --state-representation 3 --properties P35 P36 P37 P29 P03
python code/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python code/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
```
