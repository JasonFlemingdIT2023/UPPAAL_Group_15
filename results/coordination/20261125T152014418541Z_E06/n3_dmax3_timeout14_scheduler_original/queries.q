// P35: No drone exhausts command retries
A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])

// P34: Success with every heartbeat observed reachable
E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])
