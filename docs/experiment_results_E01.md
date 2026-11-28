# E01: fleet-scaling results

2026-11-25. UPPAAL 5.1.0-beta6 verifyta supplied the verdicts. Python generated configurations, invoked the verifier, recorded and checked results, and plotted the figures. The original version 08 model was unchanged.

## Design and completion

The study compared N=1, 2, 3 and 4, with three mission items per drone, service time 1–3, ACK timeout 14, up to two retransmissions, no loss and inactive heartbeats. Mission sender/receiver instances and system composition were generated for each N. Mission-integrity and fleet-wide retry queries covered every instantiated drone.

Each size was checked against 14 properties: P01–P09, P13–P16 and P23. Three repetitions gave 168 formal checks, all completed within the 120 s and 8 GiB per-query limits. Verdicts and explored/stored state counts matched across repetitions. One additional N=4 P17 witness was generated separately from the performance measurements.

## Behavioural results

| N | Success reachable, P01 | Any drone can retry, P23 | Any drone can fail, P15 | Checked safety, integrity and progress properties |
|---:|---|---|---|---|
| 1 | Yes | No | No | Satisfied |
| 2 | Yes | No | No | Satisfied |
| 3 | Yes | Yes | No | Satisfied |
| 4 | Yes | Yes | No | Satisfied |

The final column covers P02–P07, P13, P14 and P16. P05 permits terminal states at Done/Aborted, P06 checks eventual release of admitted packets, and P16 starts from Prepared. P08 and P09, which concern drone 0, agree with the fleet-wide P15 and P23 verdicts.

At these settings, retry increments become possible at three drones, while retry exhaustion remains unreachable through four drones. The checked fleet sizes retain the specified coordination rules.

## Verification cost

For P05, which excludes deadlock before an outcome:

| N | Explored states | Stored states | Median wall time (s) | Median sampled peak RSS (MiB) |
|---:|---:|---:|---:|---:|
| 1 | 45 | 40 | 0.1326 | 14.05 |
| 2 | 576 | 481 | 0.1266 | 15.90 |
| 3 | 7,541 | 6,231 | 0.1236 | 16.74 |
| 4 | 112,482 | 92,776 | 0.7850 | 34.32 |

The P05 search grows by about 14.9 times from three to four drones under the selected verifier settings.

![E01 verification cost](../results/coordination/analysis_E01/E01_scaling.png)

P01, P05 and P08 represent success reachability, absence of pre-outcome deadlock and drone-0 failure reachability. Lines show medians over three repetitions and shading shows the minimum–maximum range. State counts are identical across repetitions.

For small models, startup, licence checks and polling account for much of the wall time. N=1 P01 is the first call in each batch and has a higher startup cost. P05 median user CPU times are 0, 0, 16 and 672 ms; zero values reflect timer resolution.

RSS is sampled every 50 ms and therefore bounds peak memory from below. The verifier warns about liveness statistics for P06/P16, so their explored/stored counts and CPU summaries are excluded from cost comparisons. Raw measurements remain in the logs.

## N=4 diagnostic trace

P17 requires drone 0 to have received ARM acceptance with a positive retry counter for that ARM exchange. The witness satisfies it. Time is relative to the first ARM admission:

| Model time | Event |
|---:|---|
| 0–3 | CMD0 occupies the link |
| 3–6 | CMD1 occupies the link |
| 6–9 | CMD2 occupies the link |
| 9–12 | CMD3 occupies the link |
| 12 | Drone 0 executes abstract ARM and ACK0 enters the link |
| 14 | The client takes its timeout edge, increments its retry counter and enters Sending |
| 14 | ACK0 arrives and is accepted on Sending→Idle |

The four consecutive requests place ACK0 delivery at the timeout boundary. Late-ACK handling allows the exchange to finish. There is no second CMD0 transmission in this trace; the reported retry outcome concerns reachability of a counter increment.

## Evidence and scope

See the [experiment package and commands](../experiments/E01_fleet_scaling/README.md), [trace event table](../results/coordination/analysis_E01/n4_retry_trace.md), and audit JSON under `results/coordination/analysis_E01`. Checks covered source/configuration models, queries, runner-snapshot hashes and raw-log verdicts. Thirteen overlapping N=3 properties agree with the existing reference results. Extending the runner left the E02/E03 generated models byte-identical.

An initially empty embedded query section caused one tool error, which remains archived outside the final results. Final experiment models include a GUI example query; verification uses the external `queries.q`. Other template transitions were unchanged.

The study covers N≤4 under the fixed reliable, heartbeat-off settings. The next planned comparison was E05, using heartbeat-on/off variants of the same source model.
