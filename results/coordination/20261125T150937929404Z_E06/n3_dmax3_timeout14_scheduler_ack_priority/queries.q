// P01: Success reachable
E<> Supervisor.Done

// P15: Any drone failure reachable
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]

// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done

// P03: START prerequisite
A[] forall (i : drone_id) (started[i] imply armed[i])

// P29: ACK pending flags exactly reflect server reply states
A[] ((ackPending[0] == CommandServer(0).Decide) && (ackPending[1] == CommandServer(1).Decide) && (ackPending[2] == CommandServer(2).Decide))

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

// P34: Success with every heartbeat observed reachable
E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])
