# 代码 / Code

| 文件或目录 / File or directory | 用途 / Purpose |
|---|---|
| [run_coordination_experiments.py](run_coordination_experiments.py) | 生成模型、选择 P 查询并调用 verifyta。 / Generate model variants, select P queries and call verifyta. |
| [models](models/) | 源模型和去重后的实验模型。 / Source and deduplicated experiment models. |
| [queries](queries/README.md) | UPPAAL 性质查询。 / UPPAAL property queries. |
| [cases.csv](cases.csv) | 各查询的模型、选项与资源上限。 / Model, options and limits for each check. |
| [replay.py](replay.py) | 按配置调用 verifyta。 / Run verifyta using the case table. |
| [plot_results.py](plot_results.py) | 从结果数据重新绘图。 / Regenerate the figures from the result data. |
| [plot_activation.py](plot_activation.py) | 从判定和成本数据重绘开关对照图。 / Draw the activation figure from property verdicts and cost data. |

从本实验目录运行。复跑输出写入新的 `results/reproduced/` 目录。 / Run from the experiment directory. Replays write to a new directory under `results/reproduced/`.

```powershell
python code/replay.py --list
python code/replay.py --run 20261125T132904048744Z_E05 --property P08
python code/plot_results.py
```

下列命令从基线生成新配置并运行验证。 / These commands generate fresh variants from the reference and verify them.

```powershell
python code/run_coordination_experiments.py --suite E05
python code/run_coordination_experiments.py --suite E05 --drones 2 --heartbeat active --hb-period 40
python code/run_coordination_experiments.py --suite E05 --drones 2 --heartbeat active --hb-offsets staggered
```

三机心跳开启的延长 BFS 检查可以逐条复跑。发布的补查三条并行执行，每条时间上限 600 秒，采样 RSS 上限 2 GiB。 / The extended BFS checks for three drones with heartbeat enabled can be replayed one query at a time. The recorded follow-up ran the three searches concurrently, with a 600 s timeout and a 2 GiB sampled RSS cap per query.

```powershell
python code/run_coordination_experiments.py --suite E05 --drones 3 --heartbeat active --properties P01 P03 P08 --limit 600 --memory-gib 2
```
