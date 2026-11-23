# 04 — Explicit heartbeat communication

Contributor: Jason

Model: [04_heartbeat_protocol_v1.xml](../../models/04_heartbeat_protocol_v1.xml).

## Purpose and changes

Version 03 supplied mission uploads followed by ARM and START command exchanges. This version adds HBSender(id) and ConnectionMonitor(id) so recurring presence messages compete for the same single-slot network. These are concurrent processes, not a new sequential supervisor stages.

## How it works

Each sender has a period clock. Waiting has the invariant period <= HB_PERIOD. At the period boundary it enters Pending. It hands a heartbeat to the network when admission is available, then resets period and then starts waiting again. Pending is ordinary so a busy network can finish transmitting.  Each drone has its own sender. Their first periods initially happen together which could also cause delay in the network regarding command messages. The decision is still non-deterministic.

HB_PERIOD = 20 means model time units, not automatically seconds. A physical interpretation must be agreed for the complete model. Delivery uses heartbeat_rx. Network message kind 7 identifies the heartbeat.

The monitor starts in Unknown, then enters Tracking on reception. It sets heartbeatSeen[id] and resets its age clock on every reception. Tracking means at least one heartbeat was received, not that communication remains fresh. There is no stale-state detection, disconnection response or supervisor freshness guard in this version.

## Example and key state

| Name | Meaning |
|---|---|
| `period` | Time since the last heartbeat handover |
| `age` | Time since the last reception after entering Tracking |
| `heartbeatSeen[id]` | Historical reception flag; not current connectivity |
| `HB_PERIOD` | Source period in the model's chosen unit |

## Findings and next step

Explicit recurring traffic adds independent clock relationships, pending states and transmission requests. A long propertyfailure search was observed. Screenshots are saved under `results/Pictures/04_state_overload_heartbeat_model*.png`. This is a verification-cost observation, not evidence that heartbeat communication is unsuitable or that the queried failure is reachable. See [the event log](../events_and_bugs.md) and [the later ablation analysis](07_heartbeat_experiments_and_ablation.md).

[Versions 05–06B](05_06_network_integration.md) retain these processes while investigating an alternative packet network. [Version 07](07_heartbeat_experiments_and_ablation.md) then investigates the ongoing traffic cost.
