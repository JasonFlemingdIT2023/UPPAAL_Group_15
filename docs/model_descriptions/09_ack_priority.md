# 09 — ACK-priority experiment candidate

`models/09_ack_priority.xml` is the E06 scheduling improvement built from version 08 with three drones and heartbeat enabled. It retains D_MIN=1, D_MAX=3, ACK_TIMEOUT=14 and MAX_RETRY=2.

`ackPending[i]` mirrors CommandServer(i).Decide. An arriving command sets it, and either ACK admission clears it. Every non-command-ACK network admission requires all pending flags to be false. Accepted and denied command replies retain their admission paths. In-flight transmission remains non-preemptive.

The embedded queries cover reply exhaustion, retry activity, a six-unit post-admission reply bound, heartbeat admission progress and phase completion. P35/P36/P37 and heartbeat progress are proved for N=3 using decisive conservative over-approximation; exact witnesses demonstrate successful coordination and an ACK delivered at the six-unit bound. On 26 November, P25 (Prepared inevitably Done) was established for this N=3 configuration by a verified Prepared-boundary invariant, an exact universal-completion check on a continuation abstraction, and the documented state-coverage argument. See the [completion proof](../experiment_results_E06_completion.md). This is a compositional result; it does not replace the historical timeout records of the direct full-model query.

See [E06 results](../experiment_results_E06.md) and [experiment package](../../experiments/E06_ack_priority/README.md). Version 08 remains the historical experiment reference.
