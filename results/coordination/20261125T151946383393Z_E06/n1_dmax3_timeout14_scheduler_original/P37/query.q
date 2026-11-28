// P37: Every admitted command waits at most two packet service windows for reply
A[] ((CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX))
