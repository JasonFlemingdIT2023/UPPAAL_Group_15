# Formal requirements and property catalogue

**Luzhong · Group 15 · Main model v08**

## Scope and assumptions

One ground control station (GCS) coordinates three drones. For each drone it uploads a three-item symbolic mission, requests ARM and then requests START. The supervisor waits for every upload confirmation before ARM and for every ARM acceptance before START. Each drone handles one logical command of each type, with retries allowed. [Main model](../models/08_final_version.xml) · [Model description](../docs/model_descriptions/08_final_mission_command.md)

The GCS records evidence in `uploadDone`, `cmdAccepted`, `cmdDenied` and `cmdFailed`. Local drone effects are recorded in `missionInstalled`, `armed` and `started`. The command server sets an effect when its acceptance reply enters the link, so a lost reply can leave the effect in place without GCS confirmation. `Supervisor.Done` means all START acceptances were received. `Supervisor.Aborted` means the supervisor stopped coordination. In-flight exchanges can still finish after an abort. Flight completion, operator cancellation, start synchronisation and heartbeat monitoring are outside the v08 composition. [Architecture and modelling decisions](../docs/architecture_and_modeling_decisions.md)

| Configuration | Model parameters |
| --- | --- |
| E1 reliable reference | `N=3`, `MISSION_SIZE=3`, `D_MIN=1`, `D_MAX=3`, `ACK_TIMEOUT=14`, `MAX_RETRY=2`, `LOSSY=false`. |
| E2 command loss | E1 with `LOSSY=true`. The link can drop command requests and command accept/deny replies. Mission traffic stays reliable. Arbitrarily many consecutive command losses are permitted. |

The link has one service slot shared by both directions. Admission is a rendezvous with a waiting sender. The service clock starts at admission, so time spent waiting for the slot is outside the service window. The command clock resets on each command admission and covers the wait for its reply, including any contention before that reply is admitted. A matching reply and a timeout can compete at `ACK_TIMEOUT`. All constants use model time units. The model assumes neither a physical time conversion nor FIFO service. [Experiment plan](../docs/experiment_plan_and_results.md)

## Main model properties

The formulas refer to existing v08 declarations and locations. Query IDs and formulas match the [base model query file](base_model_queries). The repository baseline is commit `2ecefd2`, XML SHA-256 `77896d59a2282f817786b7712f0d4372432fce73bc54a6bbed32500f3c40744d`.

On 24 November 2026, UPPAAL 5.0.0 (rev. `714BA9DB36F49691`) completed E1 and E2 using breadth-first search with trace generation disabled. All 19 formulas covering R1–R14 were satisfied in both configurations. The query file SHA-256 was `168ad2c42fa0fdb0853ec772e07bfaf404852a698346a650a8cca6b1b28400a1`. [E1 verifier log](v08_reliable.log) · [E2 verifier log](v08_lossy.log)

| ID | Type | Requirement and observable evidence | UPPAAL formula | Scope |
| --- | --- | --- | --- | --- |
| R1 | Safety | When a GCS upload is confirmed, that drone shall have installed its mission. Compare `uploadDone` with `missionInstalled` for the same drone. | `A[] forall (i : drone_id) (uploadDone[i] imply missionInstalled[i])` | E1, E2 |
| R2 | Safety | Each receiver shall request and accept items in sequence and only acknowledge after all three items. Its accepted-item count shall match the requested index while exchanging items and equal `MISSION_SIZE` at `AckPending` and `Uploaded`. In this model receives are indexed by the expected sequence. | `A[] (((Drone0.RequestedItem or Drone0.WaitItem) imply Drone0.receivedCount == Drone0.nextSequence) and ((Drone0.AckPending or Drone0.Uploaded) imply Drone0.receivedCount == MISSION_SIZE))` | E1, E2. Suite repeats the check for `Drone1` and `Drone2`. |
| R3 | Safety | A drone shall arm only with its mission installed. | `A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])` | E1, E2 |
| R4 | Safety | A drone shall start only after it has armed. | `A[] forall (i : drone_id) (started[i] imply armed[i])` | E1, E2 |
| R5 | Safety | The supervisor shall activate ARM clients only after every GCS upload confirmation. `armSent` records client activation. | `A[] ((exists (i : drone_id) Supervisor.armSent[i]) imply (forall (j : drone_id) uploadDone[j]))` | E1, E2 |
| R6 | Safety | The supervisor shall activate START clients only after receiving every ARM acceptance. `startSent` records client activation. | `A[] ((exists (i : drone_id) Supervisor.startSent[i]) imply (forall (j : drone_id) cmdAccepted[j][ARM]))` | E1, E2 |
| R7 | Safety | The supervisor shall report `Done` only after it records all START acceptances, each backed by the corresponding abstract local start. | `A[] (Supervisor.Done imply (forall (i : drone_id) (cmdAccepted[i][START] and started[i])))` | E1, E2 |
| R8 | Safety | An accepted, denied or exhausted command shall have at most one recorded client outcome. The client matches replies by drone and current command. This query checks outcome consistency. | `A[] forall (i : drone_id) forall (c : cmd_id) (not (cmdAccepted[i][c] and cmdDenied[i][c]) and not (cmdAccepted[i][c] and cmdFailed[i][c]) and not (cmdDenied[i][c] and cmdFailed[i][c]))` | E1, E2 |
| R9 | Timing | Once a command enters the link, a client shall leave its current reply wait no later than `ACK_TIMEOUT` after that admission. A matching reply can close the command, a timeout can return it to `Sending` with retry budget left, and the final timeout can record failure. | `A[] forall (i : drone_id) (CommandClient(i).WaitAck imply CommandClient(i).x <= ACK_TIMEOUT)` plus `CommandClient(0).WaitAck --> (CommandClient(0).Sending or CommandClient(0).Idle or CommandClient(0).Failed)` | E1, E2. Suite repeats the leads-to check for each client. |
| R10 | Timing | An admitted packet that is delivered or lost shall take between `D_MIN` and `D_MAX` model time units. Both are measured from admission to the outcome edge. | `A[] ((Link.Delivered or Link.Lost) imply (Link.t >= D_MIN and Link.t <= D_MAX))` | E1, E2 |
| R11 | Liveness | Every admitted packet shall eventually leave the slot. This also tests for a rendezvous that cannot complete at the service deadline. | `Link.Transmitting --> Link.Idle` | E1, E2 |
| R12 | Safety | Any deadlock shall occur only in an intended terminal state, `Done` or `Aborted`, with the link idle. A deadlock before a supervisor outcome or with an occupied slot violates the requirement. | `A[] (deadlock imply ((Supervisor.Done or Supervisor.Aborted) and Link.Idle))` | E1, E2 |
| R13 | Liveness | Once the supervisor begins ARM dispatch, coordination shall eventually end in `Done` or `Aborted`. This tests the command phase under the integrated scheduling rules. | `Supervisor.Arming --> (Supervisor.Done or Supervisor.Aborted)` | E1, E2 |
| R14 | Safety | A packet in the shared slot shall carry the source and destination corresponding to its peer and message direction. Delivery uses the stored peer, kind and sequence or command indices. The formula checks the stored addresses. The delivery channel mapping can be inspected in the network template. | `A[] (Link.Transmitting imply (((Link.packet.kind == PK_COUNT or Link.packet.kind == PK_ITEM or Link.packet.kind == PK_COMMAND) and Link.packet.src == GCS_ENDPOINT and Link.packet.dst == Link.packet.peer + 1) or ((Link.packet.kind == PK_REQUEST or Link.packet.kind == PK_MISSION_ACK or Link.packet.kind == PK_ACCEPTED or Link.packet.kind == PK_DENIED) and Link.packet.src == Link.packet.peer + 1 and Link.packet.dst == GCS_ENDPOINT)))` | E1, E2. Heartbeat is inactive. |

R9's clock query restates a location invariant. Its leads-to check tests that the client can actually leave the wait. On the timeout edge, a retry increments `retries` only when it is below `MAX_RETRY`. After the final unanswered attempt the `Failed` edge sets `cmdFailed`. The two retries permit up to three admissions. Measuring time from command activation or bounding the whole operation requires accounting for all pre-admission waits. The late-ACK fix is on `Sending → Idle`, which can accept a matching reply before the retry is admitted. Verifying that edge specifically would require a trace or an observer for that transition. [Command retry and ACK handling](../docs/model_descriptions/08_final_mission_command.md)

### Scenario checks

An `E<>` query asks whether its target state is reachable under the tested configuration. The table records results for both configurations.

| ID | Scenario | UPPAAL formula | E1 reliable | E2 command loss | Interpretation |
| --- | --- | --- | --- | --- | --- |
| D1 | A successful coordination run | `E<> Supervisor.Done` | Reachable | Reachable | The GCS can collect all START acceptances in either configuration. |
| D2 | The link can lose a packet | `E<> Link.Lost` | Unreachable | Reachable | E2 exercises the command-protocol loss edge. |
| D3 | ARM can take effect without confirmation | `E<> (armed[0] and cmdFailed[0][ARM])` | Unreachable | Reachable | The local armed state can coexist with exhausted attempts at the GCS. |
| D4 | The fleet can abort after a drone starts | `E<> (Supervisor.Aborted and (exists (i : drone_id) started[i]))` | Unreachable | Reachable | The supervisor can reach `Aborted` while at least one drone has already applied START. |
| D5 | A command client can exhaust its retry budget | `E<> CommandClient(0).Failed` | Unreachable | Reachable | The query covers drone 0. Failure records missing confirmation. |
| D6 | A command client can schedule a retry | `E<> (CommandClient(0).retries > 0)` | Reachable | Reachable | The counter increments at a timeout before a retransmission is admitted. |
| D7 | ARM can still be unconfirmed and unapplied at the same instant | `E<> (cmdFailed[0][ARM] and not armed[0])` | Unreachable | Reachable | Together with D3, this shows two possible local states for the same client failure. Pending traffic may still change the local state after the queried instant. |

In E1, D6 establishes that drone 0's command client can reach a timeout and schedule a retry even with reliable delivery. The 1–3 unit bound begins when each packet gets the shared slot. The 14-unit ACK timer also covers any contention before the reply gets that slot, and an ACK at the timeout boundary can compete with the timeout transition. The E1 run did not generate a trace, so it establishes reachability without identifying the particular ordering that reaches the timeout. D5 establishes that drone 0 cannot exhaust its retry budget in this configuration.

The experiment plan's P01–P12 map in order to D1, R3, R4, R7, R12, R11, R10, D5, D6, D3, D7 and D2. R7 also checks the local start effect, and R12 also checks that the slot is idle. For fleet scaling, regenerate the explicit mission instances and adjust the per-drone query instances to match the chosen fleet size. [Experiment plan](../docs/experiment_plan_and_results.md)

R13 establishes that once the supervisor reaches `Arming`, it eventually reaches `Done` or `Aborted` in both configurations. The earlier supervisor and mission transitions can admit unbounded waiting under the model's scheduling. E2 enables loss for both requests and replies, and its log contains no diagnostic traces. Identifying which packet was lost in a particular execution would require a trace. [UPPAAL symbolic query semantics](https://docs.uppaal.org/language-reference/query-semantics/symb_queries/)

## Existing evidence and extensions

- **Standalone link evidence.** Saved runs satisfy packet integrity, single delivery per packet, accounting, service timing and slot release across all four standalone configurations (`N4–N11`). Each used two producers, four packets and compatible receiver stubs. Bounded loss belongs to the standalone harness. The saved results apply to their recorded snapshots and hashes. [Results CSV](../results/network_results.csv) · [Rerun record](../results/network_runs/README_rerun.txt)
- **Historical command and heartbeat evidence.** The v03 command description reports baseline query outcomes for its earlier link. Version 07 tests a finite heartbeat generation period. Version 08 has no active sender or monitor, so a heartbeat reachability query left in its XML has no heartbeat event to witness. [Command baseline](../docs/model_descriptions/03_mavlink_command_protocol.md) · [Heartbeat experiment](../docs/model_descriptions/07_heartbeat_experiments_and_ablation.md)
- **Meeting requirements beyond v08.** A heartbeat extension would measure from session opening or the last valid receipt and detect silence within a specified timeout. An operator cancellation extension would reject an old START after local cancellation or epoch change, and test the race between GCS cancellation and its delivery. Timed start would require actual start timestamps and an agreed skew bound. Reporting show completion would require explicit controller finish evidence from each rostered drone. [Formal requirements for model extensions](formal_requirements.md#requirements-for-model-extensions)
- **Optional SITL comparison.** On a local simulated vehicle, record one ordinary command exchange, then arrange for the test GCS to miss the first ACK for the same read-only command while allowing later replies. Compare retries, ACK timing and final client outcome with D3's command-confirmation sequence. The comparison has no recorded SITL result. [ArduPilot SITL](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)

## Reproduce the checks

From the repository root, run `verifyta models/08_final_version.xml formal-requirements/base_model_queries` for E1 and `verifyta formal-requirements/v08_lossy.xml formal-requirements/base_model_queries` for E2. The E2 copy changes only `LOSSY` to `true` and has SHA-256 `c411e623f1919ae7ab46b896fb5f4021c68e174aa39b07fbce19d0feb49781e6`. The explicit query file selects the checks above. The saved logs show the paths used when the verification runs were originally recorded. Record a search that is interrupted, exceeds its limit or cannot start as inconclusive or unrun, as applicable. [E2 model snapshot](v08_lossy.xml)
