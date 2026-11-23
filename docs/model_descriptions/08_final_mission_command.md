# 08 — Main mission and command model

Contributor: Jason

Scope of contribution: final integration, configuration selection and delayed-ACK handling. The model retains the teams command protocol and adapts the standalone network design.

Model: [08_final_version.xml](../../models/08_final_version.xml). Status: final candidate for team verification and experiments, not a declaration that all properties have passed.

## Scope and architecture

One GCS coordinates three drones through a single shared PacketNetwork. GCSSupervisor activates MissionSender sessions, waits for all upload confirmations, requests ARM, waits for all ARM acceptances, requests START, then records Done or Aborted. MissionReceiver and CommandServer are separate components of each drone. Command templates are instantiated automatically for bounded drone IDs.

Heartbeat templates and declarations remain for reference, but HBSender and ConnectionMonitor are excluded from the system composition. See [the heartbeat ablation](07_heartbeat_experiments_and_ablation.md).

## Purpose and changes

After the adapter experiment and the finite-preparation heartbeat trial, the main model keeps the simpler direct packet network and disables recurring heartbeat processes to make the selected coordination questions more tractable. It also fixes useful acknowledgements being discarded while a retry is waiting. 

## Complete workflow

1. Supervisor activates each mission sender. The corresponding receiver requests the three items in order.
2. Final mission acceptance crosses the network. Each sender sets uploadDone. The supervisor barrier requires every flag.
3. The supervisor activates ARM clients. Each server checks its local prerequisite, applies the abstract operation on acceptance handover and returns accepted/denied.
4. Clients record the delivered result or retry after a timeout. A denial or exhausted attempts takes the supervisor to Aborted.
5. After every ARM acceptance is received, START exchanges follow the same pattern. Every START acceptance received permits Done.

The supervisor sees client outcomes, not private network loss decisions. Local drone state and the GCSs knowledge are distinct.

## Mission transfer

Each fixed three-item mission follows count, request(seq), item(seq), repeated requests/items, and final mission acceptance. Receiver nextSequence and receivedCount track order and completeness. missionInstalled is drone-local evidence. uploadDone becomes true only after final acceptance reaches the GCS. 

## Command coordination and delayed-ACK handling

Each client handles one ARM and one START operation, with current command, retry counter and a timeout clock. Sending hands a command directly to the link and resets the clock. WaitAck records acceptance or denial, retries on timeout if attempts remain, or records cmdFailed after exhaustion. MAX_RETRY = 2 means three attempts.

A delayed accepted/denied acknowledgement for current can complete the exchange through Sending -> Idle. The self-loops discard only other commands (c != curren). Previously useful replies could be discarded while a retry was waiting. This avoids unnecessary retransmission without adding a clock or location. Idle, Failed and wrong-command receiving loops preserve the ability to consume obsolete replies. Repeated separate operations of the same command type are not modelled.

The server permits ARM when missionInstalled and START when armed. These are selected application rules, not universal MAVLink requirements. Accepted operations have instantaneous abstract effects when the server hands the reply to the network. They do not model flight dynamics or a complete autopilot.

## Network and outcomes

The link stores one packet privately and services it within D_MIN..D_MAX. Delivered and Lost are committed outcomes. With LOSSY = false, transmission is reliable. wth true, command requests and accepted/denied command replies can be lost after occupying the slot. Mission messages remain reliable. There is no queue, FIFO, explicit fairness, corruption or duplication.

Done means all START acceptances reached the GCS, not flight completion. Aborted means coordination stopped, not fleet cancellation or disarming. cmdFailed means confirmation was not obtained within the attempts, not that the drone did nothing. Lost acknowledgements can leave armed/started true despite client failure.

## Key parameters and state

| Name | Meaning |
|---|---|
| `N = 3`, `MISSION_SIZE = 3` | Fleet size and symbolic mission length |
| `D_MIN = 1`, `D_MAX = 3` | Service duration after network admission |
| `ACK_TIMEOUT = 14`, `MAX_RETRY = 2` | Reply timeout and at most two retransmissions |
| `LOSSY` | Optional loss of command-protocol traffic only |
| `cmdAccepted`, `cmdDenied`, `cmdFailed` | Recorded client outcomes, indexed by drone and command |
| `missionInstalled`, `armed`, `started` | Abstract local drone state |
| `armSent`, `startSent` | Supervisor activated a client, not proof of drone reception |

Time values are model units until a consistent physical interpretation is chosen. Timers reset on network admission in this direct integration. Packet loss and service order are nondeterministic; no probabilities or fairness are implied.


