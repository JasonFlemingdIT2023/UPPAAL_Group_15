# E01 机群规模 / Fleet scaling

[结果报告 / Report](E_1_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

机群规模如何影响协调结果和验证成本？

How does fleet size affect coordination and verification cost?

## 假设 / Hypothesis

更多并发会增加状态组合，并可能使命令等待超过超时。

More concurrent sessions increase the state space and may push reply waits past the timeout.

## 自变量 / Factors

无人机数量 N = 1、2、3、4。

Drone count N = 1, 2, 3, 4.

## 控制 / Controls

固定基线传输、ACK 超时、重试、无丢包与无心跳设置。每个规模检查三轮。

Use the reference delay, timeout, retries, reliable link and inactive heartbeat. Run three repetitions per fleet size.

## 实现 / Implementation

按 N 生成任务发送和接收实例及 system 组合，同步调整逐机查询。

Generate mission sender and receiver instances and system composition for each N, and adapt per-drone queries.

## 查询与预算 / Queries and budget

主实验 P01–P09、P13–P16、P23；N=4 轨迹 P17。精确 BFS，每条 120 秒、8 GiB。

P01–P09, P13–P16 and P23 in the main study, plus P17 for the N=4 trace. Exact BFS, 120 s and 8 GiB per query.

## 解释范围 / Interpretation

成本以同一查询和验证设置下的符号状态与耗时衡量。P09/P23 记录重试计数是否增长。

Cost uses symbolic states and runtime under matched query and verifier settings. P09/P23 measure whether a retry counter can increase.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T131521932777Z_E01 --property P17
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
