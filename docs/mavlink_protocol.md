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
