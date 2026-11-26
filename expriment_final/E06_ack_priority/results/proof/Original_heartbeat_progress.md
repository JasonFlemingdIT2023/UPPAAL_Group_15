# 三机原调度的心跳进展 / Three-drone heartbeat progress under original scheduling

本说明证明 P30–P32。对每个 i，只要 `HBSender(i)` 进入 Pending，它最终都会通过 `heartbeat_tx[i]` 准入并回到 Waiting。模型为版本 08 原调度的三机心跳开启配置，任务大小为 3，心跳周期为 20，传输时间为 1–3，ACK 超时为 14，最多重传两次，链路可靠。 [验证模型](../../code/models/n3_dmax3_timeout14_scheduler_original.xml)

This argument establishes P30–P32. Whenever `HBSender(i)` enters Pending, it eventually synchronizes on `heartbeat_tx[i]` to gain admission and return to Waiting. The configuration is version 08 with original scheduling, three drones, three mission items, heartbeat period 20, service times 1–3, ACK timeout 14, up to two retries and a reliable link. [Model](../../code/models/n3_dmax3_timeout14_scheduler_original.xml)

## 验证前提 / Verified premises

| 查询 / Query | 结果 / Result | 证据 / Evidence |
|---|---|---|
| P06 `Link.Transmitting --> Link.Idle` | 满足，约 83.92 秒。 / Satisfied in about 83.92 s. | [查询 / Query](../../code/queries/P06.q) · [验证输出 / Verdict](original_packet_progress.txt) |
| P46 在途任务包始终有匹配的接收者 / Every in-flight mission packet has a matching receiver | 满足，约 31.93 秒。 / Satisfied in about 31.93 s. | [查询 / Query](../../code/queries/P46.q) · [验证输出 / Verdict](original_mission_receiver.txt) |

两项检查均在原调度模型上使用保守凸包过近似，UPPAAL 返回明确的 `Formula is satisfied`。P06 是证明所用的机器验证前提，P46 补充核验任务接收状态。此前 P30–P32 的直接过近似查询返回 `MAY NOT`，后续普通 DBM 加 LU 外推得到相同判定。 [逐查询记录](../records.csv) · [UPPAAL 对近似判定的说明](https://docs.uppaal.org/gui-reference/verifier/verifying/)

Both checks used conservative convex-hull over-approximation on the original model and returned a definite `Formula is satisfied`. P06 supplies the verified premise of the proof, and P46 independently checks mission receive states. The initial direct checks of P30–P32 returned `MAY NOT`, and the subsequent plain-DBM runs with LU extrapolation gave the same verdict. [Per-query results](../records.csv) · [UPPAAL verdict semantics](https://docs.uppaal.org/gui-reference/verifier/verifying/)

采用 compact DBM 和默认外推延长验证时，P30 在 600 秒上限处超时。三架的结论由同一有限流量论证得到，因此停止了随后启动的 P31 直接搜索。辅助的 P45 全模型无死锁检查返回 `MAY NOT`。上述两条未确定记录与 P06 的满足判定分别保留。 [补充检查](../analysis/heartbeat_followup.json)

With compact DBMs and automatic extrapolation, extended direct verification of P30 reached its 600 s limit. The same finite-traffic argument covers all three drones, so the subsequent direct P31 search was stopped. The separate full-model deadlock check P45 returned `MAY NOT`. These records are retained alongside the positive P06 verdict. [Follow-up checks](../analysis/heartbeat_followup.json)

## 为什么待发心跳不能无限等待 / Why a pending heartbeat cannot wait indefinitely

1. **等待期间，空闲链路不能消耗时间。** 对原调度，目标心跳在 Pending 且链路为 Idle 时，`heartbeat_tx[i]` 的同步可用且是 urgent。验证器允许先选另一个可用的离散动作，但不能在这种空闲状态中让时间流逝。每次入网重置链路时钟，Transmitting 的上界为 3，Delivered 为 committed 且直接回到 Idle。P06 排除在途包永久阻塞。
2. **任务和命令包至多 60 个。** 每架最多发送 1 个任务数量包、3 对请求和任务项，以及 1 个任务 ACK，共 24 个任务包。每架至多发起一次 ARM 和一次 START，每条命令最多初发加重传共 3 次，因此至多 18 个命令请求。每个请求至多产生一条接受或拒绝回复，再计 18 个。三个数字相加得到 60。
3. **其他心跳无法填满所有时间。** 设目标已等待 T 个模型时间单位。其余两架各自相邻心跳准入至少间隔 20，因此每架在这段时间最多准入 `1 + T/20` 个心跳包。把进入 Pending 时可能已在途的一包计作例外，每包按最久 3 个时间单位估计，得到 `T ≤ 3 × (1 + 60 + 2 × (1 + T/20)) = 189 + 0.3T`，即 `T ≤ 270`。

1. **An idle link cannot consume time while the target waits.** In the original model, `heartbeat_tx[i]` is enabled and urgent when the target is Pending and the link is Idle. Other enabled discrete actions may be taken first. Time cannot elapse in that idle state. Each admission resets the link clock, Transmitting is bounded by 3, and the committed Delivered location immediately returns to Idle. P06 rules out a permanently blocked packet.
2. **The fleet admits at most 60 mission and command packets.** Each drone has at most one count packet, three request/item pairs and one mission ACK, giving 24 mission packets. Each drone can be issued ARM and START once. With one initial attempt and up to two retries per command, at most 18 command requests are admitted. Each request produces at most one acceptance or denial, giving at most 18 replies.
3. **Other heartbeats cannot occupy the link indefinitely.** If the target has waited T model units, each of the other two senders can admit at most `1 + T/20` heartbeats during that time, because its admissions are at least 20 units apart. Allow one packet already in flight when Pending began. Counting up to three units of service per packet gives `T ≤ 3 × (1 + 60 + 2 × (1 + T/20)) = 189 + 0.3T`, hence `T ≤ 270`.

有限时间内无法靠无限离散步绕开这个上界：新入网包在释放链路前至少传输 1 个时间单位。网络交付与返回、任务启动、命令分派、重试计数和心跳进入 Pending 等边，在相邻的入网之间只能执行有限次。目标仍待发时，若链路空闲则存在下一步心跳同步，若链路忙则 P06 保证最终释放。因此任何最大执行都需要在上述有限时间内让该目标心跳入网。270 是推导出的保守上界，实际最长等待可能更短。 [UPPAAL 紧急通道语义](https://docs.uppaal.org/language-reference/system-description/semantics/)

An infinite sequence of discrete steps cannot evade this bound in finite time. Every newly admitted packet takes at least one unit of service before releasing the link. Delivery and return, upload startup, command dispatch, retry-counter updates and transitions into Pending can occur only finitely many times between admissions. With the target still waiting, an idle link has an enabled heartbeat admission and P06 ensures a busy link eventually becomes idle. Every maximal execution therefore admits the target within the derived finite bound. The analytical bound of 270 may exceed the longest reachable wait. [UPPAAL urgent channel semantics](https://docs.uppaal.org/language-reference/system-description/semantics/)

## 复现机器检查 / Reproduce the machine checks

设置 `UPPAAL_VERIFYTA` 后从本实验目录执行。 / Set `UPPAAL_VERIFYTA` and run from the E06 directory.

```powershell
python code/run_coordination_experiments.py --suite E06 --scheduler original --drones 3 --state-representation 3 --properties P06 P46 --limit 120
```
