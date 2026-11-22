# Bug and Event Record

## Logs

18.11.2026 - Jason
Version: 02_drone_extended_missionController
Event: In the Network Link on the transfer edge messageKind == 2 for transfering mission items. Because of a typo the initilization on the update part of the edge, I typed sequence 0 instead of sequence = s, whioch produces a deadlock. A drone can frist request mission item number 0, burt after it rquests number 1, it will turn into zero again and send the correspn ding item the link already transfered, leading to the receiverDrone waiting for a never receiving item_rx[d][1]?.

22.11.2026 - Jason
Version: 04_heartbeat_protocol_v1
Event: After adding heartbeat traffic to the old shared network, checking E<> CommandClient(0).Failed took over 300 seconds and explored around one million states. Screenshots available in results folder under pictures. The additional clocks, recurring messages and possible transmission orders increase the state space. The long execution alone does not establish whether command failure is reachable. Possible experiment: compare verification time and results with heartbeats enabled/disabled and with one, two and three drones to investigate state-space growth and whether heartbeat contention can cause command timeouts.