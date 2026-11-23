# 02 — Extended mission upload

Contributor: Jason

Model: [02_drone_extended_missionProtocol.xml](../../models/02_drone_extended_missionProtocol.xml)  
Status: Mission extension for the baseline model and full Mission protocol workflow.

## Purpose and changes

Extend [version 01](01_drone_coordination.md) from the initial announcement/request exchange into a complete normal mission upload. Add symbolic item indices, repeated item requests and responses, final acceptance and a GCS that waits for every upload.

## Intended workflow

```text
Supervisor activates sender
GCS -> count -> drone
Drone -> request(0) -> GCS -> item(0) -> drone
Drone -> request(1) -> GCS -> item(1) -> drone
Drone -> request(2) -> GCS -> item(2) -> drone
Drone -> final ACK -> GCS
All uploadDone flags true -> supervisor Prepared
```

Every inter-device message passes through the single-slot network. Its message kinds distinguish count, request, item and final ACK. Acceptance stores the drone, relevant sequence and kind, then resets t. Delivery occurs after exactly two model time units. Its a design decision thast the network has only one slot which is nalso in favor of avoiding stae space explosion.

MissionSender follows Idle -> Announce -> WaitRequest. A request stores requested, leads to SendItem and then returns to WaitRequest after item handover. The final ACK instead leads to Done and sets uploadDone[id].

MissionReceiver follows WaitCount -> RequestedItem -> WaitItem. A non-final item increments receivedCount and nextSequence and returns to RequestedItem. The final item increments the count and leads to AckPending. Sending final acceptance leads to Uploaded. The receiver and GCS do not finish simultaneously: the ACK still needs network delivery before uploadDone changes.

## Key state and interfaces

| Name | Meaning |
|---|---|
| item_id | Bounded item index, 0 through MISSION_SIZE-1 |
| nextSequence | Item currently requested/expected by the receiver |
| receivedCount | Number of accepted items |
| requested | Item the sender must answer |
| sequence| Item index stored in the link |
| uploadDone[id] | Final acceptance received inside the GCS |

Request/item channels have drone and sequence indices. Count and final-ACK channels have only a drone index. Mission items are symbolic identities, not waypoint coordinates. No packet loss, retransmission or mission timeout is included.

## Saved bug and later development

The saved network request-acceptance edge assigns `sequence = 0` rather than `sequence = s`. After a request for item 1, the sender is told to resend item 0. The receiver expects item 1, so the link can block at its delivery deadline. See [events and bugs](../events_and_bugs.md).

Version 03 corrects the sequence handling and adds command coordination after mission transfer. See the [command description](03_mavlink_command_protocol.md).