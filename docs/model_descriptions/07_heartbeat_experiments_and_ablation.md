# 07 — Heartbeat stopping experiment and ablation

Contributor: Jason

Models: [04](../../models/04_heartbeat_protocol_v1.xml), [06B](../../models/06B_simple_integration.xml), [07_heartbeat_drop_after_done.xml](../../models/07_heartbeat_drop_after_done.xml), and [08](../../models/08_final_version.xml).

## Purpose and changes

Version 06B simplified the network, but retained recurring heartbeat traffic. Version 07 tests whether ending generation after the preparation outcome reduces unnecessary subsequent behaviour. 

SPOILER: it does not. 

The selected main configuration then removes active heartbeat processes rather than adding a new abstract monitor. 

## Observation

The reported observation was that the same check completed quickly without heartbeat activity but took much longer with it. Exact queries, tool settings, state counts and time limits must accompany a reproducible comparison. A cancelled search is not conclusive, not a false property.

## Version 07: stopping generation

Version 07 adds preparationFinished, set on terminal supervisor outcomes, and a Stopped location to HBSender. A sender in Waiting can stop using an urgent broadcast. Generation is guarded by !preparationFinished. A pending heartbeat still enters the network before the sender stops. in-flight traffic can drain. The network and monitors continue accepting those deliveries.

This ends the modelled preparation observation period; it does not assert real drones stop reporting after START. It also does not necessarily accelerate E<> Supervisor.Done, which can terminate as soon as a witness reaches Done. Much exploration can occur before completion.

## Sender workflow

| Sender state when preparation finishes | Behaviour |
|---|---|
| Waiting | Urgent `stopHeartbeat!` transition enters Stopped |
| Pending | Last `heartbeat_tx[id]!` handover enters Stopped |
| Heartbeat already transmitting | Network and monitor finish delivery normally |


## Final scope decision

Version 08 omits HBSender and ConnectionMonitor from system composition. Their definitions remain in the file but are inactive. No abstract connection monitor was implemented as a replacement in the main model. The main model therefore makes no heartbeat freshness or connection-loss detection claim.

Strictly, removing heartbeat is the ablation relative to a heartbeat-enabled system.

