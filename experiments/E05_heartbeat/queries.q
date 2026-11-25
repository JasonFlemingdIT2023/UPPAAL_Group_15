// P01: Successful coordination is reachable
E<> Supervisor.Done

// P03: START requires ARM
A[] forall (i : drone_id) (started[i] imply armed[i])

// P08: Drone 0 retry exhaustion is reachable (false is desirable)
E<> CommandClient(0).Failed

// P24: Every drone heartbeat has been observed in one reachable state
E<> forall (i : drone_id) heartbeatSeen[i]
