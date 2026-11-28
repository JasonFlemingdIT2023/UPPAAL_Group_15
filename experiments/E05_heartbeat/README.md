# E05 — Heartbeat traffic and verification cost

Source: `models/08_final_version.xml`; generated experiment copies retain the final command-client late-ACK fix. Python orchestrates real UPPAAL `verifyta` invocations; it does not simulate or replace the timed-automata verifier.

## Question and controlled changes

Does enabling the existing heartbeat sender/monitor change command outcomes or the effort required to verify them? Hypothesis: extra recurring concurrent processes may substantially increase symbolic-state exploration, even where selected command properties retain their truth values.

Activation ablation: N=1,2,3, heartbeat inactive/active, period=20. Each pair differs **only** by adding `HBSender, ConnectionMonitor` to the system composition. All clocks initially zero. Each template is automatically instantiated for every `drone_id`.

Controls: 3 mission items per drone; D_MIN=1, D_MAX=3; ACK_TIMEOUT=14; MAX_RETRY=2; LOSSY=false; same final-version templates, channels, shared one-slot network, query formulas and search options. Explicit mission instances are generated consistently with N. No FIFO, priority or fairness policy is added.

Settings supplements at N=2, heartbeat active:

| Setting | Period | First eligible times (drone 0,1) | Implementation |
|---|---:|---|---|
| Original | 20 | 20,20 | Existing sender |
| Longer period | 40 | 40,40 | Change HB_PERIOD only |
| Staggered first release | 20 | 20,30 | HBSender local bounded `firstOffset=id*HB_PERIOD/N`; add it to Waiting's invariant and release guard; clear it on first admission |

The staggered variant delays the first eligibility only; it does not enforce permanent phase separation. All variants reset `period` when admitted to the network. A Pending sender can wait for admission, so eligibility time is not a guaranteed transmit or receive time. These are self-timed sources, not fixed-rate sources with accumulating queues.

## Queries and limits

Four queries per configuration, also in `queries.q`:

- P01: successful coordination is reachable.
- P03: START never occurs before ARM.
- P08: drone 0 can exhaust retries and enter Failed. FALSE excludes that event; TRUE would demonstrate a possible failure.
- P24: there exists an execution where every drone's heartbeat has been seen. FALSE is the expected disabled-heartbeat control. TRUE is not a guarantee of recurring reception, bounded latency or fairness.

Formal runs use BFS (`-o 0`), `-s -u --state-representation 1 -S 1 -n 0 -r 1`, one invocation per configuration/query, 120 seconds and 8 GiB per invocation. Verifier processes run sequentially. Diagnostic runs enable `-t 0` and are recorded separately; any alternate search order is recorded explicitly and never pooled with BFS performance data.

Timeout/memory limit means unknown under the budget, never false. Partial searches do not provide complete reachable-state counts. Wall time includes launch/license overhead. RSS is sampled every 50 ms and is a lower bound on the true peak. Single observations are not runtime distributions or robust performance ratios.

## Reproduction and evidence

Run from the repository root in PowerShell:

```powershell
$verifier = 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe'
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 2 --heartbeat active --hb-period 40
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 2 --heartbeat active --hb-offsets staggered
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 2 --heartbeat active --properties P01 --trace
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 2 --heartbeat active --hb-offsets staggered --properties P24 --trace
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 3 --heartbeat active --properties P01 P08 --search-order 1 --trace
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E05 --drones 3 --heartbeat active --properties P03 --search-order 1
python scripts/summarize_E05.py
```

`evidence.json` fixes the exact runs used for this report; reruns receive fresh run directories and require an intentional evidence-index update. Every result stores actual model/query copies, hashes, tool version, command, stdout/stderr, limits, metrics and an immutable runner snapshot. Non-ASCII workspace inputs are staged byte-identically in temporary ASCII directories for the Windows verifier.

The analysis audits hashes and raw verdicts, verifies the heartbeat toggle is the only difference within each activation pair, checks disabled models/verdicts against E01, and validates period/offset variants against the generator. The original source model remains unchanged. See `docs/experiment_results_E05.md` for measured results and interpretation.

Recorded execution: 32 BFS measurement invocations (29 resolved, 3 timeouts), four successful diagnostic invocations, and one DFS P03 control (timeout): 37 total, 33 resolved, four timeouts. All limits were enforced; there were no verifier errors or memory-limit stops. N=3 active P01/P08 are established true by DFS witnesses despite the BFS limits; P03 remains unknown under both search budgets.
