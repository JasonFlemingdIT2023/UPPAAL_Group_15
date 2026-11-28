# E03: loss location

Executed 25 November 2026, Chen's experiments with Codex assistance. Human review pending.

## Question and controls

Can confirmation failure correspond to different actual drone states depending on which messages can be lost? Use the unchanged 08 reference at Git 2ecefd2, N=3, MISSION_SIZE=3, D_MIN=1, D_MAX=3, ACK_TIMEOUT=14, MAX_RETRY=2, no heartbeat. The four environments are reliable, request-only loss, reply-only loss, and both. No probability or fairness is added.

In generated copies only, replace the LOSSY declaration with DROP_COMMANDS and DROP_ACKS and replace the sole loss guard. All other declarations, templates and composition remain unchanged. The generator reverses these exact changes and asserts identical baseline text. Loss still occupies the link and requires t>=D_MIN; mission traffic cannot be lost. The source model is read-only.

Additional control: the original single switch set to LOSSY=true is tested against the split both-enabled case for P01-P21. Matching query results are a regression check, not a general equivalence proof. The split reliable mode agrees with all 16 archived baseline results.

## Queries and interpretation

P01-P17 retain earlier definitions. P18 requires Supervisor.Aborted, Link.Idle, client 0 Failed, other clients Idle, all servers Idle, ARM failure on drone 0 and armed[0]=false. In this one-shot, no-heartbeat scenario it establishes a reachable settled outcome without pending command work. It is stronger than P11's instantaneous unarmed observation, but specifically requires other clients Idle (it does not enumerate every possible terminal arrangement).

P19/P20 check eligible loss kinds; P21 excludes mission loss. P22 checks `(cmdFailed[0][ARM] && !armed[0]) --> armed[0]`. For reliable mode P22 is vacuous because P11 is unreachable. For reply-only mode P11 is reachable and P22 is satisfied, so eventual execution is a non-vacuous finding. In request/both modes P22 is false.

`queries.q` contains the 22 named formulas. The initial main run has P01-P21 (84 checks); P22 was added after inspecting the surprising reply-only P11 result (4 additional checks). This is a documented follow-up, not a preregistered hypothesis.

## Execution

Python generates XML/query copies and invokes the actual native UPPAAL executable via subprocess. UPPAAL 5.1.0-beta6 B2736CEEF00F5237 evaluates the symbolic queries. Python does not simulate or decide correctness. No GUI clicks are needed for batch runs.

The previous measurement protocol remains: exhaustive symbolic BFS, compact DBM, conservative reduction, automatic extrapolation, seed 1, sequential runs, 120-second/8-GiB sampled RSS limits. One run per configuration/property; no statistical runtime comparison is claimed. Liveness state summaries are omitted because the tool warns they are unreliable. Chinese repository paths are staged as byte-identical inputs in ASCII temporary directories. Text diagnostic traces are generated separately with `-t 0`.

```powershell
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E03
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E03 --loss-mode legacy_both --properties P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 P11 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E03 --loss-mode request --trace --properties P18 P10
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E03 --loss-mode reply --trace --properties P10 P11
python scripts/summarize_E03.py
```

The current default main suite includes P22 in the same invocation. Archived results retain the original split runs. The summarizer uses a fixed evidence list; change it explicitly to analyze a new study. Each run archives runner snapshot, manifest, generated models, individual queries, commands, stdout/stderr and result JSON.

## Evidence

All paths below are under results/coordination:

| Run | Evidence |
|---|---|
| 20261125T125634385990Z_E03 | Four modes x P01-P21: 84 checks |
| 20261125T125747351623Z_E03 | Four modes x P22: 4 checks |
| 20261125T125752125349Z_E03 | Original LOSSY=true x P01-P21: 21 control checks |
| 20261125T125832488306Z_E03 | Request-only P18/P10 witnesses |
| 20261125T125833850233Z_E03 | Reply-only P10/P11 witnesses |
| analysis_E03 | Audited records, outcome plot (PNG/SVG), trace event JSON and table |

All 113 invocations completed. The initial 20261125T125610475763Z_E03 directory contains an aborted generation attempt: an XML escaping assertion stopped before any verifier query; it is not evidence and is excluded. The final generator handles XML's escaped greater-than sign. No old results were overwritten.

Results and mechanism interpretation: ../../docs/experiment_results_E03.md. E01, E05 and optional E04 remain pending.
