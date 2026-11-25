// P01: Success reachable
E<> Supervisor.Done

// P03: START prerequisite
A[] forall (i : drone_id) (started[i] imply armed[i])

// P08: Drone 0 timeout exhaustion reachable
E<> CommandClient(0).Failed

// P24: Every drone heartbeat can be observed
E<> forall (i : drone_id) heartbeatSeen[i]
