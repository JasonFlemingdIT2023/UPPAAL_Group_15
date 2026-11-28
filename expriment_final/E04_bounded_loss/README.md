# E04 Bounded loss and retries

[Report](E_4_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

How does retry limit R affect completion when the whole coordination attempt can lose at most K packets?

## Hypothesis

A bounded loss budget and sufficient time for replies can make completion provable with finite retries.

## Factors

Test the full K ∈ {0,1,2} × R ∈ {0,1,2} grid for N=1 and N=3.

## Controls

D_MIN=1, D_MAX=3, ACK_TIMEOUT=24, inactive heartbeat, reliable mission traffic. Controls cover unrestricted loss, a reliable link and timeout 14.

## Implementation

Use a shared budget K enforced by the network. The loss edge requires lossCount<K and increments its local counter. R counts the allowed retransmissions after each initial command.

## Queries and budget

Nineteen main queries: P01–P08, P10–P16, P21, P25, P27 and P28. P26 checks startup in diagnostics. Exact BFS, 120 s and 8 GiB per query.

## Interpretation

K is shared across drones and across ARM/START requests and replies. P25 starts at Prepared and applies to the tested grid settings.

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261125T134341195424Z_E04 --property P28
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
