// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done

// P30: Drone 0 pending heartbeat eventually gains admission
HBSender(0).Pending --> HBSender(0).Waiting

// P31: Drone 1 pending heartbeat eventually gains admission
HBSender(1).Pending --> HBSender(1).Waiting

// P32: Drone 2 pending heartbeat eventually gains admission
HBSender(2).Pending --> HBSender(2).Waiting

// P06: Admitted packet eventually leaves
Link.Transmitting --> Link.Idle

// P05: No pre-outcome deadlock
A[] (deadlock imply (Supervisor.Done || Supervisor.Aborted))

// P02: ARM prerequisite
A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])

// P04: Success requires START evidence
A[] (Supervisor.Done imply forall (i : drone_id) cmdAccepted[i][START])

// P07: Service time window
A[] ((Link.Delivered || Link.Lost) imply (Link.t >= D_MIN && Link.t <= D_MAX))

// P13: Success agrees with drone states
A[] (Supervisor.Done imply forall (i : drone_id) started[i])

// P14: Confirmed missions contain every item
A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))
