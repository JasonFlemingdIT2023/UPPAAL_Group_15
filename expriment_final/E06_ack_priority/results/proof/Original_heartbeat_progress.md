# Three-drone heartbeat progress under original scheduling

This argument establishes P30–P32. Whenever `HBSender(i)` enters Pending, it eventually synchronizes on `heartbeat_tx[i]` to gain admission and return to Waiting. The configuration is version 08 with original scheduling, three drones, three mission items, heartbeat period 20, service times 1–3, ACK timeout 14, up to two retries and a reliable link. [Model](../../code/models/n3_dmax3_timeout14_scheduler_original.xml)

## Verified premises

| Query | Result | Evidence |
| --- | --- | --- |
| P06 `Link.Transmitting --> Link.Idle` | Satisfied in about 83.92 s. | [Query](../../code/queries/P06.q) · [Verdict](original_packet_progress.txt) |
| P46 Every in-flight mission packet has a matching receiver | Satisfied in about 31.93 s. | [Query](../../code/queries/P46.q) · [Verdict](original_mission_receiver.txt) |

Both checks used conservative convex-hull over-approximation on the original model and returned a definite `Formula is satisfied`. P06 supplies the verified premise of the proof, and P46 independently checks mission receive states. The initial direct checks of P30–P32 returned `MAY NOT`, and the subsequent plain-DBM runs with LU extrapolation gave the same verdict. [Per-query results](../records.csv) · [UPPAAL verdict semantics](https://docs.uppaal.org/gui-reference/verifier/verifying/)

With compact DBMs and automatic extrapolation, extended direct verification of P30 reached its 600 s limit. The same finite-traffic argument covers all three drones, so the subsequent direct P31 search was stopped. The separate full-model deadlock check P45 returned `MAY NOT`. These records are retained alongside the positive P06 verdict. [Follow-up checks](../analysis/heartbeat_followup.json)

## Why a pending heartbeat cannot wait indefinitely

1. **An idle link cannot consume time while the target waits.** In the original model, `heartbeat_tx[i]` is enabled and urgent when the target is Pending and the link is Idle. Other enabled discrete actions may be taken first. Time cannot elapse in that idle state. Each admission resets the link clock, Transmitting is bounded by 3, and the committed Delivered location immediately returns to Idle. P06 rules out a permanently blocked packet.
2. **The fleet admits at most 60 mission and command packets.** Each drone has at most one count packet, three request/item pairs and one mission ACK, giving 24 mission packets. Each drone can be issued ARM and START once. With one initial attempt and up to two retries per command, at most 18 command requests are admitted. Each request produces at most one acceptance or denial, giving at most 18 replies.
3. **Other heartbeats cannot occupy the link indefinitely.** If the target has waited T model units, each of the other two senders can admit at most `1 + T/20` heartbeats during that time, because its admissions are at least 20 units apart. Allow one packet already in flight when Pending began. Counting up to three units of service per packet gives `T ≤ 3 × (1 + 60 + 2 × (1 + T/20)) = 189 + 0.3T`, hence `T ≤ 270`.

An infinite sequence of discrete steps cannot evade this bound in finite time. Every newly admitted packet takes at least one unit of service before releasing the link. Delivery and return, upload startup, command dispatch, retry-counter updates and transitions into Pending can occur only finitely many times between admissions. With the target still waiting, an idle link has an enabled heartbeat admission and P06 ensures a busy link eventually becomes idle. Every maximal execution therefore admits the target within the derived finite bound. The analytical bound of 270 may exceed the longest reachable wait. [UPPAAL urgent channel semantics](https://docs.uppaal.org/language-reference/system-description/semantics/)

## Reproduce the machine checks

Set `UPPAAL_VERIFYTA` and run from the E06 directory.

```powershell
python code/run_coordination_experiments.py --suite E06 --scheduler original --drones 3 --state-representation 3 --properties P06 P46 --limit 120
```
