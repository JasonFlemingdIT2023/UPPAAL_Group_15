# E01 Fleet scaling

## Design

We generated fleets of one to four drones from version 08. Each drone had three mission items, shared a single link with service times of 1–3, and used an ACK timeout of 14 with up to two retries per command. Loss and heartbeat were disabled to isolate fleet size. Mission processes and per-drone queries were generated for each size. Exact breadth-first verification checked 14 properties per fleet with three repetitions, for 168 checks.

## Properties and cost

Confirmation failure remained unreachable (P15) as the fleet grew from one to four drones. Retry counter increments became reachable at three drones (P23). Verdicts and state counts agreed across three repetitions. A successful execution existed at every fleet size (P01), and the checked prerequisites, mission integrity and conditional coordination progress held. [Per-query results](results/records.csv)

| N | Any retry increment reachable | Any failure reachable | P05 Explored | P05 Stored | Median wall (s) |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | No | No | 45 | 40 | 0.1326 |
| 2 | No | No | 576 | 481 | 0.1266 |
| 3 | Yes | No | 7,541 | 6,231 | 0.1236 |
| 4 | Yes | No | 112,482 | 92,776 | 0.7850 |

![Verification cost by fleet size](results/figs/E01_scaling.png)

P05 explored about 14.9 times as many states at four drones as at three. Wall times for the three smaller fleets are close to process startup overhead, so state counts give a clearer comparison of search effort. [Three-run metrics](results/analysis/scaling_summary.json)

In the four-drone P17 witness, four requests used the shared link in sequence. Relative to the first admission, ACK0 entered the link at t=12 and arrived at t=14, immediately after the timeout transition at the same model time. The counter increased, and the client accepted the reply from Sending. This trace contains one CMD0 transmission. [Trace events](results/analysis/n4_retry_trace.md)

## Interpretation

P14 checked that every confirmed mission contained all its items. P16 checked that Prepared eventually led to Done or Aborted. Both held at every fleet size. P23 and P15 distinguish two scheduling effects. From three drones onward, extra requests can precede an ACK and trigger a timeout, while the remaining attempts in these settings still exclude retry exhaustion. The four-drone trace also shows how the ordering of events at the same model time can affect the counter.

All three repetitions finished within 120 s and 8 GiB per query. Shading shows the minimum and maximum across repetitions. State counts agreed across all three. The scaling comparison uses state counts from the selected reachability and safety checks.
