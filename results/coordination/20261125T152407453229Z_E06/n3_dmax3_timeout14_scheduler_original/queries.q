// P36: No command retry counter increment
A[] (CommandClient(0).retries == 0 && CommandClient(1).retries == 0 && CommandClient(2).retries == 0)

// P37: Every admitted command waits at most two packet service windows for reply
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX) && (CommandClient(1).WaitAck imply CommandClient(1).x <= 2 * D_MAX) && (CommandClient(2).WaitAck imply CommandClient(2).x <= 2 * D_MAX))

// P25: Prepared fleet inevitably succeeds
Supervisor.Prepared --> Supervisor.Done
