# N=4 retry and late-ACK witness

Raw log: `20261125T131521932777Z_E01/n4_dmax3_timeout14/P17/stdout.log`

Times are relative to client 0 first command admission; one witness, not a timing bound.

| Relative time | Transition |
|---:|---|
| 0 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 0 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 12 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 14 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 14 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).Sending->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
