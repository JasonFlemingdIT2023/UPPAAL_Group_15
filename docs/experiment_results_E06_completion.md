# E06 supplement: a compositional proof of Prepared→Done for three drones

2026-11-26. The target property is `Supervisor.Prepared --> Supervisor.Done`. The current three-drone ACK-priority configuration satisfies it. The proof combines two UPPAAL checks with the state-coverage argument below.

Fixed settings are N=3, MISSION_SIZE=3, active heartbeats, HB_PERIOD=20, D_MIN=1, D_MAX=3, ACK_TIMEOUT=14, MAX_RETRY=2 and LOSSY=false. Neither `models/08_final_version.xml` nor `models/09_ack_priority.xml` was modified.

## Verification results

| Check | Verified model | Method | Verdict | Wall time |
|---|---|---|---|---:|
| State boundary at Prepared | Full three-drone ACK-priority model | Conservative over-approximation, definite satisfied result | Satisfied | 8.3554 s |
| `A<> Supervisor.Done` | Verification model covering all Prepared continuations | Exact compact DBM | Satisfied | 2.8931 s |

Together these establish `Prepared --> Done` in the full model. The second check quantifies over every execution of the continuation model. Timings include startup and overlap with the extended full-model run.

The direct full-model P25 query was given a 1,200 s limit. After the compositional proof and audit completed, it was stopped at approximately 814.338 s (13 min 34 s), with no verdict and about 4.40 GiB resident memory. Its status is `interrupted_after_compositional_proof`. The [interruption record](../results/coordination/20261125T171027951246Z_E06/n3_dmax3_timeout14_scheduler_ack_priority/P25/interruption.json) is retained separately.

## Step 1: establish the boundary at Prepared

The full-model query `A[] (Supervisor.Prepared imply boundary_conditions)` returns a definite satisfied result. The boundary conditions state that:

- All three mission senders are Done and all three receivers are Uploaded; every `uploadDone` and `missionInstalled` flag is true.
- Every command client and server is Idle, the current command is ARM, and all retry counters are zero.
- ARM/START has not begun. The `armed`, `started`, `ackPending`, `cmdAccepted`, `cmdDenied` and `cmdFailed` flags are unset.
- The link is idle, in the zero-time Delivered location, or transmitting a heartbeat.
- Each heartbeat sender is Waiting with clock value at most 20, or Pending with clock value at least 20.

This check includes the complete upload phase and network. An existing exact E06 success witness establishes reachability of Prepared.

## Step 2: cover every possible heartbeat state at Prepared

The verification model retains the original transitions of the supervisor, command clients and servers, heartbeat senders, connection monitors and network. Finished mission senders/receivers are no longer instantiated. A new initialization phase constructs the environment states possible at Prepared.

**Heartbeat phases.** During a 20-unit initialization window, each heartbeat sender independently chooses when to reset its period clock. At the end, all three clocks independently cover every real value in [0,20].

**Already-pending heartbeats.** A Pending sender's period may exceed 20 in the full model, but that value occurs in no guard or invariant before admission and resets on admission. It maps to a Waiting sender at period=20 followed by an immediate transition to Pending. Each sender independently permits this case.

**An in-flight heartbeat.** The initial link can be idle or carry one residual heartbeat from any drone. That packet can be delivered after any delay in [0,3], covering every residual service time of a full-model heartbeat. Subsequent packets retain the original 1–3 service window.

**Delivered at Prepared.** Delivered is committed and has only a zero-time transition to Idle, without variable updates. Eliminating this step yields the idle-link case, with no intervening time passage.

At the end of initialization, the supervisor enters Prepared and all upload/mission-installation flags are true. Command, ACK-priority, heartbeat-period, timeout, retry and reliable-delivery rules match the full model.

## Why the continuation proves the full-model property

Take any reachable full-model Prepared state. The first check establishes its boundary conditions. Mapping its heartbeat phases and link state into the initialization construction yields a continuation-model state covering its future behaviour.

The mapping also omits data that cannot affect later control flow:

- MissionSender.Done and MissionReceiver.Uploaded have no outgoing edges, so removing those instances removes no future communication.
- CommandClient.x is unused in Idle/Sending guards and invariants and resets at first command admission. Its old value at Prepared does not affect the continuation.
- ConnectionMonitor.age and `heartbeatSeen` only record reception and are unread by command, network or supervisor guards. Both monitor receive locations can accept another heartbeat.
- The next admission completely overwrites the idle link's old packet. The continuation retains the peer choice for an in-flight heartbeat.

Every full-model continuation after Prepared is therefore covered. The continuation also admits some heartbeat-phase combinations or residual-service choices that might be unreachable in the full model. Exact UPPAAL verification of `A<> Supervisor.Done` succeeds over this larger set, so every covered full-model continuation also reaches Done. The construction uses the existing scheduling and heartbeat rules without an additional fairness assumption.

The script checks template preservation by removing the added initialization locations, transitions and declarations and restoring the initial locations. All original protocol templates then match. The full-model boundary check, generated model, actual queries, commands, raw outputs and hashes are archived. The argument above establishes state coverage; the structural audit verifies preservation of the protocol templates.

## Other attempts

A separate variant resets an observation clock at Prepared and checks whether elapsed time stays at most 120 until Done. Over-approximation returns MAY NOT; exact checking reaches its 300 s limit. These checks leave the proposed 120-unit completion bound unresolved.

The first initialization variant placed clock guards on urgent-channel edges and was rejected by the verifier. A corrected variant uses ordinary broadcast synchronization, with location invariants and guards ensuring initialization finishes at time 20. Verification then succeeds. The rejected run is indexed as a development attempt.

## Evidence and reproduction

- [Supplementary evidence index](../experiments/E06_ack_priority/completion_evidence.json)
- [Audited proof results](../results/coordination/analysis_E06/completion_proof.json)
- [Raw boundary-check output](../results/coordination/20261125T171730362946Z_E06_prepared_boundary/stdout.log)
- [Raw exact continuation-check output](../results/coordination/20261125T171822124561Z_E06_prepared_progress/stdout.log)
- [Continuation model](../results/coordination/20261125T171822124561Z_E06_prepared_progress/model.xml)

Run from the repository root:

```powershell
python scripts/run_E06_prepared_abstraction.py --mode boundary --state-representation 3 --limit 120
python scripts/run_E06_prepared_abstraction.py --mode progress --state-representation 1 --limit 300
python scripts/summarize_E06_completion_proof.py
```

New runs create new directories. By default, the audit script checks the fixed evidence referenced by the supplementary index.
