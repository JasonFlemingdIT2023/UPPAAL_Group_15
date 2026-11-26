# E06 ACK-priority scheduling

With three drones and active heartbeat, ACK priority excluded the confirmation failure and timeout retries observed in E05 (P35, P36) and bounded the post-admission reply wait at six model time units (P37). Both policies guarantee eventual admission of pending heartbeats. Under original scheduling, contention can delay a command reply until retries are exhausted. The priority policy gives that reply the next available slot.

## Scheduling change

The comparison fixes three drones, three mission items per drone, a single link slot, service times of 1–3, heartbeat period 20, ACK timeout 14, up to two retries and no loss. A server sets `ackPending` on receiving a command and entering Decide, then clears it when an acceptance or denial ACK is admitted. With an ACK pending, heartbeat, mission and new command traffic wait for a free slot after the reply. The current packet completes normally. P29 confirms the flag matches Decide, and the two-drone passive flag control agrees with original scheduling on its nine shared checks.

## Verified effects

| Three-drone result | Original | ACK priority |
| --- | --- | --- |
| Any confirmation failure | Reachable | Unreachable |
| Reply wait ≤6 | Fails | Holds |
| Eventual admission of each pending heartbeat | Holds, follow-up proof | Holds |
| Prepared leads to Done | Fails | Holds |

![Properties under original and ACK-priority scheduling](results/figs/E06_outcomes.png)

When a command arrives, its pending ACK gets the next link slot. The command and reply each take at most three units, and the exact P38 witness attains six. Under original scheduling, the START0 witness retransmits at t=14 and t=28. Its ACK enters the link at t=40, and the client fails at t=42 while that ACK is still in transit. Each trace measures time from its own first START0 admission.

![Original failure and ACK-priority reply timeline](results/figs/E06_reply_comparison.png)

## State space and verification cost

Both three-drone models satisfied P03, which checks that START requires ARM, using breadth-first search and the same conservative convex-hull over-approximation.

| P03 Metric | Original | ACK priority | Reduction |
| --- | ---: | ---: | ---: |
| Explored states | 2,722,596 | 318,619 | 88.3% |
| Stored states | 1,087,331 | 267,941 | 75.4% |
| Verification wall time | 19.80 s | 1.55 s | 92.2% |

Original scheduling allows varying numbers of heartbeats, retransmissions and other requests to interleave between a request and its reply. Priority removes branches in which those packets would take the next slot while an ACK is pending. The P03 search visited fewer states. The table reports the search counts and one wall-time measurement for the matched P03 checks. [Per-query results](results/records.csv)

## Heartbeat progress under original scheduling

P30–P32 ask whether each drone's heartbeat eventually gains admission after entering Pending. The initial over-approximate checks returned `MAY NOT` after roughly 0.13 s each. Plain DBMs with LU extrapolation also returned `MAY NOT`. The P30 run with exact state representation and automatic extrapolation reached its 600 s limit. A supplementary check proved P06 on the same original-scheduling model: every in-flight packet eventually releases the link. The heartbeat period and the finite volume of other traffic then establish eventual pending-heartbeat admission for each of the three drones.

While the target heartbeat is pending, urgent synchronization prevents idle waiting on a free link. At most 60 mission and command packets can be admitted. Each of the other two drones spaces its heartbeat admissions by at least 20 units, and a packet occupies the link for at most three units. Even a scheduler that chooses competing packets first at every opportunity cannot keep the link occupied indefinitely. The packet and time bounds give a conservative upper bound of 270 model units. [Proof and verifier output](results/proof/Original_heartbeat_progress.md)

## Command-phase completion

The three-drone Prepared-to-Done claim follows from two checks. The full model verifies that mission upload is complete and commands have yet to begin at Prepared. The continuation model covers arbitrary heartbeat phases, pending heartbeats and a possible heartbeat already in flight. Its exact A<> Done check passed. The checks took about 8.36 and 2.89 seconds. The extended direct check of the full model was stopped at about 814 seconds before issuing a verdict. [State-coverage proof](results/proof/Prepared_to_Done.md)

The result establishes both a post-admission reply bound and completion of the command phase. It applies to the tested three-drone configuration with heartbeat period 20 and no packet loss. Done records receipt of every drone's START acceptance by the ground station. [Improved model](code/models/09_ack_priority.xml)

## Inconclusive runs

Several direct checks in the original study timed out or returned `MAY NOT`. An exact counterexample settled P35 under original scheduling, while the follow-up argument above settles P30–P32. The compositional proof settles P25 under ACK priority. The separate exploratory checks P39–P43 remain inconclusive in their original runs. The timer experiment for a 120-unit completion deadline under ACK priority also remains inconclusive.
