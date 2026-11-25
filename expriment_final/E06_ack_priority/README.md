# E06 ACK 优先调度 / ACK-priority scheduling

[结果报告 / Report](E_6_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

优先发送待发命令 ACK 能否消除 E05 的失败，同时维持心跳和任务进展？

Can prioritizing pending command ACKs remove the E05 failure while retaining heartbeat and coordination progress?

## 假设 / Hypothesis

待发 ACK 占用下一个空闲链路时隙，可减少回复等待并排除超时重试。

Giving pending ACKs the next free link slot shortens reply waits and can exclude timeout retries.

## 自变量 / Factors

原调度与 ACK 优先，比较 N=1、2、3；N=2 增设只记录标记的对照。

Compare original and ACK-priority scheduling at N=1, 2, 3. N=2 includes a passive-flag control.

## 控制 / Controls

心跳开启、周期 20，其余参数取基线值。链路仍为单槽，正在传输的包完成后才选下一包。

Heartbeat is active with period 20 and remaining parameters follow the reference. The single-slot link selects another packet after the current transmission finishes.

## 实现 / Implementation

服务端进入 Decide 时置 ackPending，回复准入时清除。六条非命令 ACK 准入边要求所有标记为假。

Set ackPending at Decide entry and clear it at reply admission. Six non-command-ACK admission edges require every flag to be false.

## 查询与预算 / Queries and budget

核心 P25、P29–P32、P34–P38；回归和分解查询见查询清单。主批每条 120 秒、8 GiB，采用精确验证和凸包过近似。证明两部分分别限 120/300 秒；延长的直接 P25 限 1,200 秒，主动停止于约 814 秒。

Core queries are P25, P29–P32 and P34–P38. See the query list for regression and decomposition checks. The main study uses exact and convex-hull over-approximate verification with 120 s and 8 GiB per query. The two proof checks have 120/300 s limits. Extended direct P25 had a 1,200 s limit and was stopped at about 814 s.

## 解释范围 / Interpretation

回复上界从命令准入开始。P25 在 N=3 的结论来自 Prepared 边界与后续行为覆盖的分阶段证明。

The reply bound starts at request admission. For N=3, P25 follows from the Prepared boundary and the continuation coverage argument.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T171822124561Z_E06_prepared_progress --property ContinuationDone
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
