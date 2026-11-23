# Network interface (working version)

This is a separate network test. It does not replace the network in `03a_mavlink_protocol_base.xml` yet. The names here are provisional, and we still need to agree on the interface with the rest of the group.

## How a packet moves

1. A producer fills its own `outgoing[p]` record and leaves it unchanged while it waits in `Waiting`.
2. It offers `net_tx[p]!`. The network takes it with `net_tx[p]?` when the slot is free, copies the record into its own `packet` and resets `x`.
3. After at least `D_MIN`, the network either delivers the packet or, if the loss mode allows it, loses it. By `D_MAX` one of the two has to happen.
4. For delivery, `net_rx[packet.dst]!` hands the packet to the receiver stub. The network writes `incoming` on the sending edge and the receiver reads it on the receiving edge. In UPPAAL the sender's updates run before the receiver's, so the receiver sees the new value. The receiver is always ready in this test.
5. The network passes through `Delivered` or `Lost` and goes back to `Idle`. Both locations are committed and their exits do not need any other process.

`net_tx` is an urgent channel. When the network is idle and a producer is waiting, time cannot pass until the network takes a packet. While the network is busy, a producer can wait and time passes. If both producers are waiting, the choice is nondeterministic. There is no FIFO or round-robin promise.

`Prepare` in the test producer is urgent only so the test makes its next packet straight away. The producer never waits for the network there, that happens in the normal `Waiting` location. Real producers will need their own rules for when they send.

## Packet fields and ownership

| Field | Meaning here |
|---|---|
| `src`, `dst` | Abstract endpoint numbers 0 and 1. The test uses both directions. |
| `kind` | Two abstract traffic classes, one per test producer. They do not stand for specific MAVLink messages yet. |
| `payload` | Small example value, used to check that the contents arrive unchanged. |
| `id` | Unique test packet ID for bookkeeping. It is not meant to be a MAVLink transaction ID. |

The producer owns its outgoing record until the network takes it. After that, the network owns its copy. The receiving side owns whatever happens after the handover. Status arrays, expected packets, counters and the receiver's integrity flag are only there for the test. A real sender never gets a loss notification from them. This network does not create ACKs, retry packets, or set drone/application state.

There is one service slot for both directions. Each producer can hold one test packet waiting outside it. This is backpressure, not a shared finite queue. The test producers never make a new packet while one is still waiting, so there is no rule yet for that case. Overflow, corruption, duplication and reordering of packets already in the link are not modeled. With only one slot, a packet in the link can never be overtaken by another one.

The time in the link is `D_MIN` to `D_MAX`, counted from when the network takes the packet. Waiting to get the slot is separate, and so is processing at the receiver. With the test values, one unit is 100 ms, `D_MIN = 1` and `D_MAX = 3`. These are examples, not measured radio times.

## Loss settings

- `LOSS_MODE = 0`: reliable link, the loss edge is never enabled.
- `LOSS_MODE = 1`: any packet in the link may be lost (nondeterministic choice, not a probability).
- `LOSS_MODE = 2`: at most `K_LOSS` packets in a row from the same test flow can be lost. Here a flow is a producer: each producer has a fixed source, destination and kind, so the producer index identifies that combination. A delivery resets only that producer's counter. If real producers send to several destinations or kinds, the counter has to be indexed differently before we can call it a per-flow bound.

A lost packet uses the same service interval as a delivered one and keeps the slot busy for that time. Loss bounds do not guarantee that a producer ever gets the slot. `K_LOSS = 1` is only an example.

## Fit with the existing team model

`03a_mavlink_protocol_base.xml` already has a `Network` template, instantiated as `Link`, with one shared slot and a fixed `LINK_DELAY = 2`. It uses the channels `count_tx/rx`, `request_tx/rx`, `item_tx/rx`, `ack_tx/rx`, `cmd_tx/rx`, `accepted_tx/rx` and `denied_tx/rx`. The packet information is carried by the channel indices and the network's `drone_Peer`, `sequence`, `command` and `messageKind`. When `LOSSY` is on, command traffic can be dropped as soon as it is sent (a self-loop on `Idle`, no time passes), and mission traffic is never lost. That is different from this test, where loss happens after a delay and applies to every class.

A possible adapter would map each existing `_tx` channel and its indices to a producer's staged record, then map the network's copy back to the matching `_rx` channel. It needs a separate staging place for each sender that can send at the same time. Before connecting it, we should agree which messages may be lost and whether a loss takes time. Not all of the existing receivers are ready for every message at every moment, so the adapter needs a rule for buffering, overflow or backpressure instead of relying on the test stub always being ready. The command client's `ACK_TIMEOUT` was set for the old network, so it has to be measured again and all team queries rerun after the link changes. Some names also clash: both files have a `Network` template and a `Link` instance, and `Sender0`/`Sender1` are mission senders in `03a` but test producers here. The test templates need renaming when they go into the combined file.

The project notes mention a future bounded queue and heartbeat support. Neither is in this model. Before building them we need to agree on queue size, what happens when the queue is full, scheduling, how heartbeats are produced and how late or unexpected messages are handled. This first component is a starting point for that discussion, not a finished queue or heartbeat model.
