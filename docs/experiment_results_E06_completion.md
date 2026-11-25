# E06 补充：三机 Prepared → Done 的分阶段证明

2026-11-26。目标性质为 `Supervisor.Prepared --> Supervisor.Done`。结论：当前三机 ACK 优先配置满足这条性质。证明使用两项 UPPAAL 验证结果，以及下述连接两项结果的状态覆盖论证。

固定配置：N=3、MISSION_SIZE=3、心跳开启、HB_PERIOD=20、D_MIN=1、D_MAX=3、ACK_TIMEOUT=14、MAX_RETRY=2、LOSSY=false。`models/08_final_version.xml` 和 `models/09_ack_priority.xml` 均未修改。

## 验证结果

| 检查 | 被验证的模型 | 方法 | 结果 | 本次墙钟时间 |
|---|---|---|---|---:|
| Prepared 时的状态边界 | 完整三机 ACK 优先模型 | 保守过近似，明确返回 satisfied | 成立 | 8.3554 秒 |
| `A<> Supervisor.Done` | 覆盖所有 Prepared 后续行为的验证副本 | 精确 compact DBM | 成立 | 2.8931 秒 |

由此推出完整模型的 `Prepared --> Done`。第二项不是只选取一条成功轨迹，而是检查验证副本的全部执行。计时包含进程启动，且与完整模型延长验证有运行重叠，不作为算法性能对比。

完整模型的直接 P25 查询另设 1,200 秒上限运行。在分阶段证明及审计完成后，于约 814.338 秒（13 分 34 秒）主动停止，当时仍未返回性质结论，驻留内存约 4.40 GiB。这条记录标记为 `interrupted_after_compositional_proof`，不是超时或反例。直接查询的[停止记录](../results/coordination/20261125T171027951246Z_E06/n3_dmax3_timeout14_scheduler_ack_priority/P25/interruption.json)单独保留。

## 第一步：确认 Prepared 时已经发生了什么

在完整模型上验证 `A[] (Supervisor.Prepared imply 边界条件)`，得到明确的满足结果。边界条件包括：

- 三个任务发送者均在 Done，三个任务接收者均在 Uploaded；所有 uploadDone 和 missionInstalled 都为 true。
- 三个命令客户端和服务端均在 Idle，current 为 ARM，客户端重试次数为零。
- ARM/START 尚未发起，armed、started、ackPending、cmdAccepted、cmdDenied、cmdFailed 均未置位。
- 链路为空闲、处于零时间的 Delivered，或正在传输心跳。
- 每个心跳发送者或者在 Waiting 且计时不超过 20，或者在 Pending 且计时至少为 20。

这项检查使用完整上传过程和完整网络。准备状态的可达性已有 E06 的精确成功见证，因此边界检查有实际可达状态作为对象。

## 第二步：覆盖 Prepared 时所有可能的心跳状态

验证副本保留原有主管、命令客户端、命令服务端、心跳、连接监视器和网络的全部原始转换。已结束的任务发送者/接收者不再实例化。新增的启动过程只用来生成进入 Prepared 时的各种环境状态。

**心跳时间相位。** 启动过程经过 20 个时间单位，每个心跳发送者可以在这段时间内任意选择一次重置其 period。启动结束时，三个 period 可以分别取 [0,20] 内任意实数值，而不是只枚举整数或几种固定错峰。

**已经等待发送的心跳。** 原模型 Pending 中 period 可以大于 20，但这个值在发送之前不参与任何守卫或不变式，发送时又会重置为零。因此把这类状态映射为 period=20 的 Waiting，再立即进入 Pending，就覆盖了它的后续行为。三个心跳可以独立处于这种情况。

**已经在途的心跳。** 启动时链路可以直接空闲，也可以带有任意一架无人机的一条残余心跳包。该包允许在 0～3 个时间单位后送达。原模型在途包的剩余服务时间一定是这个区间的子集，所以这个设置覆盖原来的所有剩余传输时间。随后所有新包继续使用原来的 1～3 传输窗口。

**Prepared 时的 Delivered。** 该位置 committed，只有不更新任何变量的 Delivered→Idle 转换。先消去这个零时间步骤，就得到上述空闲情况；原模型在这一步之前也不能让时间流逝。

启动结束时主管进入 Prepared，uploadDone 和 missionInstalled 均为 true。命令、ACK 优先、心跳周期、超时、重试和无丢包规则与完整模型一致。

## 为什么这个副本足以证明原性质

任取完整模型中一个 Prepared 状态：第一项验证保证它满足边界条件。将它的心跳相位和链路状态映射到上述启动过程，就能在验证副本中得到覆盖其后续行为的状态。

映射还省略了不会影响后续控制流程的数据：

- MissionSender.Done 和 MissionReceiver.Uploaded 没有出边，删除这些实例不会取消任何后续通信。
- CommandClient.x 在 Idle/Sending 不用于守卫或不变式，第一次命令入网时重置；其 Prepared 时的旧值不影响后续行为。
- ConnectionMonitor.age 和 heartbeatSeen 只记录心跳，没有被命令、网络或主管的守卫读取；监视器的两个接收位置都能接收下一条心跳。
- 空闲链路保留的旧 packet 在下次准入时被完整覆盖；在途心跳的 peer 则在副本中保留对应选择。

因此，原模型每一种 Prepared 后续执行，都能由验证副本覆盖。副本还允许某些原模型未必可达的心跳相位组合和剩余传输情况，验证范围更大。UPPAAL 对副本精确验证 `A<> Supervisor.Done` 返回 satisfied，意味着这个更大的集合中也没有无法完成的执行，所以原模型满足 `Prepared --> Done`。这里没有额外加入公平调度假设，也没有限制心跳来让命令优先。

脚本逐项检查：删除新增启动位置、转换、声明并恢复初始位置后，所有原始协议模板恢复一致。完整模型边界验证、生成副本、实际查询、验证器命令、原始输出和哈希均保留。状态覆盖关系由本节的论证建立；结构审计检查模板未被改写。

## 其他尝试

另一个副本仅在进入 Prepared 时重置观察时钟，检查“未 Done 时，经过时间是否始终不超过 120”。过近似返回 MAY NOT；精确检查达到 300 秒上限。这两项均未得到确定结论，不用来支持上述证明，也没有证明 120 是完成时间上界。

第一次启动副本把时钟守卫放在 urgent 通道边上，被验证器拒绝。改为普通 broadcast，并由启动位置的时间不变式及守卫确保启动恰好发生在 t=20，重新验证通过。被拒绝的记录单独列为开发尝试。

## 证据与复现

- [补充证据索引](../experiments/E06_ack_priority/completion_evidence.json)
- [审计后的两项证明结果](../results/coordination/analysis_E06/completion_proof.json)
- [边界验证原始输出](../results/coordination/20261125T171730362946Z_E06_prepared_boundary/stdout.log)
- [后半段精确验证原始输出](../results/coordination/20261125T171822124561Z_E06_prepared_progress/stdout.log)
- [用于证明的副本](../results/coordination/20261125T171822124561Z_E06_prepared_progress/model.xml)

在仓库根目录执行：

```powershell
python scripts/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python scripts/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
python scripts/summarize_E06_completion_proof.py
```

新执行产生新的目录；审计脚本默认审计补充索引中固定的证据。
