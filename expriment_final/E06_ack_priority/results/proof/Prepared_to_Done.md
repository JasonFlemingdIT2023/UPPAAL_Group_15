# 三机 Prepared → Done / Three-drone Prepared-to-Done proof

目标是在 N=3、每架 3 个任务项、心跳周期 20、传输时间 1–3、ACK 超时 14、最多重试 2 次、无丢包的 ACK 优先模型中证明 `Supervisor.Prepared --> Supervisor.Done`。

The goal is to establish `Supervisor.Prepared --> Supervisor.Done` under ACK priority with three drones, three mission items each, heartbeat period 20, service time 1–3, ACK timeout 14, up to two retries and no packet loss.

## 两项机器检查 / Two machine checks

| 检查 / Check | 模型 / Model | 查询和输出 / Query and output | 方法与结论 / Method and verdict |
|---|---|---|---|
| Prepared 边界 / Prepared boundary | [XML](../../code/models/n3_dmax3_timeout14_scheduler_ack_priority.xml) | [Query](../../code/queries/PreparedBoundary.q) · [Log](prepared_boundary_verdict.txt) | 完整模型的保守过近似安全检查，明确通过。 / Full-model safety check with conservative over-approximation, satisfied. |
| 后续必然完成 / Universal continuation | [XML](../../code/models/prepared_continuation.xml) | [Query](../../code/queries/ContinuationDone.q) · [Log](prepared_continuation_verdict.txt) | compact DBM 精确验证，`A<> Supervisor.Done` 通过。 / Exact compact DBM verification, `A<> Supervisor.Done` satisfied. |

完整模型检查确认，每次进入 Prepared 时，任务发送者和接收者均已完成，所有上传和任务安装标记为真，命令组件空闲且未发送 ARM 或 START。链路为空闲、零时间的 Delivered，或正在传输一条心跳。每个心跳发送者处在 Waiting 或 Pending。E06 的 P34 见证经过 Prepared 并到达 Done。 [审计结果](../analysis/completion_proof.json)

The full-model check establishes that at Prepared, all mission senders and receivers have finished, all upload and installation flags are true, and command components are idle with neither ARM nor START dispatched. The link is idle, in the zero-time Delivered state, or transmitting a heartbeat. Each heartbeat sender is Waiting or Pending. The E06 P34 witness passes through Prepared and reaches Done. [Audit result](../analysis/completion_proof.json)

## 状态覆盖 / State coverage

在证明副本中，每架无人机的心跳时钟可在长度为 20 的启动窗口内独立重置。时刻 20 进入 Prepared 时，三个心跳时钟因此各自覆盖 [0,20] 内任意实数。原模型已经 Pending 的发送者可对应到时钟值 20、立即走 Waiting → Pending 的状态。原 Pending 的时钟值只在发送后被重置，等待期间数值不会影响行为。

In the proof model, each heartbeat clock can be reset independently during a 20-unit initialization window. At entry to Prepared, the three clock values can independently take any real value in [0,20]. A sender already Pending in the full model maps to clock value 20 followed by an immediate Waiting → Pending transition. Its old clock value has no effect while pending and is reset on admission.

启动时，证明副本的链路可以空闲，也可以带任意无人机的一条在途心跳，剩余传输时间覆盖 [0,3]。原链路的 Delivered 只能经 committed 位置的零时间边回到 Idle。原规则继续处理随后每个新入网的包。

At initialization, the proof link can be idle or carry one heartbeat from any drone with residual service in [0,3]. Delivered in the full model returns to Idle in zero time through a committed location. The original rules process every subsequent packet.

任务发送者的 Done 和接收者的 Uploaded 无出边。命令客户端的旧计时值在首个命令准入时重置。连接监控组件两个位置都可接收心跳，其时钟和已见标记只记录接收。空闲链路的旧包信息在下一次准入时覆盖。对应数据可以省略或重建，原始命令、ACK 准入、心跳和主管转换仍适用。

MissionSender.Done and MissionReceiver.Uploaded have no outgoing edges. The old command-client clock is reset on first command admission. Both connection-monitor locations accept heartbeats, and the monitor clock and seen flags only record reception. The next admission overwrites the idle link's old packet. These values can be omitted or reconstructed while the original command, ACK admission, heartbeat and supervisor transitions continue to apply.

取任一完整模型的 Prepared 状态，第一项检查保证它满足以上边界。上述映射让其后续执行在证明副本中都有对应执行。第二项检查证明副本的所有执行皆到达 Done，因此完整模型从该 Prepared 状态出发的所有执行也到达 Done。对可达的任一 Prepared 状态都成立。

Take any reachable Prepared state in the full model. The first check places it within the stated boundary. The mapping gives a corresponding proof-model execution for each of its continuations. The second check shows that every proof-model execution reaches Done. Every full-model continuation from this Prepared state therefore reaches Done, and the argument applies to every reachable Prepared state.

## 复现 / Reproduction

从 E06 目录执行。 / Run from the E06 directory.

```powershell
python code/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python code/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
```

完整模型直接查询在约 814 秒停止。候选完成时限的被动计时检查分别返回 MAY NOT 和超时。上述证明的结论是最终到达 Done。 [直接查询记录](../records.csv)

The direct full-model check was stopped after about 814 seconds. The passive timer checks for a candidate completion deadline returned MAY NOT and timeout. The proof establishes eventual completion. [Supplementary run index](../analysis/completion_proof.json)
