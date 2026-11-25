# E03 丢包位置 / Loss location

[结果报告 / Report](E_3_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

请求丢失与 ACK 丢失时，确认失败分别对应哪些 ARM 状态？

What ARM states can accompany confirmation failure under request or ACK loss?

## 假设 / Hypothesis

请求可能从未到达，回复也可能在命令已经执行后丢失。

A request can fail to reach its receiver and a reply can be lost after command execution.

## 自变量 / Factors

可靠、只丢请求、只丢 ACK、两种包均可丢。

Reliable, request loss only, ACK loss only, and loss of either kind.

## 控制 / Controls

沿用基线 N=3、传输时间、超时、重试和无心跳设置；任务上传可靠。原版 LOSSY=true 验证 21 项对照。

Use the reference N=3, transmission times, timeout, retries and inactive heartbeat. Mission upload is reliable. Run 21 checks with the original LOSSY=true setting.

## 实现 / Implementation

在实验副本用 DROP_COMMANDS 与 DROP_ACKS 控制原丢包边的包类型。

Use DROP_COMMANDS and DROP_ACKS in the generated models to restrict the packet kinds eligible on the existing loss edge.

## 查询与预算 / Queries and budget

P01–P22，诊断见证用 P10/P11/P18。精确 BFS，每条 120 秒、8 GiB。

P01–P22 with diagnostic witnesses for P10/P11/P18. Exact BFS, 120 s and 8 GiB per query.

## 解释范围 / Interpretation

P11 描述失败瞬间，P18 描述指定的无待处理命令中止状态，P22 检查之后是否仍将 ARM。

P11 checks the instant of failure, P18 checks the specified settled abort state, and P22 checks whether ARM must follow.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T125832488306Z_E03 --property P18
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
