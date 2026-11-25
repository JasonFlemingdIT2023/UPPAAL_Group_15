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
