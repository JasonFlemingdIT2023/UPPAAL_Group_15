# Three-drone Prepared-to-Done proof

The goal is to establish `Supervisor.Prepared --> Supervisor.Done` under ACK priority with three drones, three mission items each, heartbeat period 20, service time 1–3, ACK timeout 14, up to two retries and no packet loss.

## Two machine checks

| Check | Model | Query and output | Method and verdict |
| --- | --- | --- | --- |
| Prepared boundary | [XML](../../code/models/n3_dmax3_timeout14_scheduler_ack_priority.xml) | [Query](../../code/queries/PreparedBoundary.q) · [Log](prepared_boundary_verdict.txt) | Full-model safety check with conservative over-approximation, satisfied. |
| Universal continuation | [XML](../../code/models/prepared_continuation.xml) | [Query](../../code/queries/ContinuationDone.q) · [Log](prepared_continuation_verdict.txt) | Exact compact DBM verification, `A<> Supervisor.Done` satisfied. |

The full-model check establishes that at Prepared, all mission senders and receivers have finished, all upload and installation flags are true, and command components are idle with neither ARM nor START dispatched. The link is idle, in the zero-time Delivered state, or transmitting a heartbeat. Each heartbeat sender is Waiting or Pending. The E06 P34 witness passes through Prepared and reaches Done. [Audit result](../analysis/completion_proof.json)

## State coverage

In the proof model, each heartbeat clock can be reset independently during a 20-unit initialization window. At entry to Prepared, the three clock values can independently take any real value in [0,20]. A sender already Pending in the full model maps to clock value 20 followed by an immediate Waiting → Pending transition. Its old clock value has no effect while pending and is reset on admission.

At initialization, the proof link can be idle or carry one heartbeat from any drone with residual service in [0,3]. Delivered in the full model returns to Idle in zero time through a committed location. The original rules process every subsequent packet.

MissionSender.Done and MissionReceiver.Uploaded have no outgoing edges. The old command-client clock is reset on first command admission. Both connection-monitor locations accept heartbeats, and the monitor clock and seen flags only record reception. The next admission overwrites the idle link's old packet. These values can be omitted or reconstructed while the original command, ACK admission, heartbeat and supervisor transitions continue to apply.

Take any reachable Prepared state in the full model. The first check places it within the stated boundary. The mapping gives a corresponding proof-model execution for each of its continuations. The second check shows that every proof-model execution reaches Done. Every full-model continuation from this Prepared state therefore reaches Done, and the argument applies to every reachable Prepared state.

## Reproduction

Run from the E06 directory.

```powershell
python code/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python code/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
```

The direct full-model check was stopped after about 814 seconds. The passive timer checks for a candidate completion deadline returned MAY NOT and timeout. The proof establishes eventual completion. [Supplementary run index](../analysis/completion_proof.json) · [Direct-query records](../records.csv)
