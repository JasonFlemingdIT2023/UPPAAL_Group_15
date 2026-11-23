# Bug and Event Record

## Logs

18.11.2026 - Jason
Version: 02_drone_extended_missionController
Event: In the Network Link on the transfer edge messageKind == 2 for transfering mission items. Because of a typo the initilization on the update part of the edge, I typed sequence 0 instead of sequence = s, whioch produces a deadlock. A drone can frist request mission item number 0, burt after it rquests number 1, it will turn into zero again and send the correspn ding item the link already transfered, leading to the receiverDrone waiting for a never receiving item_rx[d][1]?.

22.11.2026 - Jason
Version: 04_heartbeat_protocol_v1
Event: After adding heartbeat traffic to the old shared network, checking E<> CommandClient(0).Failed took over 300 seconds and explored around one million states. Screenshots available in results folder under pictures. The additional clocks, recurring messages and possible transmission orders increase the state space. The long execution alone does not establish whether command failure is reachable. Possible experiment: compare verification time and results with heartbeats enabled/disabled and with one, two and three drones to investigate state-space growth and whether heartbeat contention can cause command timeouts.

23.11.2026 - Jason
Version: 06B_simple_integration.xml
Event: Verification was much slower with recurring heartbeat traffic than in the same model with heartbeat activity removed. The exact query, settings and result should be recorded for a reproducible timing comparison. Heartbeats add independent clocks, pending states and competing transmissions. They can also interact with command timeouts and retries. The trace in report/Trace.xtr reaches Supervisor.Done and continues with heartbeat activity afterwards. Infinite heartbeat activity does not itself imply that symbolic verification cannot terminate. An interrupted search has an unknown result, not a failed property. A no-heartbeat configuration is useful as a comparison and for isolating mission/command behaviour, but cannot establish guarantees about heartbeat freshness or the full traffic load. Next experiment: compare continuous heartbeats with a finite-preparation configuration that stops new generation at Done or Aborted while draining pending messages. Keep network and protocol parameters unchanged and record query results, runtime and explored states.

23.11.2026 - Jason
Version: 08_final_version.xml
Event: Fixed acknowledgement handling in CommandClient.Sending. Previously, its self-loops discarded every accepted or denied ACK, including a valid reply to the current command arriving after a timeout while a retry was waiting to be sent. I added Sending -> Idle transitions that record cmdAccepted or cmdDenied for the current command and restricted the discard loops with c != current. This lets a delayed result finish the current exchange instead of causing an unnecessary retransmission, while acknowledgements for other commands are still ignored. The transitions were inspected in the model; this entry does not claim a new verification result.
