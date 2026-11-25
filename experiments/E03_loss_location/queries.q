// P01: Success reachable
E<> Supervisor.Done

// P02: ARM prerequisite
A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])

// P03: START prerequisite
A[] forall (i : drone_id) (started[i] imply armed[i])

// P04: Success requires START evidence
A[] (Supervisor.Done imply forall (i : drone_id) cmdAccepted[i][START])

// P05: No pre-outcome deadlock
A[] (deadlock imply (Supervisor.Done || Supervisor.Aborted))

// P06: Admitted packet eventually leaves
Link.Transmitting --> Link.Idle

// P07: Service time window
A[] ((Link.Delivered || Link.Lost) imply (Link.t >= D_MIN && Link.t <= D_MAX))

// P08: Drone 0 timeout exhaustion reachable
E<> CommandClient(0).Failed

// P09: Drone 0 retry reachable
E<> (CommandClient(0).retries > 0)

// P10: ARM executed despite failed confirmation
E<> (cmdFailed[0][ARM] && armed[0])

// P11: ARM not yet executed at failed confirmation
E<> (cmdFailed[0][ARM] && !armed[0])

// P12: Loss reachable
E<> Link.Lost

// P13: Success agrees with drone states
A[] (Supervisor.Done imply forall (i : drone_id) started[i])

// P14: Confirmed missions contain every item
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))

// P15: Any drone failure reachable
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]

// P16: Prepared fleet eventually reaches an outcome
Supervisor.Prepared --> (Supervisor.Done || Supervisor.Aborted)

// P17: ARM accepted after timeout-triggered retry counter increment
E<> (cmdAccepted[0][ARM] && CommandClient(0).current == ARM && CommandClient(0).retries > 0)

// P18: ARM still absent at a quiescent aborted outcome
E<> (Supervisor.Aborted && Link.Idle && CommandClient(0).Failed && CommandClient(1).Idle && CommandClient(2).Idle && CommandServer(0).Idle && CommandServer(1).Idle && CommandServer(2).Idle && !armed[0] && cmdFailed[0][ARM])

// P19: Command request loss reachable
E<> (Link.Lost && Link.packet.kind == PK_COMMAND)

// P20: Command acknowledgement loss reachable
E<> (Link.Lost && (Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))

// P21: Mission-message loss unreachable
A[] (Link.Lost imply (Link.packet.kind == PK_COMMAND || Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))

// P22: Unexecuted ARM after confirmation failure eventually executes
(cmdFailed[0][ARM] && !armed[0]) --> armed[0]
