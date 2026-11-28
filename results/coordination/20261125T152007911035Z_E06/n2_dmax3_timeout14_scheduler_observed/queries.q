// P01: Success reachable
E<> Supervisor.Done

// P15: Any drone failure reachable
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]

// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done

// P29: ACK pending flags exactly reflect server reply states
A[] ((ackPending[0] == CommandServer(0).Decide) && (ackPending[1] == CommandServer(1).Decide))

// P30: Drone 0 pending heartbeat eventually gains admission
HBSender(0).Pending --> HBSender(0).Waiting

// P31: Drone 1 pending heartbeat eventually gains admission
HBSender(1).Pending --> HBSender(1).Waiting

// P35: No drone exhausts command retries
A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])

// P36: No command retry counter increment
A[] (CommandClient(0).retries == 0 && CommandClient(1).retries == 0)

// P37: Every admitted command waits at most two packet service windows for reply
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX) && (CommandClient(1).WaitAck imply CommandClient(1).x <= 2 * D_MAX))

// P34: Success with every heartbeat observed reachable
E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])
