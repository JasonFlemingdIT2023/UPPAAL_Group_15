// P34: Success with every heartbeat observed reachable
E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])
