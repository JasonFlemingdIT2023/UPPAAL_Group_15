# E05 diagnostic traffic witnesses

Model time is absolute from initialization. Each trace is one possible execution, not a bound or average.

## n2_dmax3_timeout14_hb_active_period20 / P01

Raw log: [UPPAAL trace](../traces/n2_dmax3_timeout14_hb_active_period20_P01.txt)

| Time | Transition |
|---:|---|
| 20 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 20 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 36 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 36 | Supervisor.Arming->Supervisor.Arming { !armSent[1], begin_command[1][ARM]!, armSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 36 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 37 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 37 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][0]?, storePacket(1, PK_COMMAND, 0, 0), t := 0 } |
| 38 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 38 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 39 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 39 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][0]?, storePacket(1, PK_ACCEPTED, 0, 0), t := 0 } |
| 40 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 40 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 40 | Supervisor.Starting->Supervisor.Starting { !startSent[1], begin_command[1][START]!, startSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 40 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 41 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][1]?, storePacket(1, PK_COMMAND, 0, 1), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 42 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 43 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][1]?, storePacket(1, PK_ACCEPTED, 0, 1), t := 0 } |
| 44 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |

## n2_dmax3_timeout14_hb_active_period20_staggered / P24

Raw log: [UPPAAL trace](../traces/n2_dmax3_timeout14_hb_active_period20_staggered_P24.txt)

| Time | Transition |
|---:|---|
| 20 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD + firstOffset, tau, 1 } |
| 20 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0, firstOffset := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 23 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 30 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD + firstOffset, tau, 1 } |
| 30 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0, firstOffset := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 31 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |

## n3_dmax3_timeout14_hb_active_period20 / P01

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_hb_active_period20_P01.txt)

| Time | Transition |
|---:|---|
| 20 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 20 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 20 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 60 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 61 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[2], begin_command[2][ARM]!, armSent[2] := true };   CommandClient(2).Idle->CommandClient(2).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 101 | CommandClient(2).Sending->CommandClient(2).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[2][0]?, storePacket(2, PK_COMMAND, 0, 0), t := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[1], begin_command[1][ARM]!, armSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 102 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(2).Idle->CommandServer(2).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 102 | CommandServer(2).Decide->CommandServer(2).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[2][0]?, storePacket(2, PK_ACCEPTED, 0, 0), t := 0 } |
| 102 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 103 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(2).WaitAck->CommandClient(2).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 103 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][0]?, storePacket(1, PK_COMMAND, 0, 0), t := 0 } |
| 104 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 104 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][0]?, storePacket(1, PK_ACCEPTED, 0, 0), t := 0 } |
| 105 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 105 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 106 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[2], begin_command[2][START]!, startSent[2] := true };   CommandClient(2).Idle->CommandClient(2).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 107 | CommandClient(2).Sending->CommandClient(2).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[2][1]?, storePacket(2, PK_COMMAND, 0, 1), t := 0 } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[1], begin_command[1][START]!, startSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 108 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(2).Idle->CommandServer(2).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 108 | CommandServer(2).Decide->CommandServer(2).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[2][1]?, storePacket(2, PK_ACCEPTED, 0, 1), t := 0 } |
| 109 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(2).WaitAck->CommandClient(2).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 109 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][1]?, storePacket(1, PK_COMMAND, 0, 1), t := 0 } |
| 110 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 110 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][1]?, storePacket(1, PK_ACCEPTED, 0, 1), t := 0 } |
| 111 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 111 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 112 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 112 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 113 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |

## n3_dmax3_timeout14_hb_active_period20 / P08

Raw log: [UPPAAL trace](../traces/n3_dmax3_timeout14_hb_active_period20_P08.txt)

| Time | Transition |
|---:|---|
| 20 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 20 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 20 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 20 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 21 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Unknown->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 21 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 22 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Unknown->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 22 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 25 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Unknown->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0, heartbeatSeen[id] := true } |
| 40 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 40 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 41 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 41 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 41 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 42 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 42 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 42 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 43 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 60 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 61 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 61 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 62 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 62 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 62 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 65 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 65 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 68 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 81 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 81 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 82 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 82 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 82 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 85 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 85 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 85 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 88 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 101 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[2], begin_command[2][ARM]!, armSent[2] := true };   CommandClient(2).Idle->CommandClient(2).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 101 | CommandClient(2).Sending->CommandClient(2).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[2][0]?, storePacket(2, PK_COMMAND, 0, 0), t := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[1], begin_command[1][ARM]!, armSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 101 | Supervisor.Arming->Supervisor.Arming { !armSent[0], begin_command[0][ARM]!, armSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][0]?, current := 0, retries := 0 } |
| 102 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(2).Idle->CommandServer(2).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 102 | CommandServer(2).Decide->CommandServer(2).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[2][0]?, storePacket(2, PK_ACCEPTED, 0, 0), t := 0 } |
| 102 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 103 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(2).WaitAck->CommandClient(2).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 103 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][0]?, storePacket(1, PK_COMMAND, 0, 0), t := 0 } |
| 104 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 104 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][0]?, storePacket(1, PK_ACCEPTED, 0, 0), t := 0 } |
| 105 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 105 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][0]?, storePacket(0, PK_COMMAND, 0, 0), t := 0 } |
| 105 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 106 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][0]?, current := 0 } |
| 106 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][0]?, storePacket(0, PK_ACCEPTED, 0, 0), t := 0 } |
| 107 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(0).WaitAck->CommandClient(0).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[2], begin_command[2][START]!, startSent[2] := true };   CommandClient(2).Idle->CommandClient(2).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 107 | CommandClient(2).Sending->CommandClient(2).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[2][1]?, storePacket(2, PK_COMMAND, 0, 1), t := 0 } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[1], begin_command[1][START]!, startSent[1] := true };   CommandClient(1).Idle->CommandClient(1).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 107 | Supervisor.Starting->Supervisor.Starting { !startSent[0], begin_command[0][START]!, startSent[0] := true };   CommandClient(0).Idle->CommandClient(0).Sending { 1, begin_command[id][1]?, current := 1, retries := 0 } |
| 109 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(2).Idle->CommandServer(2).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 109 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][1]?, storePacket(1, PK_COMMAND, 0, 1), t := 0 } |
| 110 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Idle->CommandServer(1).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 110 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 113 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Idle->CommandServer(0).Decide { 1, cmd_rx[id][1]?, current := 1 } |
| 113 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 116 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 116 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 118 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 118 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 121 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 121 | CommandClient(2).WaitAck->CommandClient(2).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 121 | CommandClient(2).Sending->CommandClient(2).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[2][1]?, storePacket(2, PK_COMMAND, 0, 1), t := 0 } |
| 123 | CommandClient(1).WaitAck->CommandClient(1).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 124 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(2).Decide->CommandServer(2).Decide { 1, cmd_rx[id][1]?, 1 } |
| 124 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 124 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 127 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Decide->CommandServer(0).Decide { 1, cmd_rx[id][1]?, 1 } |
| 127 | CommandServer(2).Decide->CommandServer(2).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[2][1]?, storePacket(2, PK_ACCEPTED, 0, 1), t := 0 } |
| 130 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(2).WaitAck->CommandClient(2).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 130 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][1]?, storePacket(1, PK_COMMAND, 0, 1), t := 0 } |
| 133 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Decide->CommandServer(1).Decide { 1, cmd_rx[id][1]?, 1 } |
| 133 | HBSender(2).Waiting->HBSender(2).Pending { period >= HB_PERIOD, tau, 1 } |
| 133 | HBSender(2).Pending->HBSender(2).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[2]?, storePacket(2, PK_HEARTBEAT, 0, 0), t := 0 } |
| 136 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(2).Tracking->ConnectionMonitor(2).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 136 | HBSender(1).Waiting->HBSender(1).Pending { period >= HB_PERIOD, tau, 1 } |
| 136 | HBSender(1).Pending->HBSender(1).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[1]?, storePacket(1, PK_HEARTBEAT, 0, 0), t := 0 } |
| 138 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(1).Tracking->ConnectionMonitor(1).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 138 | HBSender(0).Waiting->HBSender(0).Pending { period >= HB_PERIOD, tau, 1 } |
| 138 | CommandClient(0).WaitAck->CommandClient(0).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 138 | CommandClient(0).Sending->CommandClient(0).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[0][1]?, storePacket(0, PK_COMMAND, 0, 1), t := 0 } |
| 141 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(0).Decide->CommandServer(0).Decide { 1, cmd_rx[id][1]?, 1 } |
| 141 | HBSender(0).Pending->HBSender(0).Waiting { 1, heartbeat_tx[id]!, period := 0 };   Link.Idle->Link.Transmitting { 1, heartbeat_tx[0]?, storePacket(0, PK_HEARTBEAT, 0, 0), t := 0 } |
| 144 | Link.Transmitting->Link.Delivered { packet.kind == PK_HEARTBEAT && t >= D_MIN, heartbeat_rx[packet.peer]!, 1 };   ConnectionMonitor(0).Tracking->ConnectionMonitor(0).Tracking { 1, heartbeat_rx[id]?, age := 0 } |
| 144 | CommandClient(1).WaitAck->CommandClient(1).Sending { x >= ACK_TIMEOUT && retries < MAX_RETRY, tau, retries++ } |
| 144 | CommandClient(1).Sending->CommandClient(1).WaitAck { 1, cmd_tx[id][current]!, x := 0 };   Link.Idle->Link.Transmitting { 1, cmd_tx[1][1]?, storePacket(1, PK_COMMAND, 0, 1), t := 0 } |
| 147 | Link.Transmitting->Link.Delivered { packet.kind == PK_COMMAND && t >= D_MIN, cmd_rx[packet.peer][packet.cmd]!, 1 };   CommandServer(1).Decide->CommandServer(1).Decide { 1, cmd_rx[id][1]?, 1 } |
| 147 | CommandServer(1).Decide->CommandServer(1).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[1][1]?, storePacket(1, PK_ACCEPTED, 0, 1), t := 0 } |
| 150 | Link.Transmitting->Link.Delivered { packet.kind == PK_ACCEPTED && t >= D_MIN, accepted_rx[packet.peer][packet.cmd]!, 1 };   CommandClient(1).WaitAck->CommandClient(1).Idle { 1, accepted_rx[id][current]?, cmdAccepted[id][current] := true } |
| 150 | CommandServer(0).Decide->CommandServer(0).Idle { canExecute(current), accepted_tx[id][current]!, execute(current) };   Link.Idle->Link.Transmitting { 1, accepted_tx[0][1]?, storePacket(0, PK_ACCEPTED, 0, 1), t := 0 } |
| 152 | CommandClient(0).WaitAck->CommandClient(0).Failed { x >= ACK_TIMEOUT && retries == MAX_RETRY, tau, cmdFailed[id][current] := true } |

