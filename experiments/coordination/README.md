# Baseline and E02 execution package

Executed on 24 November 2026 for Chen's experiments and analysis work, with Codex assistance.

## Scope

Reference: `models/08_final_version.xml` at Git `2ecefd273fa74ad147060c31bc5d48424331fdfe`.
Source SHA-256: `77896d59a2282f817786b7712f0d4372432fce73bc54a6bbed32500f3c40744d`.
The source model is unchanged. Only D_MAX and ACK_TIMEOUT declarations change in E02 copies; the generator asserts identical templates, system composition and embedded queries.

N=3, MISSION_SIZE=3, D_MIN=1, MAX_RETRY=2, LOSSY=false, heartbeat inactive. Base D_MAX=3 and ACK_TIMEOUT=14. E02 uses all nine combinations of D_MAX={2,3,5} and ACK_TIMEOUT={6,14,24}. See `configurations.json`.

P01-P12 follow the group plan. P13 checks actual started states at Done; P14 checks all three confirmed missions; P15 checks ARM/START failure on any drone; P16 checks eventual outcome after Prepared; P17 asks whether an ARM acceptance can coexist with a positive retry counter for that ARM operation. `properties.q` is the exported GUI-readable suite; the named formulas in the runner are its generation source. Any formula change requires regenerating this file and new evidence.

P09 counts a timeout-triggered transition into Sending, not necessarily a transmitted retry. In the observed P17 witness, a late ACK arrives before another transmission starts. P11 is a state observation and does not establish permanent non-execution. A P08/P15 satisfied result means failure is possible, not a successful safety check.

## Environment and measurement

- UPPAAL 5.1.0-beta6, revision B2736CEEF00F5237 (October 2026). The locally installed 5.0.0 failed license preflight (`Error 422: missing device`); its results are not mixed into this study.
- Windows, Intel Core i9-14900HX, approximately 32 GiB physical RAM. Actual platform, memory and executable hash are stored in each manifest.
- Python dependencies: psutil for monitoring, matplotlib for figures. No spreadsheet authoring dependency is needed.
- Sequential queries, exhaustive symbolic exploration, breadth-first search, compact DBM, conservative space optimization, automatic extrapolation, fixed seed 1, no cross-query state reuse.
- Formal measurement: no diagnostic trace, 120 seconds and 8 GiB sampled RSS limit per query. E02 has three repetitions; the baseline has one.
- Wall time includes executable startup/license overhead and up to one polling interval (50 ms). Verifier CPU user time is extracted separately when available. These small runs are not evidence of meaningful speed differences.
- Sampled RSS is a lower bound on peak process resident memory, not exact peak allocation. Reported resident memory is kept separately. Missing metrics remain null. `verifyta -u` warns that liveness summaries are incorrect; state counts/CPU/resident summary values for leads-to properties are not used.
- Diagnostic runs are separate, excluded from performance comparisons. Text traces are preserved in stdout.log. The beta's `-X` export returned nonzero and a zero-byte XML file; those attempts are marked tool_error, excluded from conclusions, and retained for audit.
- Native verifyta rejected Unicode paths. The runner copies byte-identical inputs into an ASCII temporary directory, checks their hashes, invokes the verifier there, and archives logs under the repository. No credentials are copied into the experiment package.

## Reproduce from repository root (PowerShell)

```powershell
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite baseline --properties P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 P11 P12 P13 P14 P15 P16
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E02 --repetition 1
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E02 --repetition 2
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite E02 --repetition 3
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite pilot --trace --properties P17
python scripts/run_coordination_experiments.py --verifyta 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe' --suite pilot --trace --dmax 5 --ack-timeout 14 --properties P08
```

Each invocation creates a new timestamped folder and never overwrites prior runs. `summary.csv` is an intermediate convenience table; per-query JSON, exact query, raw logs, command, actual model and run manifest provide the evidence. Runner snapshots preserve executed code. The initial failed Unicode-path pilot predates snapshot support and is not scientific evidence.

The analysis script is bound to this first study's evidence set. Run `python scripts/summarize_coordination_experiments.py` to audit and regenerate its plots. Before including new repetitions, explicitly select a new evidence set; its three-repetition assertion prevents silently pooling additional runs.

## Evidence index

Under `results/coordination/`:

| Folder | Purpose |
|---|---|
| `20261124T073157336815Z_baseline` | Baseline P01-P16, 16 invocations |
| `20261124T073241323529Z_E02` | E02 repetition 1, 72 invocations |
| `20261124T073436212851Z_E02` | E02 repetition 2, 72 invocations |
| `20261124T073532193363Z_E02` | E02 repetition 3, 72 invocations |
| `20261124T073418861392Z_pilot` | Baseline P01 success and P09 retry-trigger witnesses |
| `20261124T073421895292Z_pilot` | D_MAX=5, timeout=14, P08 failure witness |
| `20261124T073644478957Z_pilot` | Baseline P17 late-ACK witness |
| `20261124T073646154114Z_pilot` | D_MAX=5, timeout=14, additional P10 check |
| `analysis` | Audited records, matrix, parsed trace events, PNG and SVG figures |

## Remaining work

Update 25 November 2026: E03 is now completed separately; see `../E03_loss_location/README.md` and `../../docs/experiment_results_E03.md`. The following paragraph records the scope of this original baseline/E02 package.

E03 loss-location variants, E01 fleet scaling, E05 matched heartbeat experiments, and optional E04 bounded loss have not been run by this package. E02 has P01-P05/P08/P09/P15 throughout; the other baseline properties must not be reported as verified for every E02 configuration.
