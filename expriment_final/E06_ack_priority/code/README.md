# 代码 / Code

| 文件或目录 / File or directory | 用途 / Purpose |
|---|---|
| [run_coordination_experiments.py](run_coordination_experiments.py) | 生成模型、选择 P 查询并调用 verifyta。 / Generate model variants, select P queries and call verifyta. |
| [run_E06_completion_bound.py](run_E06_completion_bound.py) | 用被动计时器检查 Prepared 后的候选时间上界。 / Check a candidate time bound after Prepared with a passive timer. |
| [run_E06_followups.py](run_E06_followups.py) | 执行小规模、被动标记和部分诊断对照。 / Run the small-fleet, passive-flag and selected diagnostic controls. |
| [run_E06_prepared_abstraction.py](run_E06_prepared_abstraction.py) | 生成并运行完整模型边界检查与后续模型完成性查询。 / Generate and run the full-model boundary and continuation checks. |
| [models](models/) | 源模型和去重后的实验模型。 / Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL 性质查询。 / UPPAAL property queries. |
| [cases.csv](cases.csv) | 各查询的模型、选项与资源上限。 / Model, options and limits for each check. |
| [replay.py](replay.py) | 按配置调用 verifyta。 / Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | 从结果数据重新绘图。 / Regenerate the figures from the result data. |

从本实验目录运行。复跑输出写入新的 `results/reproduced/` 目录。 / Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T171822124561Z_E06_prepared_progress --property ContinuationDone
python code/plot_results.py
```

下列命令从基线生成新配置并运行验证。 / These commands generate fresh variants from the reference and verify them.

```powershell
python code/run_E06_followups.py
python code/run_coordination_experiments.py --suite E06 --scheduler ack_priority --drones 3 --state-representation 3 --properties P35 P36 P37 P29 P03
python code/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python code/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
```
