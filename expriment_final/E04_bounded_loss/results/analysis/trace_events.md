# E04 diagnostic traces

Finite traces use time relative to drone 0 first ARM admission. They are witnesses, not timing bounds.

## n1_dmax3_timeout24_legacy_both_budget0_retry0 / P26

Raw log: [UPPAAL trace](../traces/n1_dmax3_timeout24_legacy_both_budget0_retry0_P26.txt)

The counterexample consists of the initial symbolic state. Supervisor.Idle has no invariant/urgent outgoing edge, so time can elapse indefinitely without beginning uploads.

## n3_dmax3_timeout24_legacy_both_budget0_retry0 / P26

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout24_legacy_both_budget0_retry0_P26.txt)

The counterexample consists of the initial symbolic state. Supervisor.Idle has no invariant/urgent outgoing edge, so time can elapse indefinitely without beginning uploads.

## n1_dmax3_timeout24_legacy_both_budget2_retry2 / P28

Raw log: [UPPAAL trace](../traces/n1_dmax3_timeout24_legacy_both_budget2_retry2_P28.txt)

| Relative time | Event | lossCount |
|---:|---|---:|
| 0 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } | 0 |
| 0 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 0 |
| 1 | Link.Transmitting->Link.Lost { lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND &#124;&#124; packet.kind == PK_ACCEPTED &#124;&#124; packet.kind == PK_DENIED), tau, lossCount++ } | 1 |
| 24 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } | 1 |
| 24 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 1 |
| 25 | Link.Transmitting->Link.Lost { lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND &#124;&#124; packet.kind == PK_ACCEPTED &#124;&#124; packet.kind == PK_DENIED), tau, lossCount++ } | 2 |
| 48 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } | 2 |
| 48 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 2 |
| 49 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } | 2 |
| 50 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } | 2 |
| 50 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } | 2 |
| 50 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } | 2 |
| 51 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } | 2 |
| 52 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } | 2 |
| 52 | Supervisor.Starting->Supervisor.Done { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) cmdAccepted[i][START], hurry!, 1 } | 2 |

Final locations: `( Supervisor.Done Sender0.Done Drone0.Uploaded Link.Idle CommandClient(0).Idle CommandServer(0).Idle )`

## n1_dmax3_timeout24_legacy_both_budget2_retry1 / P11

Raw log: [UPPAAL trace](../traces/n1_dmax3_timeout24_legacy_both_budget2_retry1_P11.txt)

| Relative time | Event | lossCount |
|---:|---|---:|
| 0 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } | 0 |
| 0 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 0 |
| 1 | Link.Transmitting->Link.Lost { lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND &#124;&#124; packet.kind == PK_ACCEPTED &#124;&#124; packet.kind == PK_DENIED), tau, lossCount++ } | 1 |
| 24 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } | 1 |
| 24 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 1 |
| 25 | Link.Transmitting->Link.Lost { lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND &#124;&#124; packet.kind == PK_ACCEPTED &#124;&#124; packet.kind == PK_DENIED), tau, lossCount++ } | 2 |
| 48 | CommandClient(0).WaitAck->CommandClient(0).Failed { x >= ACK_TIMEOUT && retries == MAX_RETRY, tau, cmdFailed[id][current] := true } | 2 |

Final locations: `( Supervisor.Arming Sender0.Done Drone0.Uploaded Link.Idle CommandClient(0).Failed CommandServer(0).Idle )`

## n1_dmax3_timeout24_legacy_both_budget1_retry0 / P10

Raw log: [UPPAAL trace](../traces/n1_dmax3_timeout24_legacy_both_budget1_retry0_P10.txt)

| Relative time | Event | lossCount |
|---:|---|---:|
| 0 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } | 0 |
| 0 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 0 |
| 3 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } | 0 |
| 4 | Link.Transmitting->Link.Lost { lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND &#124;&#124; packet.kind == PK_ACCEPTED &#124;&#124; packet.kind == PK_DENIED), tau, lossCount++ } | 1 |
| 24 | CommandClient(0).WaitAck->CommandClient(0).Failed { x >= ACK_TIMEOUT && retries == MAX_RETRY, tau, cmdFailed[id][current] := true } | 1 |

Final locations: `( Supervisor.Arming Sender0.Done Drone0.Uploaded Link.Idle CommandClient(0).Failed CommandServer(0).Idle )`

## n3_dmax3_timeout14_legacy_both_budget0_retry0 / P08

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_legacy_both_budget0_retry0_P08.txt)

| Relative time | Event | lossCount |
|---:|---|---:|
| 0 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } | 0 |
| 0 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } | 0 |
| 12 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } | 0 |
| 14 | CommandClient(0).WaitAck->CommandClient(0).Failed { x >= ACK_TIMEOUT && retries == MAX_RETRY, tau, cmdFailed[id][current] := true } | 0 |

Final locations: `( Supervisor.Arming Sender0.Done Sender1.Done Sender2.Done Drone0.Uploaded Drone1.Uploaded Drone2.Uploaded Link.Transmitting CommandClient(0).Failed CommandClient(1).Idle CommandClient(2).WaitAck CommandServer(0).Idle CommandServer(1).Idle CommandServer(2).Decide )`

