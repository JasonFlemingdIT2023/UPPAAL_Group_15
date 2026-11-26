# E03 Loss location

[Report](E_3_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

What ARM states can accompany confirmation failure under request or ACK loss?

## Hypothesis

A request can fail to reach its receiver and a reply can be lost after command execution.

## Factors

Reliable, request loss only, ACK loss only, and loss of either kind.

## Controls

Use the reference N=3, transmission times, timeout, retries and inactive heartbeat. Mission upload is reliable. Run 21 checks with the original LOSSY=true setting.

## Implementation

Use DROP_COMMANDS and DROP_ACKS in the generated models to restrict the packet kinds eligible on the existing loss edge.

## Queries and budget

P01–P22 with diagnostic witnesses for P10/P11/P18. Exact BFS, 120 s and 8 GiB per query.

## Interpretation

P11 checks the instant of failure, P18 checks the specified settled abort state, and P22 checks whether ARM must follow.

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T125832488306Z_E03 --property P18
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
