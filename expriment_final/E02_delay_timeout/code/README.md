# 代码 / Code

| 文件或目录 / File or directory | 用途 / Purpose |
|---|---|
| [run_coordination_experiments.py](run_coordination_experiments.py) | 生成模型、选择 P 查询并调用 verifyta。 / Generate model variants, select P queries and call verifyta. |
| [models](models/) | 源模型和去重后的实验模型。 / Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL 性质查询。 / UPPAAL property queries. |
| [cases.csv](cases.csv) | 各查询的模型、选项与资源上限。 / Model, options and limits for each check. |
| [replay.py](replay.py) | 按配置调用 verifyta。 / Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | 从结果数据重新绘图。 / Regenerate the figures from the result data. |
| [configurations.json](configurations.json) | 实验参数网格。 / Experiment parameter grid. |

从本实验目录运行。复跑输出写入新的 `results/reproduced/` 目录。 / Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261124T073421895292Z_pilot --property P08
python code/plot_results.py
```

下列命令从基线生成新配置并运行验证。 / These commands generate fresh variants from the reference and verify them.

```powershell
python code/run_coordination_experiments.py --suite baseline --properties P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 P11 P12 P13 P14 P15 P16
1..3 | ForEach-Object { python code/run_coordination_experiments.py --suite E02 --repetition $_ }
```
