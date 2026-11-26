# E05 Heartbeat traffic

[Report](E_5_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

How does heartbeat traffic change the allowed executions and verification cost, and how do the period and first release phase affect the comparison?

## Hypothesis

Heartbeat and command traffic share the link, adding timing interleavings that can delay ACKs.

## Factors

Pair heartbeat off/on at N=1, 2, 3, with period 20. At N=2 also test period 40 and period 20 with staggered first releases.

## Controls

Use three mission items per drone, service time 1–3, ACK timeout 14, up to two retries, no loss and original scheduling.

## Implementation

Enable or disable HBSender and ConnectionMonitor through system composition. First-release staggering adds floor(id×period/N) to the first wait and clears it at the first admission.

## Queries and budget

P01, P03, P08 and P24. Main runs use exact BFS, and the initial DFS follow-ups have the same 120 s and 8 GiB per-query limits. Extended BFS checks for P01, P03 and P08 use a 600 s, 2 GiB budget per query.

## Interpretation

Heartbeat periods restart at link admission. The offset changes only the first release. Matched verification costs use one measurement per setting and query.

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T132904048744Z_E05 --property P08
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
