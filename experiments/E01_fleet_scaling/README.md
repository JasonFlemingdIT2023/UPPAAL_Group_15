# E01: fleet scaling

Executed 25 November 2026 for Chen's experiments, with Codex assistance. Human review pending.

## Controlled change

Source: models/08_final_version.xml at commit 2ecefd2, SHA-256 77896d59a2282f817786b7712f0d4372432fce73bc54a6bbed32500f3c40744d. The source remains unchanged.

N varies over 1,2,3,4. All configurations keep MISSION_SIZE=3, D_MIN=1, D_MAX=3, ACK_TIMEOUT=14, MAX_RETRY=2, LOSSY=false and inactive heartbeats. Copies change N and explicitly generate N MissionSender/MissionReceiver instances and the system list. Parameterized CommandClient/CommandServer templates instantiate for the bounded drone_id domain. All template bodies are asserted unchanged, and declaration differences are restricted to N.

Inherited embedded queries contain fixed indices and inactive-heartbeat checks. The copies replace them with one safe GUI starter query. Actual experiments use external per-configuration queries.q. P14 is expanded over every actual receiver; P23 checks retry counters of every active command client. Thus a one-drone model never references Drone1/Drone2 and a four-drone integrity check includes Drone3. P15 already quantifies over all drone IDs and command types.

## Scope and results

Each of four sizes runs P01-P09, P13-P16 and P23: 14 properties. Three serial repetitions give 168 formal checks. The diagnostic N=4 P17 witness is separate (169 completed invocations total). All formal checks complete under 120 seconds and an 8-GiB sampled RSS budget per query. Three repetitions agree on truth values and explored/stored counts; N=3 agrees with all 13 overlapping baseline properties.

No retransmission-counter increment is reachable at N=1 or N=2. At N=3 and N=4 it is reachable, but neither client 0 nor any fleet member can exhaust retries under these reference assumptions. Successful coordination is reachable for all four sizes. No claim is made for N>4 or for loss/heartbeat configurations.

## Measurement

UPPAAL 5.1.0-beta6 B2736CEEF00F5237; executable path/hash and host metadata in manifests. Python invokes the native verifier, rather than deciding correctness itself. Use the same exhaustive symbolic BFS, compact DBM, conservative reduction, automatic extrapolation and seed 1 as prior experiments. No diagnostic trace during performance measurements or cross-query state reuse; each invocation starts a fresh process.

Three repetitions are used for cost ranges, not success probabilities. Wall time includes process startup/license overhead and 50-ms polling granularity. N=1 P01, the first invocation of every batch, has conspicuously higher overhead; do not interpret its drop at N=2 as a model speedup. CPU user time is separately available, with coarse timer resolution (0 ms is not zero work). RSS is sampled every 50 ms and is a lower bound on peak; report it as sampled RSS. Reported resident memory is kept separately. Liveness summary counts/CPU/resident values are omitted per verifyta's warning; P06/P16 have wall time and sampled RSS only.

States are query-specific symbolic exploration/storage statistics, not a physical network metric or a general formula for the entire model state space. The plot uses medians and min-max bands for wall time/RSS; identical counts are plotted directly. No asymptotic complexity fit is claimed from four sizes.

## Reproduce (repository root, PowerShell)

```powershell
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E01 --repetition 1
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E01 --repetition 2
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E01 --repetition 3
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E01 --drones 4 --trace --properties P17
python scripts/summarize_E01.py
```

Each run gets a new timestamped folder. The summarizer uses the fixed evidence set below; explicitly update it to analyze newly generated runs. To inspect manually, open a saved model.xml and use its sibling queries.q or this folder's matching queries_nN.q.

## Evidence index (under results/coordination)

| Folder | Contents |
|---|---|
| 20261125T131340771891Z_E01 | Repetition 1: 56 checks |
| 20261125T131410593895Z_E01 | Repetition 2: 56 checks |
| 20261125T131448881664Z_E01 | Repetition 3: 56 checks |
| 20261125T131521932777Z_E01 | N=4 P17 diagnostic witness |
| analysis_E01 | Audited JSON, aggregated metrics, PNG/SVG cost figure, parsed trace and event table |

The initial 20261125T131300341037Z_E01 attempt failed with a tool error on a generated empty queries section; the final generator uses a safe embedded starter query. That failed attempt is retained and excluded from study results. ASCII temporary staging is retained for the native Windows verifier's Unicode-path limitation.

Checks: generated fleet sizes and query coverage tested; all nine old E02 model copies and four old E03 modes remain byte-identical when regenerated; all study source/model/query/runner hashes and raw verdicts audited. See ../../docs/experiment_results_E01.md for interpretation. E05 heartbeat and optional E04 remain pending.
