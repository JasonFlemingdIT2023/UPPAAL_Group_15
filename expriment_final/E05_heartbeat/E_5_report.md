# E05 心跳流量 / Heartbeat traffic

开启心跳后，三机原调度在无丢包条件下出现确认失败见证，同时成功仍可达。单机和双机开启心跳时，P08 排除了无人机 0 的确认失败。

With heartbeat enabled, original scheduling admitted a three-drone confirmation failure on a reliable link. Success also remained reachable. For one and two drones with heartbeat, P08 excluded confirmation failure for drone 0.

## 设计与配对结果 / Design and paired results

对 N=1、2、3 使用同一个 08 源模型，通过系统组合启用或停用心跳发送和接收进程。每对固定传输时间 1–3、ACK 超时 14、最多重传两次和无丢包链路。周期为 20，从上次心跳获得链路时隙开始计时。除 P01、P03 和 P08 外，P24 检查地面站能否至少收到每架无人机的一次心跳。

For N=1, 2 and 3, we paired models built from the same version 08 source by enabling or disabling heartbeat sender and receiver processes. Service times of 1–3, ACK timeout 14, up to two retransmissions, and no packet loss were fixed. The period is 20 and restarts at each heartbeat admission. In addition to P01, P03 and P08, P24 checks whether a state exists in which at least one heartbeat from every drone has been received.

![心跳开关与验证成本 / Heartbeat activation and verification cost](results/figs/E05_activation.png)

## 失败见证 / Failure witness

三机见证中，START0 在 t=110 入网，t=113 送达。心跳、其他命令和重传占用后续链路时隙。t=150，ACK0 获得发送机会，服务端执行 START。t=152，客户端进入 Failed，ACK0 仍在传输，主管仍位于 Starting。 [原始轨迹事件](results/analysis/traffic_traces.md)

In the three-drone witness, START0 entered the link at t=110 and arrived at t=113. Heartbeats, other commands and retransmissions took subsequent link slots. At t=150, ACK0 gained admission and the server executed START. At t=152, the client entered Failed while ACK0 was still in transit and the supervisor was in Starting. [Trace events](results/analysis/traffic_traces.md)

![心跳竞争导致确认失败 / Confirmation failure under heartbeat contention](results/figs/E05_failure_timeline.png)

## 验证成本与参数对照 / Verification cost and parameter controls

N=2 的 P03 探索状态由 576 增至 53,314，约为原来的 92.6 倍。心跳周期从 20 改为 40 后增加到 124,082，首次错开后为 49,460，但错开后的存储状态由 24,687 增至 26,697。周期和释放相位改变了符号状态的时间交错，三个设置的查询真值一致。首次错开仅移动第一轮发送条件，之后各发送者仍按自身准入时间重新计时。

For N=2, P03 explored 53,314 states with heartbeat, about 92.6 times the 576 states with heartbeat disabled. Period 40 increased this to 124,082. Staggered first releases gave 49,460 explored states, with stored states increasing from 24,687 to 26,697. Period and release phase changed symbolic timing interleavings while query verdicts agreed across all three settings. Staggering changes the first release only. Each sender subsequently restarts its timer at its own admission.

![心跳周期和首次释放偏移对照 / Heartbeat period and first-release offset](results/figs/E05_settings.png)

E05 的三机心跳开启 BFS 有三条超时，DFS 随后给出 P01 和 P08 的具体见证。P03 的 DFS 仍超时，E06 在相同原调度模型上用保守过近似证明了 P03。 [E05 原始记录](results/records.csv) · [E06 对照结果](../E06_ack_priority/results/analysis/original_overapprox_records.json)

The three-drone BFS with heartbeat had three timeouts. DFS then found witnesses for P01 and P08. DFS also timed out on P03. E06 subsequently proved P03 using conservative over-approximation on the same original-scheduling model. [E05 records](results/records.csv) · [E06 control result](../E06_ack_priority/results/analysis/original_overapprox_records.json)

因此，E05 有四次单次运行超时，但三机心跳开启的三个相关问题都有后续结论：成功可达、确认失败可达、START 前置条件成立。原 BFS 超时仍保留在成本图中，因为它描述该次搜索的资源开销。

E05 therefore contains four timed-out invocations, while all three associated questions for the heartbeat-active three-drone model have follow-up answers. Success and confirmation failure are reachable, and START requires ARM. The BFS timeouts remain marked in the cost figure because they record the resource budget of those searches.
