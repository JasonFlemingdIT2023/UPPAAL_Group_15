// P01: Success reachable
E<> Supervisor.Done

// P08: Drone 0 timeout exhaustion reachable
E<> CommandClient(0).Failed

// P10: ARM executed despite failed confirmation
E<> (cmdFailed[0][ARM] && armed[0])

// P15: Any drone failure reachable
E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]

// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done
