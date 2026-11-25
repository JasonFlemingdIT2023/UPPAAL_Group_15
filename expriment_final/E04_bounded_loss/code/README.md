# 代码 / Code

| 文件或目录 / File or directory | 用途 / Purpose |
|---|---|
| [run_coordination_experiments.py](run_coordination_experiments.py) | 生成模型、选择 P 查询并调用 verifyta。 / Generate model variants, select P queries and call verifyta. |
| [run_E04_controls.py](run_E04_controls.py) | 执行有界实验的对照与诊断批次。 / Run the bounded-loss controls and diagnostic cases. |
| [models](models/) | 源模型和去重后的实验模型。 / Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL 性质查询。 / UPPAAL property queries. |
| [cases.csv](cases.csv) | 各查询的模型、选项与资源上限。 / Model, options and limits for each check. |
| [replay.py](replay.py) | 按配置调用 verifyta。 / Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | 从结果数据重新绘图。 / Regenerate the figures from the result data. |
| [configurations.json](configurations.json) | 实验参数网格。 / Experiment parameter grid. |

从本实验目录运行。复跑输出写入新的 `results/reproduced/` 目录。 / Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T134341195424Z_E04 --property P28
python code/plot_results.py
```

下列命令从基线生成新配置并运行验证。 / These commands generate fresh variants from the reference and verify them.

```powershell
foreach ($n in 1,3) { python code/run_coordination_experiments.py --suite E04 --drones $n }
python code/run_E04_controls.py
```
