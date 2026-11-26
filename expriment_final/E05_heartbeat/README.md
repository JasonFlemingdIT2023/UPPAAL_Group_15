# E05 心跳流量 / Heartbeat traffic

[结果报告 / Report](E_5_report.md) · [代码 / Code](code/README.md) · [结果与证据 / Results and evidence](results/README.md)

## 问题 / Question

心跳如何影响允许的执行和验证成本？改变周期或首次释放相位有什么效果？

How does heartbeat traffic change the allowed executions and verification cost, and how do the period and first release phase affect the comparison?

## 假设 / Hypothesis

心跳与命令竞争同一链路，会增加可达时间交错，并可能拖延 ACK。

Heartbeat and command traffic share the link, adding timing interleavings that can delay ACKs.

## 自变量 / Factors

N=1、2、3 配对测试心跳开关，默认周期 20。N=2 补测周期 40 与周期 20 首次错开。

Pair heartbeat off/on at N=1, 2, 3, with period 20. At N=2 also test period 40 and period 20 with staggered first releases.

## 控制 / Controls

固定每架 3 个任务项、传输 1–3、ACK 超时 14、最多重传 2 次、无丢包，采用原调度。

Use three mission items per drone, service time 1–3, ACK timeout 14, up to two retries, no loss and original scheduling.

## 实现 / Implementation

用 system 组合启停 HBSender 和 ConnectionMonitor。首次错开在初次等待中加入 floor(id×周期/N)，首次准入后清零。

Enable or disable HBSender and ConnectionMonitor through system composition. First-release staggering adds floor(id×period/N) to the first wait and clears it at the first admission.

## 查询与预算 / Queries and budget

P01、P03、P08、P24。精确 BFS 主实验与 DFS 补查每条 120 秒、8 GiB。三机启用心跳的 P01、P03、P08 另做延长 BFS 检查，每条 600 秒、2 GiB。

P01, P03, P08 and P24. Main runs use exact BFS, and the initial DFS follow-ups have the same 120 s and 8 GiB per-query limits. Extended BFS checks for P01, P03 and P08 use a 600 s, 2 GiB budget per query.

## 解释范围 / Interpretation

心跳周期从网络准入计时，首次错开只影响首个周期。验证成本取自相同查询下的一次配对测量。

Heartbeat periods restart at link admission. The offset changes only the first release. Matched verification costs use one measurement per setting and query.

## 复现命令 / Reproduction

配置 `UPPAAL_VERIFYTA` 后，从本实验目录复跑代表性查询或所有已完成的检查。 / Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T132904048744Z_E05 --property P08
python code/replay.py --all
```

[交付包总览 / Package overview](../README.md) · [逐查询结果 / Per-query results](results/records.csv) · [实际查询 / Exact formulas](code/queries/README.md)
