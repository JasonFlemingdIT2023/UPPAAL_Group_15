# Architecture and modelling decisions
Jason  
23 November 2026  
Reference model: [08_final_version.xml](../models/08_final_version.xml)

## 1. Problem and real-life orientation

The system studies a GCS coordinating mission upload, ARM and START for several drones. The key distinction is between an operation occurring on a drone and the GCS obtaining confirmation of it. Shared communication, delay, timeout and missing replies can separate these facts.

The real-life grounding is selected MAVLink microservice exchanges, not an ISO architecture, a complete autopilot or a universal drone-show implementation. The following links are protocol sources, not proof that our abstraction conforms to every detail:

| Reference | Grounding in this model | Deliberate abstraction |
|---|---|---|
| [MAVLink mission protocol](https://mavlink.io/en/services/mission.html) | Count, item requests, indexed item responses, final acceptance | Fixed symbolic mission; no full waypoint fields or mission recovery |
| [MAVLink command protocol](https://mavlink.io/en/services/command.html) | Commands, matching acknowledgements and retry after missing replies | Two symbolic commands and accepted/denied outcomes; no long-running progress protocol |
| [MAVLink heartbeat protocol](https://mavlink.io/en/services/heartbeat.html) | Periodic presence reports in historical extensions | Packet-level heartbeat retained as an experiment; inactive in the main model |

ARM and START are internal identifiers. The intended concrete references are arming via `MAV_CMD_COMPONENT_ARM_DISARM` and mission start via `MAV_CMD_MISSION_START`, with the selected parameters abstracted away. This is a conceptual mapping, not an implemented encoding. Command acceptance is not general evidence of physical completion. Our immediate changes to armed/started are explicit application abstractions. Heartbeat presence alone does not establish mission validity or mission completion.

## 2. One GCS with concurrent sessions

The GCS comprises GCSSupervisor, MissionSender instances and CommandClient instances. A separate sender/client for each drone is a session inside one GCS, not another physical ground station. MissionReceiver and CommandServer with the same index belong to the same drone.

The supervisor enforces upload-all -> ARM-all -> START-all. This barrier policy is our application design, not a prescribed MAVLink fleet algorithm. Per-drone protocol exchanges overlap within a stage. Ordinary UPPAAL parallel composition implements this logical hierarchy without one huge automaton encoding every state combination.

Three drones and three mission items are separate size choices. Bounded types keep the state space finite. Scaling N requires updating explicitly named mission instances, not merely changing the constant. 

## 3. Internal events versus network messages

`begin_upload` and `begin_command` activate GCS workers locally. Inter-device messages use `_tx` for network admission and `_rx` for delivery. The network owns the packet between these events. The supervisor uses GCS outcome flags. It does not use a hidden loss notification or directly inspect the network to infer success.

## 4. Mission abstraction

Items are sequence identities, not full coordinates or flight paths. The receiver requests the next index, accepts that indexed item, increments receivedCount and acknowledges after all items. The sender records completion only after final acceptance reaches it. In later versions missionInstalled is set when the receiver hands its final acceptance to the network; it is not a detailed transactional-storage implementation.

Mission traffic is reliable. This isolates the command uncertainty questions without implementing mission timeout/retry and duplicate handling. It is not a claim that real mission messages cannot be lost. Historical snapshots 01 and 02 retain development errors, described in their documentation.

## 5. Commands, retries and acknowledgement policy

One command per client is outstanding. Each type is used once in the scenario. ARM requires the modelled mission to be installed. START requires armed. These are chosen local rules, not universal MAVLink command prerequisites. The command server applies an accepted effect when its acknowledgement is handed to the link, so local execution is coupled to reply admission. Physical execution time and subsequent flight are excluded.

A client resets its timer at command admission, retries after timeout up to MAX_RETRY and records failure when its attempt budget is exhausted. Failure means missing confirmation, not proof of non-execution. A matching late acknowledgement in Sending now completes the exchange. wrong-command replies are consumed and ignored. Receiving loops prevent irrelevant replies blocking the direct-delivery network. Repeated separate operations of the same command type and general transaction correlation remain outside scope.

Done means every START acceptance was received. Aborted means the supervisor stopped coordination. other already-issued exchanges can still finish. Neither outcome implements fleet-wide cancellation, disarming, landing or rollback. A failed/aborted run can leave drones armed or started.

## 6. Shared packet network

The network uses only one slot at a time which is a intended design decicion to prevent a higher risk of stae explosion.

The standalone component motivated a private packet record, a variable service window, and loss that consumes service time. The integrated model adapts those concepts rather than embedding the standalone test harness. Its finite-packet integrity results do not transfer automatically to the integrated application.

One service slot represents one effective shared resource for both directions. Waiting senders use backpressure. There is no central queue. Packet sizes, medium access, interference, bandwidth, multiple radios and simultaneous transmissions are abstracted away. This is adequate for studying resource contention; it is not a measured radio model or a claim that all drone deployments use one physical link.

Transmitting has `t <= D_MAX`; outcomes require `t >= D_MIN`. Delivered and Lost are committed outcome markers that release the slot without elapsed delay. With LOSSY enabled, only command requests and accepted/denied command acknowledgements can be lost. Unlike the old Idle loss loops, a lost transmission occupies the link. Loss is nondeterministic, with no probability or bound on consecutive losses. The standalone bounded-loss mode is not integrated.

Direct delivery requires a compatible protocol receiving edge. The invariant does not create a receiver: absence of one at the service deadline can block the link. That is a property to test, not a guaranteed consequence of bounded service time.

## 7. Timing and scheduling assumptions

Clocks advance continuously together. integer counters change only through updates. Time units have no intrinsic physical scale. D_MIN=1, D_MAX=3, ACK_TIMEOUT=14 and MAX_RETRY=2 are experimental values. A physical unit must be stated consistently if results are converted to seconds. The standalone test's 100 ms convention does not automatically calibrate the application.

Urgent command admission channels prevent time passing while their synchronisation is available. They do not guarantee FIFO order or fairness. The urgent broadcast hurry expresses immediate supervisor transitions when enabled; it is not a transmitted command. Ordinary mission/application edges may wait indefinitely. Consequently, bounded per-packet service does not by itself prove a bounded whole preparation time or universal progress. An acknowledgement exactly at the timeout boundary can compete with a timeout transition.

## 8. Integration and heartbeat scope decisions

Versions 05/06 tried packet adapters, independent staging and receive mailboxes. These changed admission timing and added many buffer-state combinations. Version 06B removed them while preserving packet storage, variable delay and delayed command loss. This limits complexity without redesigning the protocols.

Explicit recurring heartbeats increased observed verification effort. Version 07 stopped new generation after an outcome while allowing pending traffic to drain, but still retained pre-outcome interleavings. Version 08 excludes heartbeat processes from composition; no abstract monitor replaces them. Main-model conclusions therefore exclude freshness and connection-loss response. The no-heartbeat setting is an ablation relative to the heartbeat-enabled extension. Comparison copies must otherwise match, including the delayed-ACK fix.
