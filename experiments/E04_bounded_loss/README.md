# E04 — Retry limits under a global loss budget

Executed 25 November 2026 with UPPAAL 5.1.0-beta6. Python generates copies, invokes `verifyta`, records evidence and plots results; verification is performed by UPPAAL.

## Question and environment

Under a stronger communication assumption, do retries guarantee coordination after mission preparation, or only make success possible?

The environment may lose **at most K command-protocol transmissions over the entire coordination attempt**, counting all drones, both ARM/START, and both requests and accepted/denied replies together. K is not reset after delivery, a new command, a new drone or supervisor abort. Loss remains nondeterministic: it need not consume the budget. Mission traffic remains reliable.

The experimental copy starts from `models/08_final_version.xml`, keeps its delayed-ACK handling and unscheduled single-slot link, and sets:

- N=1, then N=3; K=0,1,2; MAX_RETRY=0,1,2: 18 configurations.
- D_MIN=1, D_MAX=3, ACK_TIMEOUT=24, MISSION_SIZE=3, heartbeat inactive.
- MAX_RETRY counts retransmissions after the initial transmission, and resets for each command exchange as in the source client.

The timeout is selected from E02's D_MAX=3/ACK_TIMEOUT=24 configuration, which had neither demonstrated retries nor timing-only failure. E04 additionally verifies all K=0/retry settings and compares them against uninstrumented reliable controls. The reference timeout 14 is deliberately tested separately as a sensitivity control.

## Exact model changes

Generated copies enable the original LOSSY switch, change the MAX_RETRY constant, add global constant `LOSS_BUDGET`, and add local `PacketNetwork.lossCount` with range `0..LOSS_BUDGET`, initialized to zero. Only the network's Transmitting→Lost edge changes:

```text
guard: lossCount < LOSS_BUDGET && LOSSY && t >= D_MIN
       && (packet.kind == PK_COMMAND || packet.kind == PK_ACCEPTED || packet.kind == PK_DENIED)
update: lossCount++
```

No client, server, mission or supervisor transition reads the counter. All other templates are unchanged; no priority, fairness, cancellation or new client algorithm is introduced. The counter enforces an environmental assumption, not a protocol feature that the client can use. K=0 disables this branch, including with the original LOSSY switch enabled.

The generator also builds the N-specific mission instances/system composition and a safe embedded GUI query; external `queries_n1.q` and `queries_n3.q` define the actual suite. The source file remains unchanged.

## Properties and scope

Main suite: P01–P08, P10–P16, P21, P25, P27, P28: 19 properties per configuration, 342 invocations. The following additions make the interpretation explicit:

| ID | Formula | Interpretation |
|---|---|---|
| P25 | `Supervisor.Prepared --> Supervisor.Done` | Every continuation from Prepared eventually succeeds; conditional on reaching the command phase |
| P26 | `A<> Supervisor.Done` | Unconditional eventual success from initialization; diagnostic control only |
| P27 | `A[] Link.lossCount <= LOSS_BUDGET` | Budget integrity regression; also independently audit counter placement/updates |
| P28 | `E<> (Supervisor.Done && Link.lossCount == LOSS_BUDGET)` | Successful execution consuming all allowed losses, avoiding a zero-loss-only success witness |

P01 establishes a successful execution exists, making the Prepared premise reachable. P15 covers any drone failure; P08/P10/P11 focus on drone 0. P16 checks eventual Done or Aborted after Prepared, separately from guaranteed success. No observed truth is a success probability. The tested R>=K pattern is not asserted for arbitrary fleet size, delay or heartbeat settings.

## Controls and evidence

- Unrestricted loss: N=1, R=0,1,2; P01/P08/P10/P11/P25: 15 checks.
- Uninstrumented reliable network: N=1,3, R=0,1,2; P01/P08/P15/P25: 24 checks. Verdicts match K=0.
- Timing control: N=3, K=0, R=0, timeout=14; P01/P08/P10/P15/P25: 5 checks.
- Six diagnostic invocations: unconditional success counterexamples for N=1,3; recovery after two losses; unexecuted ARM failure; executed ARM with lost ACK; timing-only failure.

Total: **392 completed invocations, no timeout, no memory-limit stop and no tool error**. Main and control measurements are separate from diagnostic traces. Each query uses BFS, `-s -u -o 0 --state-representation 1 -S 1 -n 0 -r 1`, a 120-second limit and 8 GiB sampled-RSS limit. Measurements are single runs; do not interpret launch-dominated small timing differences as speedups. RSS is sampled every 50 ms, giving a lower bound on peak. Liveness state/CPU summaries are not used in comparisons.

`evidence.json` lists the exact runs and all control commands. Each per-query record includes original model/query copies, hashes, executable version/hash, command, result, metrics and logs; each run saves the executed runner snapshot. ASCII temporary staging is byte-checked for compatibility with the Windows verifier. All diagnostic traces are in stdout.log.

## Reproduction

From the repository root:

```powershell
$verifier = 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe'
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E04
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E04 --drones 3
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E04 --drones 1 --loss-budget 2 --max-retry 2 --properties P28 --trace
python scripts/run_coordination_experiments.py --verifyta $verifier --suite E04 --drones 3 --loss-budget 0 --max-retry 0 --ack-timeout 14 --properties P08 --trace
python scripts/summarize_E04.py
```

Reruns create fresh raw-result directories. `summarize_E04.py` audits the fixed evidence index, not every matching directory. To analyze new runs, intentionally update that index. `run_E04_controls.py` is the sequential control orchestrator used for this study; it references the two recorded main runs and writes a new control index when explicitly rerun. Update those main-run references if replacing the whole study.

The analysis independently checks the loss edge, its counter update, unchanged non-network templates, exact input hashes, source preservation, raw verdicts and K=0/reliable agreement. It exports matrix JSON, execution summary, outcome PNG/SVG, recovery-trace PNG/SVG and event tables. See `docs/experiment_results_E04.md` for the findings and their limits.
