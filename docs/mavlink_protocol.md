# 3 MAVLink protocol

---

## 3a_mavlink_protocol_base.xml

The model simulates 3 drones and a GCS. All communication passes through a single mocked "Network" automaton than handles only one message at a time with a transmission latency of exactly:
```c
const int LINK_DELAY = 2;
```

In "LOSSY" mode, it can also drop messages belonging to the command protocol. No other automaton communicates directly with any other; the flow is always: `GCS -> *_tx -> Network -> *_rx -> drone`.

GCS uploads a 3-item mission to each drone (using the mission protocol inherited from version 02),
then sends an "ARM" command to all of them,
followed by a "START" command (using the MAVLink command protocol).

Each command must be acknowledged via `COMMAND_ACK`; if an acknowledgment fails to arrive, the GCS retries before eventually aborting the process.

## Conventions

```c
const int N = 3; //<< Drones
```
```c
const int MISSION_SIZE = 3; //<< Mission items
```
```c
const int LINK_DELAY = 2; //<< Link delay
```

`X_tx` = sender to network
`X_rx` = network to receiver
`*_tx` = declared as `urgent chan` -> synchronization occurs as soon as both parties are ready, though time may elapse while the network is busy.
An `urgent location` would prevent this and trigger a timelock.

---

## Changes from 01 and 02

01 is a skeleton: the network only carries the count and the item request, the MissionReceiver never receives the items, so the MissionSender stays stuck in SendItem. The supervisor has no end state.

02 completes the mission transfer. The network bug on the item edge is fixed here (`sequence = 0` -> `sequence = s`, it delivered item 0 forever) and the supervisor gains Prepared.
Query 2 in 02 is broken: the `HaveCount` location was renamed to `RequestedItem` without updating the query. Fixed in 03a.

03a keeps the 02 mission logic unchanged and adds the MAVLink command protocol on top of it:

- the network now carries 7 message kinds: the 4 mission ones (count, request, item, mission ack) plus COMMAND, COMMAND_ACK (accepted) and COMMAND_ACK (denied)
- LOSSY drops command-protocol messages only, mission messages are never lost
- MissionReceiver sets `missionInstalled[id] = true` when it sends the mission ACK
- two new templates: CommandClient (GCS side) and CommandServer (drone side)
- the supervisor gains the command phase: Arming, Starting, Done, Aborted

## Global declarations

```c
const bool LOSSY = false; //<< true = the network may drop any command-protocol message
const int NB_CMD = 2;
const int ARM = 0;
const int START = 1;
const int ACK_TIMEOUT = (2*N+1)*LINK_DELAY; //<< 14, worst-case ACK wait is 2*N*LINK_DELAY = 12 (measured with the sup query)
const int MAX_RETRY = 2; //<< re-sends after the first try, 3 tries in total
```

`hurry` is an `urgent broadcast chan` with no receiver. As long as a `hurry!` transition is enabled, time cannot pass, so the supervisor is forced to move on as soon as its guard is true. Without it the GCS could wait forever in Prepared and the liveness queries (12) would fail.

Two separate truths are kept:

- what the GCS believes: `uploadDone`, `cmdAccepted`, `cmdDenied`, `cmdFailed`, set by the GCS-side templates
- what is true on the drone: `missionInstalled`, `armed`, `started`, set by the drone-side templates

This split is what the safety queries check.

## Templates

### GCSSupervisor

8 locations, two phases.

Mission phase, unchanged from 02: `Idle -> DispatchUploads -> Uploading -> Prepared`, waiting for `forall uploadDone[i]`.

Command phase: `Prepared ->(hurry!)-> Arming`, loops `begin_command[i][ARM]!` for every drone, then:

- `forall cmdAccepted[i][ARM]` -> Starting
- `exists cmdDenied[i][ARM] || cmdFailed[i][ARM]` -> Aborted

Starting works the same way with START, ending in Done if every drone accepted, in Aborted otherwise.

### Network

This is the mocked network. Two locations: Idle and Delivering (invariant `t <= LINK_DELAY`). For each of the 7 message kinds there is one edge into Delivering that stores the message (`drone_Peer`, `sequence` or `command`, `messageKind`, `t = 0`) and one delivery edge back to Idle, guarded `t >= LINK_DELAY`. Three loss loops, guarded by LOSSY, consume a command message without delivering it.

### MissionReceiver / MissionSender

Unchanged from 02, except the `missionInstalled` line on the receiver.

Receiver: `WaitCount -> RequestedItem -> WaitItem`, loops over the items one by one; on the last item -> `AckPending ->` sends `ack_tx` and sets `missionInstalled[id] = true` -> `Uploaded`.

Sender: `Idle ->(begin_upload)-> Announce (count_tx!) -> WaitRequest`; for every `request_rx` -> `SendItem -> item_tx`; on the mission ack sets `uploadDone[id] = true` -> `Done`.

### CommandClient (GCS side)

`Idle ->(begin_command[id][c]?)-> Sending -> cmd_tx[id][current]!` with `x = 0` -> `WaitAck`, invariant `x <= ACK_TIMEOUT`. Three ways out:

1. `accepted_rx[id][current]?` -> Idle, `cmdAccepted = true`
2. `denied_rx[id][current]?` -> Idle, `cmdDenied = true`
3. `x >= ACK_TIMEOUT`: `retries < MAX_RETRY` -> Sending (re-send), else -> Failed, `cmdFailed = true`

The self-loops absorb late or unrelated ACKs so the network never stays blocked on one:

- Idle: ACK for a command already answered
- Sending: ACK of the current command arriving early
- WaitAck with `c != current`: ACK of the other command
- Failed: late ACK arriving after the client gave up

### CommandServer (drone side)

`Idle ->(cmd_rx[id][c]?)-> Decide`, guarded by `canExecute(c)`:

- ARM is accepted iff `missionInstalled[id]`, START iff `armed[id]`
- accepted: `accepted_tx` + `execute(c)` -> `armed[id] = true` or `started[id] = true`
- refused: `denied_tx`

Self-loop "duplicate: ignored": a second COMMAND received while the answer to the first one is still in flight is ignored, the answer already on its way covers it. This is what makes the server idempotent.

## System

```c
system Supervisor, Sender0, Sender1, Sender2, Drone0, Drone1, Drone2, Link,
       CommandClient, CommandServer;
```

Writing the template name alone instantiates one copy per drone_id, which is why the queries can use `CommandClient(0)`.

## Queries (verified with verifyta 5.0.0, 21.11.2026)

| # | Query | LOSSY = false | LOSSY = true |
|---|---|---|---|
| 1 | SendItem imply WaitItem | satisfied | satisfied |
| 2 | RequestedItem imply expectedCount == MISSION_SIZE | satisfied | satisfied |
| 3 | E<> all 3 SendItem at once | satisfied | satisfied |
| 4 | E<> Prepared | satisfied | satisfied |
| 5 | E<> Done | satisfied | satisfied |
| 6 | E<> Aborted | NOT satisfied | satisfied |
| 7 | deadlock imply (Done or Aborted) | satisfied | satisfied |
| 8 | armed[i] imply missionInstalled[i] | satisfied | satisfied |
| 9 | started[i] imply armed[i] | satisfied | satisfied |
| 10 | Done imply forall started[i] | satisfied | satisfied |
| 11 | WaitAck --> (Idle or Failed) | satisfied | satisfied |
| 12 | Prepared --> (Done or Aborted) | satisfied | satisfied |
| 13 | armed[0] --> cmdAccepted[0][ARM] | satisfied | NOT satisfied |
| 14 | E<> Failed | NOT satisfied | satisfied |
| 15 | never cmdAccepted and cmdFailed together | satisfied | satisfied |
| 16 | E<> (cmdFailed[0][ARM] && armed[0]) | NOT satisfied | satisfied |
| 17 | sup of the ACK wait | 12 | 14 |

The two NOT satisfied with LOSSY = false are by construction: without loss nothing is ever denied or failed, so Aborted and Failed are unreachable.

Query 13 fails with LOSSY = true because all ACKs can be lost, the GCS then never learns the drone is armed. This is a real limit of the protocol, not a model bug.

Query 17 measures the worst-case ACK wait and is what ACK_TIMEOUT is calibrated on.

## Open points

- the network model (one message in flight, fixed delay, unbounded loss on 3 message kinds) is the part that will be replaced by the bounded queue. After that, ACK_TIMEOUT has to be re-measured with query 17 and all queries re-run
- heartbeat is not modeled yet: a periodic message is not compatible with a blocking link, it would cause a timelock. It has to wait for the new network

---

Léo QUINZLER - Gabriel LARGE
