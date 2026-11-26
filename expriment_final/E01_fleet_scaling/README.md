# E01 Fleet scaling

[Report](E_1_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

How does fleet size affect coordination and verification cost?

## Hypothesis

More concurrent sessions increase the state space and may push reply waits past the timeout.

## Factors

Drone count N = 1, 2, 3, 4.

## Controls

Use the reference delay, timeout, retries, reliable link and inactive heartbeat. Run three repetitions per fleet size.

## Implementation

Generate mission sender and receiver instances and system composition for each N, and adapt per-drone queries.

## Queries and budget

P01–P09, P13–P16 and P23 in the main study, plus P17 for the N=4 trace. Exact BFS, 120 s and 8 GiB per query.

## Interpretation

Cost uses symbolic states and runtime under matched query and verifier settings. P09/P23 measure whether a retry counter can increase.

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T131521932777Z_E01 --property P17
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
