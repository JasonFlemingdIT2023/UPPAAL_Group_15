# E06: ACK-priority scheduling

2026-11-25; completion proof added on 2026-11-26. The study added ACK priority to the final model and verified it in UPPAAL. The improved model is [09_ack_priority.xml](../models/09_ack_priority.xml).

## Verified improvements

For the E05 configuration with three drones, heartbeat period 20, service time 1–3, ACK timeout 14, up to two retries and reliable delivery, ACK priority establishes that:

- No drone exhausts its retry budget while waiting for a reply.
- Every command client's retry counter remains zero.
- The reply wait after command admission is at most **six model time units**.
- Every pending heartbeat eventually gains admission.
- The checked mission integrity, ARM/START prerequisites, success evidence, admitted-packet progress and pre-outcome deadlock properties hold.

The rule removes the E05 failure mechanism in which heartbeats and retransmissions delay an ACK until retry exhaustion. Supplementary verification on 2026-11-26 also established Prepared→Done for three drones by checking the full-model boundary at Prepared and then exactly verifying a model covering its continuations. See the [completion proof](experiment_results_E06_completion.md).

## Model change

When the link is free, a pending command ACK is admitted before other traffic. With no ACK pending, other messages compete under the original rule. A packet already in service completes normally.

`ackPending[i]` records whether server i is in Decide. It is set on command reception and entry to Decide, then cleared when an acceptance or denial ACK is admitted. Six non-command-ACK admission edges require all pending flags to be false. P29 verifies agreement between the flags and server locations.

Mission, command, heartbeat and supervisor logic otherwise remains the same. ARM/START still executes when the server admits the acceptance ACK, so earlier ACK admission also advances that action.

## Comparison with original scheduling

Fixed settings are ACK_TIMEOUT=14, D_MIN=1, D_MAX=3, MAX_RETRY=2, HB_PERIOD=20, active heartbeats, reliable delivery and three mission items per drone.

| N | Policy | Retry exhaustion | Retry increment | Post-admission reply time ≤6 | Every pending heartbeat is admitted | Prepared leads to Done |
|---:|---|---|---|---|---|---|
| 1 | Original | Unreachable | Unreachable | False | True | True |
| 1 | ACK priority | Unreachable | Unreachable | True | True | True |
| 2 | Original | Unreachable | Reachable | False | True | True |
| 2 | ACK priority | Unreachable | Unreachable | True | True | True |
| 3 | Original | Reachable | Reachable | False | True, supplementary proof | False |
| 3 | ACK priority | Unreachable | Unreachable | True | True | True, supplementary compositional proof |

![Property comparison](../results/coordination/analysis_E06/E06_outcomes.png)

The one- and two-drone results use exact verification. Three-drone counterexamples for the original model come from exact search. The improved model's safety and heartbeat-progress checks return definite positive verdicts under conservative over-approximation. TRUE* marks the three-drone compositional completion proof; TRUE† marks heartbeat progress established from P06 and finite competing traffic.

A passive-flag control records `ackPending` without adding priority guards. At N=2, its nine shared properties agree with original scheduling, and flag consistency also holds. The checked behavioural improvement comes from the admission guards.

## Why the reply bound is six

A command takes at most three units after admission. On delivery, its ACK becomes pending. Other requests and heartbeats yield the next available slot to that ACK, which takes at most another three units.

The request/reply exchange therefore consists of command transmission followed by ACK transmission. The verified bound `2*D_MAX=6` is below timeout 14 and starts at command admission.

P37 bounds every client's clock in WaitAck by six. P06 checks eventual packet release, while P35/P36 exclude retry exhaustion and counter increments. P38 supplies a witness whose ACK arrives exactly at six, attaining the bound.

## Diagnostic traces

The comparison uses an original-policy failure trace and an improved-policy witness attaining six units. Each starts at drone 0's first START admission.

| Relative time | Original policy | ACK priority |
|---:|---|---|
| 0–3 | START0 request transmission | START0 request transmission |
| 3–6 | Heartbeats and other traffic occupy the link while the ACK waits | ACK0 transmission; reply received at 6 |
| 14 | First timeout and retransmission | Exchange already complete |
| 28 | Second timeout and retransmission | Exchange already complete |
| 40 | ACK0 finally gains admission | — |
| 42 | Client exhausts retries while ACK0 remains in flight | — |

![Reply-timing comparison](../results/coordination/analysis_E06/E06_reply_comparison.png)

The original trace reuses E05's recorded execution. The priority trace is a new UPPAAL witness. Complete events, model times and packet kinds are archived in the analysis directory. Both policies also admit a path reaching Supervisor.Done with all heartbeats observed.

## Verification method and completion

Exact exploration remains costly for the three-drone heartbeat model. Initial checks for absence of fleet-wide failure and Prepared→Done reached 120 s. Alternative exact state representations and extrapolations also left the direct completion query at its limit. The next checks used UPPAAL's conservative convex-hull over-approximation.

Over-approximation enlarges the checked behaviour set. A definite safety proof over that set applies to the original model. MAY/MAY NOT verdicts remain inconclusive, following [UPPAAL's approximation guidance](https://uppaal.org/benchmarks/) and [verdict documentation](https://docs.uppaal.org/gui-reference/verifier/verifying/).

The three-drone priority model receives definite positive verdicts for P02–P07, P13, P14, P29–P32 and P35–P37. On November 25, the over-approximate Prepared→Done verdict was MAY NOT. Separate command, ARM-stage and START-stage progress checks were also inconclusive, while Prepared→Arming was established. On November 26, the full Prepared boundary check and an exact `A<> Done` check on a continuation covering arbitrary heartbeat phases and an in-flight heartbeat established P25.

The November 25 analysis set retains **100 query records**: 87 definite verdicts, three timeouts and ten inconclusive over-approximate results. Queries then ran sequentially with 120 s and 8 GiB limits. November 26 proof checks and attempts have separate indexes; some ran concurrently with the extended full-model query. Model-generation and parser-debugging records are stored separately.

One matched P03 measurement under the same over-approximation settings gives:

| Three-drone model | Explored states | Stored states | Wall time (s) |
|---|---:|---:|---:|
| Original | 2,722,596 | 1,087,331 | 19.8023 |
| ACK priority | 318,619 | 267,941 | 1.5468 |

The original-policy P03 proof also settles E05's previously unknown safety result. These are single-run costs, including startup. ACK priority reduces explored states by 88.3% and stored states by 75.4%. The rule removes competing admissions ahead of pending ACKs and excludes the later behaviour caused by retries.

## Heartbeat progress under original scheduling

P30–P32 initially returned MAY NOT after about 0.13 s. Plain DBMs with LU extrapolation remained inconclusive. An extended compact-DBM P30 check with automatic extrapolation timed out at 600 s. Supplementary checks established eventual release of admitted packets (P06) and checked receivers for in-flight mission packets (P46). Urgent admission on an idle link, at most 60 non-heartbeat packets, and at least 20 units between each competing sender's heartbeat admissions imply that every pending heartbeat gains admission in finite time. See the [heartbeat-progress proof](../expriment_final/E06_ack_priority/results/proof/Original_heartbeat_progress.md).

## Deliverables and reproduction

- [Improved model for UPPAAL](../models/09_ack_priority.xml)
- [Settings, queries and reproduction commands](../experiments/E06_ack_priority/README.md)
- [Fixed evidence index](../experiments/E06_ack_priority/evidence.json)
- [Three-drone completion proof and supplementary evidence](experiment_results_E06_completion.md)
- [Trace event tables](../results/coordination/analysis_E06/trace_events.md)
- [Execution summary](../results/coordination/analysis_E06/execution_summary.json)

Audits checked raw-log verdicts, input hashes, all six guarded admission edges, flag updates and location consistency, and generation of 43 historical configurations. The deliverable differs from the verified three-drone priority variant only in the embedded query list and guard-label coordinates. The version 08 reference file remains unchanged.
