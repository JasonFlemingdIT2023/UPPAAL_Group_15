# 05–06B — Network integration and simplification

Contributor: Jason

Builds on the standalone network component from Faissal and the existing team protocols.

## Models and development sequence

- [05_network_integration_part1.xml](../../models/05_network_integration_part1.xml): packet declarations and TxAdapter definition. The adapter is not in the system composition. The old network still runs.
- [06_network_integration_adapter_state_explosion.xml](../../models/06_network_integration_adapter_state_explosion.xml): active sending adapters, receiving adapters and packet network.
- [06B_simple_integration.xml](../../models/06B_simple_integration.xml): direct protocol-to-packet-network integration. Adapters and receive mailboxes removed, explicit heartbeat processes retained.

These files record design milestones, not three independently established correctness results.

## Source concept

The [standalone network description](STANDALONE_network_model.md) supplies the single shared service slot, private in-flight packet, bounded variable transmission duration and explicit delivery/loss outcomes. Its two test producers and always-ready receivers are not the applications GCS and drones. Its saved results do not prove the integrated system.

## Purpose and changes

Version 04 exposed both shared-link interference and expensive recurring traffic. The integration inckudes variable service duration and transmission-time-consuming loss from the standalone component while trying to preserve  the mission, command and heartbeat behaviours. Versions 05 and 06 first use an explicit translation layer. 06B removes its buffering complexity to tackle state space explosion.

## Packet interface and adapter attempt

The packet interface defines endpoint 0 for the GCS and endpoint id + 1 for a drone. packet_t stores source, destination, kind, drone session, mission sequence, mission count and command. Internal kind constants identify count, request, item, mission ACK, command, accepted ACK, denied ACK and heartbeat. They are not MAVLink numeric identifiers. This concept is oriented on Faissals standalone implementation.

TxAdapter(id, kind) translates an existing _tx event into a staged record. Its slot is kind * N + id, preventing different sources from overwriting each other. Ready accepts a protocol message. Pending waits for generic net_tx. With three drones and eight kinds there are 24 instances, not 24 separate template definitions.

RxAdapter(endpoint) copies generic incoming into a private mailbox and forwards it on the appropriate existing _rx channel. Occupancy is tracked by rxBusy. The adapter version can record overflowSeen when delivery encounters a full mailbox at the network deadline. Ordinary forwarding can be postponed, so overflow can show permissive scheduling as well as buffer pressure. Adapter admission also starts a clients existing timer before link admission.

## Reason for simplification

Independent staging slots, receive mailboxes, recurring traffic and variable timing introduced many additional state combinations. To reduce that cost and avoid defining a whole buffering architecture, version 06B retains the protocols original channel interfaces and puts packet construction directly on the network's acceptance edges. It was the goal to preserve as many concepts from faissals network part as possible.

storePacket fills one private in-flight record. The network has Idle, Transmitting, Delivered and Lost. Transmitting has t <= D_MAX. outcomes require t >= D_MIN. Delivered and Lost are committed and return to Idle without elapsed time. D_MIN = 1 and D_MAX = 3 replace the old exact duration of 2. Other senders wait outside the link. There is no shared queue, priority or general fairness guarantee.

Command traffic may be discarded after occupying the link when LOSSY is enabled. Mission and heartbeat traffic remain reliable. The standalone component's per-producer bounded-loss mode was not transferred. No adapters, overflow policy or generic net_tx/net_rx infrastructure remain active in 06B.

## Example: item delivery in 06B

For mission item 1 of drone 2, item_tx[2][1] lets the network store peer = 2, seq = 1, kind = PK_ITEM, src = 0 and dst = 3, and reset t. During Transmitting no other packet can enter. Between D_MIN and D_MAX, item_rx[2][1] synchronises with the receiver. The network passes through Delivered and frees the slot. Command and heartbeat packets follow the same service structure, using their own fields and channels. Loss is nondeterministic, not a measured probability.

| Change from the old network | Effect |
|---|---|
| Exact duration 2 -> interval 1..3 | Different permitted message timings |
| Separate message variables -> packet record | Explicit grouping and direction |
| Idle loss loops -> loss after admission | Lost command traffic still occupies the link |
| Direct channel delivery in 06B | No adapter admission wait or receive-mailbox policy |

## Limits and next step

Variable service duration supports latency-sensitivity experiments. Delayed loss accounts for resource consumption by unsuccessful transmissions. The record groups message information clearly. Delivery still uses the protocols peer/kind/sequence/command channels.

Physical radio contention, bandwidth, packet sizes, queues, corruption, duplication and parallel links are outside scope. The command timeout remains an experimental parameter, not a demonstrated end-to-end bound. Diagram rearrangements only changed coordinates and edge routes.

[Version 07](07_heartbeat_experiments_and_ablation.md) investigates heartbeat termination. [Version 08](08_final_mission_command.md) uses the simplified network without active heartbeat processes.
