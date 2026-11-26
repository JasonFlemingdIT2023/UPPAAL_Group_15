# E05 Heartbeat traffic

With heartbeat enabled, original scheduling admitted a three-drone confirmation failure on a reliable link. Success also remained reachable. For one and two drones with heartbeat, P08 excluded confirmation failure for drone 0.

## Design and paired results

For N=1, 2 and 3, we paired models built from the same version 08 source by enabling or disabling heartbeat sender and receiver processes. Service times of 1–3, ACK timeout 14, up to two retransmissions, and no packet loss were fixed. The period is 20 and restarts at each heartbeat admission. In addition to P01, P03 and P08, P24 checks whether a state exists in which at least one heartbeat from every drone has been received.

![Heartbeat activation and verification cost](results/figs/E05_activation.png)

The upper-left panel shows final property verdicts. Asterisks mark the three properties resolved after the initial timeouts. The three cost panels retain the original BFS measurements with a 120 s, 8 GiB budget. They show the cutoff and the memory measured at that point for P03 with three drones and heartbeat enabled.

## Failure witness

In the three-drone witness, START0 entered the link at t=110 and arrived at t=113. Heartbeats, other commands and retransmissions took subsequent link slots. At t=150, ACK0 gained admission and the server executed START. At t=152, the client entered Failed while ACK0 was still in transit and the supervisor was in Starting. [Trace events](results/analysis/traffic_traces.md)

![Confirmation failure under heartbeat contention](results/figs/E05_failure_timeline.png)

## Verification cost and parameter controls

For N=2, P03 explored 53,314 states with heartbeat, about 92.6 times the 576 states with heartbeat disabled. Period 40 increased this to 124,082. Staggered first releases gave 49,460 explored states, with stored states increasing from 24,687 to 26,697. Period and release phase changed symbolic timing interleavings while query verdicts agreed across all three settings. Staggering changes the first release only. Each sender subsequently restarts its timer at its own admission.

![Heartbeat period and first-release offset](results/figs/E05_settings.png)

## Three-drone heartbeat follow-up

We reran P01, P03 and P08 using byte-identical models and queries and the original BFS options. Each of the three concurrent searches had a 600 s time limit and a 2 GiB sampled RSS cap. All three reached the memory cap first. The table gives the stop reason and the evidence for each final property verdict. [Follow-up records](results/analysis/activation_followup.json)

| Query | Extended BFS | Final verdict | Decisive evidence |
| --- | --- | --- | --- |
| P01 Success reachable | memory cap | TRUE | exact DFS witness to Done |
| P03 START requires ARM | memory cap | TRUE | E06 conservative proof on the identical model |
| P08 Drone 0 confirmation failure reachable | memory cap | TRUE | exact DFS witness to Failed |

The P01 and P08 witnesses show different executions. Some schedules complete fleet coordination, while others exhaust the retries for drone 0. P03 checks the prerequisite across all executions. The E06 safety proof on the same model establishes this property. [Per-query results](results/records.csv) · [P03 verifier output](results/analysis/P03_conservative_proof.txt)
