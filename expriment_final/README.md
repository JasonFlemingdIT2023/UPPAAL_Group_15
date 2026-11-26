# Group 15 experiment package

This package contains six UPPAAL experiments on fleet coordination for mission upload, ARM and START. Each report links to the models, queries, verdicts and traces.

| Experiment | Main result | Design and commands | Report |
| --- | --- | --- | --- |
| E01 Fleet scaling | Retry counter increments become reachable at three drones, and the P05 search grows with fleet size. | [README](E01_fleet_scaling/README.md) | [E01](E01_fleet_scaling/E_1_report.md) |
| E02 Delay and timeout | Four of nine settings admit confirmation failure on a reliable link. | [README](E02_delay_timeout/README.md) | [E02](E02_delay_timeout/E_2_report.md) |
| E03 Loss location | ARM can be executed or unexecuted at confirmation failure. | [README](E03_loss_location/README.md) | [E03](E03_loss_location/E_3_report.md) |
| E04 Bounded loss and retries | With timeout 24 in the tested grid, R≥K gives completion after Prepared. | [README](E04_bounded_loss/README.md) | [E04](E04_bounded_loss/E_4_report.md) |
| E05 Heartbeat | Both success and confirmation failure are reachable with three heartbeat senders. | [README](E05_heartbeat/README.md) | [E05](E05_heartbeat/E_5_report.md) |
| E06 ACK priority | The tested three-drone policy excludes retry exhaustion and guarantees completion after Prepared. | [README](E06_ack_priority/README.md) | [E06](E06_ack_priority/E_6_report.md) |

## Reference and terminology

The group’s version 08 reference has three drones, three mission items per drone, a single-slot link, transmission time 1–3, ACK timeout 14, up to two retries after the initial send, no loss and inactive heartbeat. Each experiment README lists departures from the reference. E06 uses version 09 to give pending command ACKs priority over other traffic.

| Term | Definition |
| --- | --- |
| GCS | Ground control station |
| ACK | Acknowledgement. The command model has accepted and denied replies. |
| Prepared | Mission upload has been confirmed for the full fleet. |
| Done | The ground station has received every START acceptance. |
| Confirmation failure | The ACK wait has exhausted its retry budget. |
| Admission | A packet gains the link slot and starts transmission. |
| P01 and P25 | P01 asks if a successful execution exists. P25 asks if every continuation after Prepared eventually succeeds. |

## Environment and reproduction

The records use UPPAAL 5.1.0-beta6 on Windows. Use Python 3.10 or newer, install the dependencies below and set the path to your local verifyta. The packaged commands were tested with Python 3.13.9, matplotlib 3.10.6 and psutil 7.0.0. Python orchestrates the runs and plots results. verifyta supplies the property verdicts.

```powershell
python -m pip install -r requirements.txt
$env:UPPAAL_VERIFYTA = 'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe'
```

Run the README commands from an experiment directory. On Windows, use a writable temporary directory with an ASCII-only path, where the scripts stage verifier inputs. Each `code/cases.csv` specifies the models, queries and verifier options. `results/records.csv` records verdicts and links to available witnesses. Replay outputs go to `results/reproduced/`.

Model parameters use model time units and verifier runtime uses seconds. Wall time includes verifier startup. RSS is sampled every 50 ms and reported as the peak sample. The archive retains timeouts and inconclusive over-approximation results.

## Verification evidence

The UPPAAL models, property queries and verifier logs form the verification evidence. E06 also includes a state-coverage argument that connects the full-model boundary check to the exact verification of the continuation model. [E06 completion proof](E06_ack_priority/results/proof/Prepared_to_Done.md)
