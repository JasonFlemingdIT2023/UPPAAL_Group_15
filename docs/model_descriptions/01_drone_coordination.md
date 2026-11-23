# 01 — Initial drone coordination

Contributor: Jason

Model: [01_drone_coordination.xml](../../models/01_drone_coordination.xml)  
Status: first development and baseline for a supervisor as state maschine and a network between the procols.

## Purpose and changes

Establish one GCS, three drone sessions and an explicit shared network before adding the complete mission protocol. Separate templates let the same communication behaviour be instantiated for each drone without drawing implementations per drone. A supervisor coordinates the sessions not GCS for each drone

## Intended workflow

1. `GCSSupervisor` leaves Idle and activates each session through `begin_upload[id]`.
2. `MissionSender(id)` moves from Idle to Announce and hands over a mission count.
3. `Network` remembers the drone and message kind, resets `t`, and delivers after `LINK_DELAY = 2`.
4. `MissionReceiver(id)` records the announced mission length and requests the first item.
5. The network returns that request to the corresponding sender.

The supervisor uses a DispatchUploads self-loop for all but the last session, which increments nextDrone. The last activation leaves the loop without incrementing beyond the valid range. Activations are sequential, but activated sessions can run concurrently.

The network has Idle and Delivering. The invariant t <= LINK_DELAY and delivery guard t >= LINK_DELAY specify an exact service time, if the receiving edge is available. Other senders wait outside the link. No queue is modelled. _tx means handover into the network and _rx means delivery out of it. The internal begin_upload event does not use the radio link.

## Key state

| Name | Meaning |
|---|---|
| `N = 3` | Number of drone sessions |
| `MISSION_SIZE = 3` | Fixed number of symbolic items, independent of drone count |
| `id` | Fixed drone index for a template instance |
| `nextDrone` | Next session the supervisor activates |
| `expectedCount` | Receiver's announced mission length |
| `drone_Peer`, `messageKind`, `t` | Network's stored session, message type and service clock |

## Next step
Extend it with an mission protocol which does not onl;y provide the mission length, but also the items.
[Version 02](02_mission_protocol.md) completes the item loop, extends the networks message kinds and adds a supervisor completion barrier.
