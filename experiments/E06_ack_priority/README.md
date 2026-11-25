# E06 — ACK-priority scheduling improvement

Date: 25 November 2026; completion proof added 26 November. Reference: current `models/08_final_version.xml`. GUI candidate: `models/09_ack_priority.xml`.

## Controlled change

When the shared link becomes idle, a pending command reply (accepted or denied ACK) takes precedence over heartbeats, new command requests and mission traffic. An in-flight packet finishes normally. The priority rule does not order ACKs among themselves.

Implementation:

1. Global `bool ackPending[N]` starts false.
2. CommandServer sets its flag when a command is delivered and it enters Decide; it clears the flag when sending either reply and returning to Idle. Duplicate-request self-loops keep the flag set.
3. Six non-command-ACK admission edges in PacketNetwork gain `forall (i : drone_id) !ackPending[i]`. The accepted/denied reply admission edges keep their original guards.

P29 verifies that each flag equals its server's Decide location. An additional `observed` variant updates the same flags but adds no admission guards; its ten N=2 checks validate the bookkeeping independently. The structural audit reverses exactly these changes and recovers the original model's semantics.

All experiment models use HB_PERIOD=20, D_MIN=1, D_MAX=3, ACK_TIMEOUT=14, MAX_RETRY=2, no loss and three mission items per drone. N=1,2 provide exact controls; N=3 reproduces the E05 problem. Original variants match the E05 input bytes. Command, mission, heartbeat and supervisor logic otherwise remain as in version 08, including late-ACK handling and the execution effect on reply admission.

## Queries

| ID | Question |
|---|---|
| P35 | Does every drone avoid retry exhaustion? `A[] forall(i:drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])` |
| P36 | Are all clients' retry counters always zero? |
| P37 | While a client waits for its reply, is its admission timer at most `2*D_MAX`? |
| P29 | Do pending flags exactly match CommandServer.Decide? |
| P30/P31/P32 | Does each drone's pending heartbeat eventually obtain link admission? |
| P34 | Is Done reachable with every heartbeat observed? |
| P38 | Can START0's ACK be delivered exactly `2*D_MAX` after command admission? |
| P25 | Does Prepared inevitably reach Done? |
| P39–P44 | Decomposed client/phase progress checks |

P02–P07, P13 and P14 cover prerequisites, success evidence, deadlock, admitted-packet progress, service timing and mission integrity. `queries_n3.q` mirrors the convenient query list embedded in the GUI candidate.

## Verification methods

The original 100-record study ran sequentially with per-query 120-second/8-GiB limits. Exact checks use compact DBM or DBM with recorded extrapolation/search settings. N=3 exhaustive safety/liveness searches reached their budgets; convex-hull over-approximation (`--state-representation 3`) completed the safety and heartbeat-progress checks. The 26 November supplement uses separate limits and evidence; auxiliary checks may overlap the extended direct query.

The over-approximation contains additional behaviors. A definite satisfied invariant proves the invariant for the original model; an approximation result containing MAY/MAY NOT is recorded as `maybe`, not true or false. See [UPPAAL's explanation of definite invariant proofs](https://uppaal.org/benchmarks/) and [verifier result semantics](https://docs.uppaal.org/gui-reference/verifier/verifying/). Concrete success/failure witnesses use exact state representations.

N=3 ACK-priority P35, P36, P37, P29, P02–P07, P13/P14 and P30–P32 are definitively satisfied. P34/P38 have exact witnesses. P25 was unresolved in the initial direct attempts: two exact attempts timed out, and the approximation returned MAY NOT. Its decomposed checks P39–P43 also returned MAY NOT; P44 was satisfied. N=1,2 P25 is satisfied with exact verification.

On 26 November, N=3 P25 was established by a compositional proof. A full-model invariant verifies the Prepared boundary. An exact check of `A<> Supervisor.Done` then passes on a proof copy covering arbitrary heartbeat ages in [0,20], pending heartbeats, and an optional heartbeat with 0..3 residual transmission time. All original post-boundary protocol edges are retained. The state-coverage argument is in [the completion note](../../docs/experiment_results_E06_completion.md), with fixed runs in `completion_evidence.json`. These records are separate from the original 100 invocations. Neither production model was changed.

## Execution and evidence

`evidence.json` fixes 100 analyzed invocation records: 87 definite answers (73 satisfied, 14 not satisfied), three timeouts and ten approximation results marked maybe. XML-generation/parser development attempts and one unfinished query are listed separately. The evidence keeps each run's source/query hashes, actual generated model, command, raw logs, limits, metrics and runner snapshot.

The audit checks verdict text, method settings, hashes, input regeneration, original E05 identity, flag invariants, passive-control verdicts and the six-edge priority transformation. Forty-three prior E01–E05 configurations were also checked for byte-identical generation. The original version 08 file is unchanged.

## Reproduce selected checks

From the repository root in PowerShell:

```powershell
$verifier = 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe'
# Definite N=3 safety and reply-bound proofs
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E06 --scheduler ack_priority --drones 3 --state-representation 3 --properties P35 P36 P37 P29 P03
# Each heartbeat progresses; admitted packets leave; no pre-outcome deadlock
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E06 --scheduler ack_priority --drones 3 --state-representation 3 --properties P30 P31 P32 P06 P05
# Exact success and tight reply-bound witnesses
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E06 --scheduler ack_priority --drones 3 --search-order 1 --trace --properties P34 P38
# Original model's concrete counterexamples
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E06 --scheduler original --drones 3 --search-order 1 --trace --properties P35 P36 P37 P25
# Audit fixed evidence, regenerate plots and export the GUI candidate
python scripts/summarize_E06.py
# Prepared-boundary proof and exact universal continuation proof
python scripts/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python scripts/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
python scripts/summarize_E06_completion_proof.py
```

`run_E06_followups.py` contains the executed small-scale comparisons, passive control and witness batch. The later progress-decomposition and counterexample runs are explicitly listed in `evidence.json`. New runs receive new directories; select new evidence deliberately before regenerating an updated study.

## Open in UPPAAL

Open `models/09_ack_priority.xml`; the three heartbeat senders/monitors are active. The embedded comments identify P35/P36/P37 and the heartbeat progress checks. In the verifier's Options menu, choose **State Space Representation → Over Approximation** for the N=3 safety and heartbeat-progress proofs. Use an exact representation and depth-first search for concrete P34 witnesses. P25 is established through the supplemental compositional proof; the unchanged embedded full-model query can still be computationally expensive.

The exported model differs from the verified N=3 priority model only in embedded query list and guard-label positions. `analysis_E06/gui_model_audit.json` records that semantic-equivalence check. The results note is `docs/experiment_results_E06.md`.
