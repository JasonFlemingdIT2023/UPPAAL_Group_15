# Formal requirements for drone show coordination

**Luzhong · Group 15 · Main model v08**

A ground control station (GCS) uploads missions to three drones, waits for their upload confirmations, then sends ARM and START in stages. Each drone has a three-item symbolic mission. `Done` means the GCS received all START acceptances. `Aborted` means that the supervisor stopped coordinating. An abstract local START and the physical completion of the show are different events. The current model ends at command coordination. [v08 model](../models/08_final_version.xml) · [Model behaviour](../docs/model_descriptions/08_final_mission_command.md)

The two configurations use one shared packet slot, 1–3 model time units of service after packet admission, a reply timeout of 14 units per admitted command attempt, and at most two retransmissions. The command-loss configuration can drop a command request or acknowledgment (ACK). Mission packets remain reliable. [Modelling assumptions](../docs/architecture_and_modeling_decisions.md)

## Model requirements

R-numbers match the property catalogue. P-numbers refer to the group’s experiment plan. The scenarios motivate the rules. Some deliberately illustrate what would happen if a prerequisite were bypassed. [Property catalogue](property_catalog.md) · [Experiment plan](../docs/experiment_plan_and_results.md)

| ID | Requirement | Reason | Motivating scenario | Plan |
| --- | --- | --- | --- | --- |
| R1 | The GCS shall mark a drone’s upload successful only after that drone installs its mission and the GCS receives its final acknowledgment. | The fleet proceeds on confirmed mission uploads. | Drone 2 has installed its mission, but the ACK is still in transit. Its upload stays pending at the GCS. | |
| R2 | Each drone shall request and accept mission items in sequence and issue its upload acknowledgment only after accepting all three items. | A complete and correctly ordered mission determines what the drone is prepared to execute. | The receiver has accepted items 0 and 1 and is waiting for item 2. It cannot acknowledge the upload yet. | |
| R3 | A drone shall apply ARM only after it has installed its own mission. | The installed mission is the drone’s local prerequisite for arming. | If an ARM request reaches a drone before its upload completes, the drone declines it. | P02 |
| R4 | A drone shall apply START only while armed. | The drone needs a local readiness check at START. | If a START request reaches a drone that remains disarmed, the drone declines it. | P03 |
| R5 | The GCS shall start ARM dispatch only after confirming mission uploads for every rostered drone. | A late upload must hold the fleet in preparation. | The third drone’s mission ACK arrives later than the first two. The GCS waits for it before dispatching ARM. | |
| R6 | The GCS shall start START dispatch only after receiving an ARM acceptance from every rostered drone. | The fleet start decision depends on confirmed arming across the roster. | Two ARM acceptances arrive while the third is outstanding. The GCS keeps START pending. | |
| R7 | The GCS shall record successful coordination only after receiving all START acceptances. Each acceptance shall correspond to an actual local START effect in the model. | The GCS needs evidence from the entire fleet. | Two drones return their START acceptances and the third reply is delayed. The GCS waits for the third reply before recording success. | P04 |
| R8 | For each drone and command, the GCS shall record at most one final outcome of accepted, denied, or unconfirmed after timeout exhaustion. | The supervisor needs a consistent outcome for each exchange. | A reply arrives after timeout exhaustion. The command remains recorded as unconfirmed. | |
| R9 | The client shall leave an attempt’s reply wait within 14 model time units of admitting the command to the link. On timeout it shall schedule another attempt if the retry budget allows it and record the command as unconfirmed when that budget is exhausted. | A missing reply needs a bounded response per attempt. | The first attempt times out and the client schedules a retry. If the initial attempt and both permitted retransmissions go unanswered, the client records failure. | P08, P09 |
| R10 | Every delivered or dropped packet shall spend 1–3 model time units in the slot, measured from admission. | A dropped transmission consumes link service time too. | The link admits a command and drops it after service while another sender waits for the slot. | P07 |
| R11 | Every admitted packet shall eventually leave the slot through delivery or loss. | A stuck packet would block all other senders. | An ACK is in the slot when its client moves into retry handling. The link must still be able to finish handling the ACK. | P06 |
| R12 | If no further action is possible, the supervisor shall already have recorded success or abort and the link shall be idle. | A blocked exchange leaves coordination unresolved or link work unfinished. | An admitted packet reaches its service deadline with no compatible receiving action. A deadlock there would violate this requirement. | P05 |
| R13 | Once ARM dispatch begins, the supervisor shall eventually record successful coordination or abort. | The command phase needs a terminal decision even when retries fail. | Repeated request or reply loss exhausts a client’s attempts. The supervisor must reach an abort outcome. | |
| R14 | The link shall store the source and destination that match each packet’s drone and transmission direction. | Concurrent exchanges need distinct peer information. | Drone 1’s acceptance enters the shared slot while drone 0 also awaits a reply. The packet identifies drone 1 as source and the GCS as destination. | |

## Scenario requirements for the experiments

Each row states a behaviour the test configuration is expected to admit. The experiment may show both success and failure on different runs.

| ID | Plain-language expectation | Reason and motivating scenario | Plan |
| --- | --- | --- | --- |
| D1 | In either configuration it shall be possible for the GCS to reach successful coordination. | If all required requests and replies arrive, the three-drone workflow should be able to complete. | P01 |
| D2 | With command loss enabled, the link shall be able to admit and then drop a command request or reply. With loss disabled, a packet drop shall be unreachable. | A START request occupies the slot and is then dropped. This exercises the configured network fault. | P12 |
| D3 | With command loss enabled, drone 0 shall be able to remain armed when the GCS records that ARM ended without confirmation. | The request reaches the drone and takes effect, but its reply and later attempts leave the GCS without confirmation. | P10 |
| D4 | With command loss enabled, the supervisor shall be able to abort after at least one drone applies START. | A drone can act on START while a command exchange times out. The GCS outcome may coexist with local START. | |
| D5 | With command loss enabled, drone 0’s command client shall be able to exhaust its attempts and record missing confirmation. | Requests or replies can be lost on all attempts. This exercises the end of the finite retry budget. | P08 |
| D6 | A drone 0 client that reaches its reply deadline with retry budget remaining shall be able to schedule another attempt. | Shared-slot contention can bring an ACK to the deadline even on a reliable link. A subsequent send transition can establish that a retransmission entered the link. | P09 |
| D7 | With command loss enabled, drone 0 shall also be able to remain unarmed at the instant the GCS records ARM as unconfirmed. | All ARM requests for that drone can be dropped. Together with D3, this shows why the failure record represents missing confirmation. | P11 |

## Requirements for model extensions

| ID | Candidate requirement | Reason and motivating scenario |
| --- | --- | --- |
| EXT-01 | The GCS shall detect link silence within a configured timeout after session opening or the last valid heartbeat. Only the monitored drone’s matching heartbeat shall reset that timeout. | A drone may never send its first heartbeat, or fall silent after one valid heartbeat. The GCS needs to detect both cases. [Earlier heartbeat experiment](../docs/model_descriptions/07_heartbeat_experiments_and_ablation.md) |
| EXT-02 | The GCS shall stop sending START for a cancelled show. A drone that processes cancellation or installs a newer show epoch shall reject a delayed START for the invalidated epoch. | An in-flight START can arrive before or after CANCEL. Both arrival orders matter because each endpoint learns of cancellation at a different time. |
| EXT-03 | An authorised local START shall occur within its configured start window. The difference between the first and last start shall stay within an agreed bound. | Contention can stagger starts across drones. Compare local start events under an explicit clock synchronisation assumption. |
| EXT-04 | The GCS shall report show completion only after receiving matching finish evidence from every rostered drone. | A drone can accept START and fail to provide a finish report. Completion needs its own evidence. |
| EXT-05 | If a mission transfer step loses a packet, each missing step shall be retried within a configured budget. The upload shall close with confirmed success or failure by its deadline. | A lost mission item can halt transfer. A lost final ACK can leave the drone with an installed mission and the GCS without confirmation. |
| EXT-06 | Repeated START requests for the same drone and show shall produce at most one local start effect. | START takes effect, its ACK is lost, and the GCS resends it. A model observer would need to count actual start effects because v08 stores a Boolean. |

## Verification evidence and open work

All 19 formulas covering the 14 model requirements were satisfied in both configurations. Nominal success and retry scheduling were reachable in both. All seven scenario targets were reachable with command loss enabled. The reliable run found no witness for loss, retry exhaustion on drone 0, either ARM-failure scenario, or a fleet abort after START. The catalogue records the exact results. [Property catalogue](property_catalog.md) · [Reliable log](v08_reliable.log) · [Command-loss log](v08_lossy.log)

The runs establish which states are reachable. A D3 diagnostic trace would document the command and ACK sequence for a report example. The extensions need observers or model changes before their requirements can be verified. One possible experiment outside UPPAAL is to compare the retry sequence after withholding the first ACK of a supported read-only command on an ArduPilot SITL vehicle. [Command-loss model](v08_lossy.xml) · [ArduPilot SITL](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)
