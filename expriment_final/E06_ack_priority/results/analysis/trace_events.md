# E06 diagnostic events

Absolute model times are parsed from the original trace delays.

## original / P34

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_scheduler_original_P34.txt)

| Time | Event |
|---:|---|
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 111 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 112 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 113 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |

## original / P35

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_scheduler_original_P35.txt)

| Time | Event |
|---:|---|
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 113 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 115 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 118 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 118 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 120 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 120 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 121 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 127 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 130 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 133 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 135 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 138 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 140 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 140 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 143 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 143 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 146 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |

## ack_priority / P34

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_scheduler_ack_priority_P34.txt)

| Time | Event |
|---:|---|
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current), ackPending[id] := false };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 111 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 112 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current), ackPending[id] := false };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 113 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |

## ack_priority / P38

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_scheduler_ack_priority_P38.txt)

| Time | Event |
|---:|---|
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current), ackPending[id] := false };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 111 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { forall(i:(const (label drone_id:(range (int) "0" "N - 1")))) !ackPending[i], cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 114 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current), ackPending[id] := false };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 117 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |

