# E06 ACK 优先调度 / ACK-priority scheduling

三机开启心跳时，ACK 优先排除了 E05 中的确认失败和超时重试（P35、P36），使命令准入后等待 ACK 的时间上界为 6 个模型时间单位（P37）。三个待发心跳分别都能获得发送机会（P30–P32）。 [调度对照](results/figs/E06_outcomes.png)

With three drones and active heartbeat, ACK priority excluded the confirmation failure and timeout retries observed in E05 (P35, P36). It bounded the post-admission ACK wait at six model time units (P37). Every pending heartbeat eventually gained admission (P30–P32). [Scheduling comparison](results/figs/E06_outcomes.png)

| 三机结果 / Three-drone result | 原调度 / Original | ACK 优先 / ACK priority |
|---|---|---|
| 任一确认失败 / Any confirmation failure | 可达 / Reachable | 不可达 / Unreachable |
| 回复等待 ≤6 / Reply wait ≤6 | 不成立 / Fails | 成立 / Holds |
| 每架待发心跳最终准入 / Eventual admission of each pending heartbeat | 本组查询未确定 / Inconclusive | 成立 / Holds |
| Prepared 后必到 Done / Prepared leads to Done | 不成立 / Fails | 成立 / Holds |

命令包送达后，待发 ACK 获得下一个链路时隙。命令和回复各最多传输 3 个单位，P38 的精确见证达到 6。原调度的 START0 失败见证中，同一计时起点下客户端于 t=42 失败，此时回复仍在途。 [两条轨迹对照](results/figs/E06_reply_comparison.png)

When a command arrives, its pending ACK gets the next link slot. The command and reply each take at most three units, and the exact P38 witness attains six. In the original-scheduling START0 witness, the client failed 42 units after its initial admission while the reply was still in transit. [Witness comparison](results/figs/E06_reply_comparison.png)

三机 Prepared → Done 由两项验证共同建立。完整模型验证 Prepared 时上传已经完成、命令尚未启动。后续模型覆盖 Prepared 时任意心跳相位、待发心跳及一条可能在途的心跳，精确验证 A<> Done 通过。两项检查分别耗时约 8.36 和 2.89 秒。直接验证完整模型的长时运行在约 814 秒主动停止，当时尚无判定。 [状态覆盖证明](results/proof/Prepared_to_Done.md)

The three-drone Prepared-to-Done claim follows from two checks. The full model verifies that mission upload is complete and commands have yet to begin at Prepared. The continuation model covers arbitrary heartbeat phases, pending heartbeats and a possible heartbeat already in flight. Its exact A<> Done check passed. The checks took about 8.36 and 2.89 seconds. The extended direct check of the full model was stopped at about 814 seconds before issuing a verdict. [State-coverage proof](results/proof/Prepared_to_Done.md)

这项结果把准入后的回复时限和整段命令流程的完成性连接起来。保证适用于当前三机、心跳周期 20、无丢包配置，Done 表示地面站已收到全队 START 接受确认。 [实际改进模型](code/models/09_ack_priority.xml)

The result establishes both a post-admission reply bound and completion of the command phase. It applies to the tested three-drone configuration with heartbeat period 20 and no packet loss. Done records receipt of every drone's START acceptance by the ground station. [Improved model](code/models/09_ack_priority.xml)
