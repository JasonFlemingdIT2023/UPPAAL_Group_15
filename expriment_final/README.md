# 第 15 组实验交付包 / Group 15 experiment package

本包包含机群任务上传、ARM 和 START 协调模型的六项 UPPAAL 实验。每份报告链接到模型、查询、验证结果与轨迹。

This package contains six UPPAAL experiments on fleet coordination for mission upload, ARM and START. Each report links to the models, queries, verdicts and traces.

| 实验 / Experiment | 核心结果 / Main result | 设计与命令 / Design and commands | 报告 / Report |
|---|---|---|---|
| E01 机群规模 / Fleet scaling | 3 架起允许重试计数增长，P05 探索状态随规模增长。 / Retry counter increments become reachable at three drones, and the P05 search grows with fleet size. | [README](E01_fleet_scaling/README.md) | [E01](E01_fleet_scaling/E_1_report.md) |
| E02 延迟与超时 / Delay and timeout | 无丢包时，9 组参数中有 4 组允许确认失败。 / Four of nine settings admit confirmation failure on a reliable link. | [README](E02_delay_timeout/README.md) | [E02](E02_delay_timeout/E_2_report.md) |
| E03 丢包位置 / Loss location | 确认失败时，ARM 可能已经执行或仍未执行。 / ARM can be executed or unexecuted at confirmation failure. | [README](E03_loss_location/README.md) | [E03](E03_loss_location/E_3_report.md) |
| E04 有界丢包与重试 / Bounded loss and retries | 在所测超时 24 配置中，R≥K 时 Prepared 后必到 Done。 / With timeout 24 in the tested grid, R≥K gives completion after Prepared. | [README](E04_bounded_loss/README.md) | [E04](E04_bounded_loss/E_4_report.md) |
| E05 心跳 / Heartbeat | 三机开启心跳后成功与确认失败均可达。 / Both success and confirmation failure are reachable with three heartbeat senders. | [README](E05_heartbeat/README.md) | [E05](E05_heartbeat/E_5_report.md) |
| E06 ACK 优先 / ACK priority | 当前三机配置排除重试耗尽，并证明 Prepared 后必到 Done。 / The tested three-drone policy excludes retry exhaustion and guarantees completion after Prepared. | [README](E06_ack_priority/README.md) | [E06](E06_ack_priority/E_6_report.md) |

## 基线与术语 / Reference and terminology

基线为小组的 08 模型，N=3，每架 3 个任务项，网络单槽，传输时间 1–3，ACK 超时 14，首次发送后最多重试 2 次，丢包与心跳关闭。各实验 README 列出相对于基线的变化。E06 的 09 模型在待发命令 ACK 与其他流量竞争时给予 ACK 优先权。

The group’s version 08 reference has three drones, three mission items per drone, a single-slot link, transmission time 1–3, ACK timeout 14, up to two retries after the initial send, no loss and inactive heartbeat. Each experiment README lists departures from the reference. E06 uses version 09 to give pending command ACKs priority over other traffic.

| 术语 / Term | 含义 / Definition |
|---|---|
| GCS / 地面控制站 | Ground control station |
| ACK / 确认回复 | Acknowledgement. The command model has accepted and denied replies. / 命令模型有接受与拒绝两类回复。 |
| Prepared / 准备完成 | 全队任务上传确认完成。 / Mission upload has been confirmed for the full fleet. |
| Done / 协调完成 | 地面站已收到全队 START 接受确认。 / The ground station has received every START acceptance. |
| 确认失败 / Confirmation failure | 等待 ACK 的重试预算已耗尽。 / The ACK wait has exhausted its retry budget. |
| 准入 / Admission | 消息获得链路时隙并开始传输。 / A packet gains the link slot and starts transmission. |
| P01 与 P25 / P01 and P25 | P01 检查是否存在成功执行。P25 检查到达 Prepared 后的所有执行是否最终成功。 / P01 asks if a successful execution exists. P25 asks if every continuation after Prepared eventually succeeds. |

## 环境与复现 / Environment and reproduction

记录使用 Windows 上的 UPPAAL 5.1.0-beta6。使用 Python 3.10 或更新版本，安装下列依赖并设置本机 verifyta 路径。打包复测环境为 Python 3.13.9、matplotlib 3.10.6、psutil 7.0.0。Python 组织运行并绘图，性质判定由 verifyta 产生。

The records use UPPAAL 5.1.0-beta6 on Windows. Use Python 3.10 or newer, install the dependencies below and set the path to your local verifyta. The packaged commands were tested with Python 3.13.9, matplotlib 3.10.6 and psutil 7.0.0. Python orchestrates the runs and plots results. verifyta supplies the property verdicts.

```powershell
python -m pip install -r requirements.txt
$env:UPPAAL_VERIFYTA = 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe'
```

进入任一实验目录后运行其 README 中的命令。Windows 下请使用可写且路径仅含 ASCII 字符的临时目录，脚本会在那里暂存实际验证输入。各实验的 `code/cases.csv` 指定模型、查询和验证选项，`results/records.csv` 提供逐项结果和对应见证。重跑结果写入 `results/reproduced/`。

Run the README commands from an experiment directory. On Windows, use a writable temporary directory with an ASCII-only path, where the scripts stage verifier inputs. Each `code/cases.csv` specifies the models, queries and verifier options. `results/records.csv` records verdicts and links to available witnesses. Replay outputs go to `results/reproduced/`.

时间参数使用模型单位，验证耗时使用秒。墙钟时间包含验证器启动。RSS 每 50 ms 采样，表中的峰值为采样值。归档保留超时与过近似未确定结果。

Model parameters use model time units and verifier runtime uses seconds. Wall time includes verifier startup. RSS is sampled every 50 ms and reported as the peak sample. The archive retains timeouts and inconclusive over-approximation results.

## 证明与 AI 使用 / Proof and AI assistance

UPPAAL 的模型、性质查询和验证日志共同构成验证证据。E06 另附中文及英文状态覆盖论证，将完整模型的边界检查和后续模型的精确完成性检查连接起来。 [E06 证明 / E06 proof](E06_ack_priority/results/proof/Prepared_to_Done.md)

The UPPAAL models, property queries and verifier logs form the verification evidence. E06 also includes a bilingual state-coverage argument that connects the full-model boundary check to the exact verification of the continuation model. [AI 使用记录 / AI assistance log](AI_usage_log.md)
