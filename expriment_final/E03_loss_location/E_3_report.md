# E03 丢包位置 / Loss location

相同的确认失败可以发生在 ARM 已执行或尚未执行时。区分这两种情况需要结合地面站的确认状态、无人机状态和在途消息。 [四种模式的查询结果](results/figs/E03_outcomes.png)

The same confirmation failure can occur with ARM already executed or still unexecuted. Distinguishing the cases requires the ground station's confirmation state, the drone state and messages still in transit. [Query outcomes across four loss modes](results/figs/E03_outcomes.png)

| 查询 / Query | 可靠 / Reliable | 只丢请求 / Request only | 只丢 ACK / ACK only | 两种均可丢 / Either |
|---|---|---|---|---|
| P01 成功可达 / Success reachable | 是 / Yes | 是 / Yes | 是 / Yes | 是 / Yes |
| P08 确认失败可达 / Failure reachable | 否 / No | 是 / Yes | 是 / Yes | 是 / Yes |
| P10 失败时已 ARM / Armed at failure | 否 / No | 是 / Yes | 是 / Yes | 是 / Yes |
| P11 失败时未 ARM / Unarmed at failure | 否 / No | 是 / Yes | 是 / Yes | 是 / Yes |
| P18 中止并处理完毕后仍未 ARM / Settled abort while unarmed | 否 / No | 是 / Yes | 否 / No | 是 / Yes |

只丢请求的 P18 见证中，三次 ARM 请求全部丢失，t=42 协调中止，链路和服务端均空闲，且无人机 0 未 ARM。只丢 ACK 的 P10 见证中，ARM 执行后 ACK 丢失，t=42 同样出现确认失败，但无人机已经 ARM。两条时间线均以首个 ARM 请求准入为起点。 [逐事件轨迹](results/analysis/trace_events.md)

In the request-only P18 witness, all three ARM requests were lost. At t=42 coordination aborted, the link and servers were idle, and drone 0 was unarmed. In the ACK-only P10 witness, ACKs were lost after ARM execution. The client again failed at t=42, with the drone armed. Both timelines begin at the first ARM request admission. [Trace events](results/analysis/trace_events.md)

只丢 ACK 时 P11 可达且 P22 成立。也就是说，失败瞬间还未 ARM 的执行随后仍会 ARM。服务端可以已收到请求，等待回复获得链路时才执行 ARM。只丢请求与两种包均可丢时，P22 均不成立。可靠对照中 P22 的前提不可达。 [P22 公式和记录](code/queries/README.md#p22)

With ACK loss only, P11 was reachable and P22 held. Executions that were still unarmed at failure subsequently reached ARM. The server can receive the request and wait to execute ARM until its reply enters the link. P22 failed when requests could be lost. Its premise was unreachable in the reliable control. [P22 formula and evidence](code/queries/README.md#p22)
