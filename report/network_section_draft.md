## Network model (working draft)

I started with a network that handles one packet at a time. A producer offers a packet, and the network accepts it when the slot is free. The network keeps its own copy of the source, destination, message kind and a small payload, then either delivers or loses the packet. In the first test, delivery or loss happens between one and three time units after admission. I used 100 ms per unit as an example, not as a measured network delay. A packet may also wait before the network accepts it, and that waiting is not part of the one to three units.

The network has four locations: `Idle`, `Transmitting`, `Delivered` and `Lost`. The clock is reset when a packet is accepted. While the packet is in `Transmitting`, the invariant stops the clock from going past the maximum delay, and delivery or loss can happen once the minimum delay is reached. After either outcome, the slot becomes free again. The sender is never told about a loss. In the full system it would have to notice through its own timeout.

The group's `03a` model already has a shared network for mission and command messages. It uses a fixed delay of two time units and, in its lossy setting, can drop command messages as soon as they are sent. My network is a separate test with a delay range and different loss settings. It still needs an adapter for the group's `_tx` and `_rx` channels, and we need to agree which messages can be lost before putting it together with the other components. The results below come from the standalone test, not from the combined model.

For the test, two producers share the slot and send two packets each in opposite directions. Each can hold one packet while it waits, there is no shared queue yet. The receiver stubs are always ready and check the packet fields. Using UPPAAL 5.0.0, I ran 18 queries in four settings:

The table comes from the earlier model copies saved with the results. The current file has updated comments, while its declarations, transitions and queries are the same. A rerun of the edited file is still needed because the last attempt could not retrieve the UPPAAL license.

| Setting | Loss reachable | All 4 packets lost reachable | Longest admission wait, producer 1 |
|---|---|---|---:|
| Reliable, max. delay 3 | no | no | 9 |
| Unrestricted loss, max. delay 3 | yes | yes | 9 |
| Bounded loss (1 in a row), max. delay 3 | yes | no | 9 |
| Reliable, max. delay 5 | no | no | 15 |

In all four settings the checks for integrity, packet accounting, the service interval and the packet leaving the slot passed, and the only deadlock was the normal end of the test. Loss was reachable in both loss settings and not in the reliable ones. With unrestricted loss there was a run where all four packets were lost. That run was not possible with the test's limit of one consecutive loss per fixed flow. The loss choices are nondeterministic, so they don't stand for a measured probability.

The last column shows that the producers can get in each other's way. Producer 1's second packet can wait behind its own first packet and both of producer 0's packets, so the longest wait before admission was 9 time units when the maximum service time was 3, and 15 when it was 5. This result depends on the four-packet workload and on how the test producers offer packets. It is not an end-to-end command bound. After integration, the command timeout will need to be measured again and the group queries rerun. Heartbeat is not part of the current group model yet.

Contribution (draft): Network modeling: standalone shared-link model and test harness, queries and verification runs for delivery, loss and timing, a script to repeat the runs, and notes for integration. The model and draft were developed with AI assistance (see the AI usage log). The results and integration still need to be reviewed with the group.
