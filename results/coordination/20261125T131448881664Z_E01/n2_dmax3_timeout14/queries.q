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

// P13: Success agrees with drone states
A[] (Supervisor.Done imply forall (i : drone_id) started[i])

// P14: Confirmed missions contain every item
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)))

// P15: Any drone failure reachable
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]

// P16: Prepared fleet eventually reaches an outcome
Supervisor.Prepared --> (Supervisor.Done || Supervisor.Aborted)

// P23: Any drone retry counter increment reachable
E<> (CommandClient(0).retries > 0 || CommandClient(1).retries > 0)
