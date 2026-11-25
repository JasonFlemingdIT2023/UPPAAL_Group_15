# E04 有界丢包与重试 / Bounded loss and retries

[结果报告 / Report](E_4_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

整个协调过程最多损失 K 个包时，重试次数 R 如何影响完成保证？

How does retry limit R affect completion when the whole coordination attempt can lose at most K packets?

## 假设 / Hypothesis

有界损失和足够的 ACK 等待时间使有限重试能够提供完成保证。

A bounded loss budget and sufficient time for replies can make completion provable with finite retries.

## 自变量 / Factors

N=1、3，每个规模完整测试 K ∈ {0,1,2} × R ∈ {0,1,2}。

Test the full K ∈ {0,1,2} × R ∈ {0,1,2} grid for N=1 and N=3.

## 控制 / Controls

D_MIN=1、D_MAX=3、ACK_TIMEOUT=24、无心跳、任务上传可靠；另测无限制丢包、可靠链路和超时 14。

D_MIN=1, D_MAX=3, ACK_TIMEOUT=24, inactive heartbeat, reliable mission traffic. Controls cover unrestricted loss, a reliable link and timeout 14.

## 实现 / Implementation

添加仅由网络使用的全局适用预算 K，在丢包边检查 lossCount<K 并递增局部计数。R 是每次命令首次发送后的重传上限。

Use a shared budget K enforced by the network. The loss edge requires lossCount<K and increments its local counter. R counts the allowed retransmissions after each initial command.

## 查询与预算 / Queries and budget

主实验 P01–P08、P10–P16、P21、P25、P27、P28，共 19 条；P26 用于启动条件诊断。精确 BFS，每条 120 秒、8 GiB。

Nineteen main queries: P01–P08, P10–P16, P21, P25, P27 and P28. P26 checks startup in diagnostics. Exact BFS, 120 s and 8 GiB per query.

## 解释范围 / Interpretation

K 跨所有无人机、ARM/START 请求与回复共享。P25 的保证从 Prepared 开始，适用于矩阵的具体参数。

K is shared across drones and across ARM/START requests and replies. P25 starts at Prepared and applies to the tested grid settings.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T134341195424Z_E04 --property P28
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
