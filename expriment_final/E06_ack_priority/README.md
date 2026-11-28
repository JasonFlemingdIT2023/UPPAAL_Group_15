# E06 ACK-priority scheduling

[Report](E_6_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

Can prioritizing pending command ACKs remove the E05 failure while retaining heartbeat and coordination progress?

## Hypothesis

Giving pending ACKs the next free link slot shortens reply waits and can exclude timeout retries.

## Factors

Compare original and ACK-priority scheduling at N=1, 2, 3. N=2 includes a passive-flag control.

## Controls

Heartbeat is active with period 20 and remaining parameters follow the reference. The single-slot link selects another packet after the current transmission finishes.

## Implementation

Set ackPending at Decide entry and clear it at reply admission. Six non-command-ACK admission edges require every flag to be false.

## Queries and budget

Core queries are P25, P29–P32 and P34–P38. See the query list for regression and decomposition checks. The main study uses exact and convex-hull over-approximate verification with 120 s and 8 GiB per query. The two proof checks have 120/300 s limits. Extended direct P25 had a 1,200 s limit and was stopped at about 814 s.

## Interpretation

The reply bound starts at request admission. For N=3, P25 follows from the Prepared boundary and the continuation coverage argument. Under original scheduling, P30–P32 follow from P06 and finite competing traffic. [Heartbeat proof](results/proof/Original_heartbeat_progress.md)

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T171822124561Z_E06_prepared_progress --property ContinuationDone
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
