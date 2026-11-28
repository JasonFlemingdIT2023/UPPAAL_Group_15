// P01: Success reachable
E<> Supervisor.Done

// P08: Drone 0 timeout exhaustion reachable
E<> CommandClient(0).Failed

// P10: ARM executed despite failed confirmation
E<> (cmdFailed[0][ARM] && armed[0])

// P11: ARM not yet executed at failed confirmation
E<> (cmdFailed[0][ARM] && !armed[0])

// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done
