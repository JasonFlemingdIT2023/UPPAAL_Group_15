# E02 网络延迟与超时 / Delay and timeout

[结果报告 / Report](E_2_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

可靠链路上，哪些传输延迟与 ACK 超时组合会触发重试或耗尽？

Which transmission-delay and ACK-timeout combinations allow retries or retry exhaustion on a reliable link?

## 假设 / Hypothesis

共享链路的排队竞争会拉长回复时间，增大超时窗口可减少部分组合中的失败。

Shared-link contention extends reply waits. A longer timeout can exclude failure in some settings.

## 自变量 / Factors

D_MAX ∈ {2,3,5}，ACK_TIMEOUT ∈ {6,14,24}，全因子 9 组。

Full 3 × 3 grid with D_MAX ∈ {2,3,5} and ACK_TIMEOUT ∈ {6,14,24}.

## 控制 / Controls

N=3，D_MIN=1，每架 3 个任务项，重传上限 2，关闭丢包和心跳。基线是 D_MAX=3、ACK_TIMEOUT=14。

N=3, D_MIN=1, three mission items per drone, two allowed retries, reliable link and inactive heartbeat. Reference cell is D_MAX=3 and ACK_TIMEOUT=14.

## 实现 / Implementation

仅修改生成副本中的 D_MAX 与 ACK_TIMEOUT，保留迟到 ACK 接收路径。

Change D_MAX and ACK_TIMEOUT in generated models and retain late-ACK handling.

## 查询与预算 / Queries and budget

基线 P01–P16。网格 P01–P05、P08、P09、P15，每组 3 轮。补查 P01/P09/P08/P17 轨迹和 P10。精确 BFS，每条 120 秒、8 GiB。

P01–P16 for the reference, and P01–P05, P08, P09 and P15 for three grid repetitions. Supporting traces use P01/P09/P08/P17, with a P10 check. Exact BFS, 120 s and 8 GiB per query.

## 解释范围 / Interpretation

热图记录行为是否可达。数值为模型时间单位，实际轨迹中的等待时间对应单条执行。

The heatmap reports reachability. All model times use model units, and each trace describes one execution.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261124T073421895292Z_pilot --property P08
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
