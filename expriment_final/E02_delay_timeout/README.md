# E02 Delay and timeout

[Report](E_2_report.md) · [Code](code/README.md) · [Results and evidence](results/README.md)

## Question

Which transmission-delay and ACK-timeout combinations allow retries or retry exhaustion on a reliable link?

## Hypothesis

Shared-link contention extends reply waits. A longer timeout can exclude failure in some settings.

## Factors

Full 3 × 3 grid with D_MAX ∈ {2,3,5} and ACK_TIMEOUT ∈ {6,14,24}.

## Controls

N=3, D_MIN=1, three mission items per drone, two allowed retries, reliable link and inactive heartbeat. Reference cell is D_MAX=3 and ACK_TIMEOUT=14.

## Implementation

Change D_MAX and ACK_TIMEOUT in generated models and retain late-ACK handling.

## Queries and budget

P01–P16 for the reference, and P01–P05, P08, P09 and P15 for three grid repetitions. Supporting traces use P01/P09/P08/P17, with a P10 check. Exact BFS, 120 s and 8 GiB per query.

## Interpretation

The heatmap reports reachability. All model times use model units, and each trace describes one execution.

## Reproduction

Set `UPPAAL_VERIFYTA`, then run a representative query or replay the completed study from this directory.

```powershell
python code/replay.py --run 20261124T073421895292Z_pilot --property P08
python code/replay.py --all
```

[Package overview](../README.md) · [Per-query results](results/records.csv) · [Exact formulas](code/queries/README.md)
