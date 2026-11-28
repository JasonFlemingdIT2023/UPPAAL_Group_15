// P45: No deadlock with heartbeat active
A[] !deadlock

// P06: Admitted packet eventually leaves
Link.Transmitting --> Link.Idle
