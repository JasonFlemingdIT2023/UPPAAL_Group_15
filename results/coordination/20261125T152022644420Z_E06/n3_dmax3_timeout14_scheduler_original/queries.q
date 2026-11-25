// P03: START prerequisite
A[] forall (i : drone_id) (started[i] imply armed[i])

// P35: No drone exhausts command retries
A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])

// P30: Drone 0 pending heartbeat eventually gains admission
HBSender(0).Pending --> HBSender(0).Waiting

// P31: Drone 1 pending heartbeat eventually gains admission
HBSender(1).Pending --> HBSender(1).Waiting

// P32: Drone 2 pending heartbeat eventually gains admission
HBSender(2).Pending --> HBSender(2).Waiting
