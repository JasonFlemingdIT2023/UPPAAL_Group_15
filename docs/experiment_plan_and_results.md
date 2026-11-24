# Experiment plan and result collection

Reference: [08_final_version.xml](../models/08_final_version.xml)


## 1. What the experiments should establish

Main question: under which communication and timing assumptions can the GCS correctly coordinate mission upload, ARM and START across multiple drones sharing a link?

The evaluation should distinguish:

- Correctness: prerequisites, evidence and supervisor decisions remain consistent.
- Communication uncertainty: a drone can act without its acknowledgement reaching the GCS.
- Timing sensitivity: delay, timeout and retry choices affect possible outcomes.
- Verification scalability: increasing concurrent activity changes the cost of checking properties.
- Modelling trade-offs: explicit heartbeat traffic and alternative abstractions change both behaviour and verification effort.

A useful result may be a proof for the model, a counterexample, an exact symbolic bound where justified, or a documented resource limit. A screenshot or one successful simulator execution is not a universal guarantee.

## 2. Common reference and controls

| Setting | Reference value |
|---|---:|
| Drones N | 3 |
| MISSION_SIZE | 3 |
| D_MIN | 1 |
| D_MAX | 3 |
| ACK_TIMEOUT | 14 |
| MAX_RETRY | 2 |
| LOSSY | false |
| Heartbeat processes | inactive |
| Network | one shared slot and no scheduler |
| Mission traffic | reliable |

Time values are model units, not automatically seconds. MAX_RETRY chounts retransmissions after the first attempt. Each experiment must identify all differences from this reference. Keep the command-client delayed-ACK fix in matched variants unless that fix is the variable being evaluated.

The model permits nondeterministic loss and service ordering. It has no packet-loss probability or fairness guarantee. Do not estimate loss/success percentages from symbolic witness traces. Physical flight completion is outside scope.

## 3. Common property suite

Keep queries in a separate versioned property file. Resolve inherited queries that do not fit the experiment: heartbeat reception cannot occur when its processes are inactive and keep in mind that plain deadlock freedommis not applicable for a system like this with a fixed end, so change the querie or put a self loop on the point.

| ID | Claim or question | Example formula | Limit of interpretation |
|---|---|---|---|
| P01 | Success is reachable | `E<> Supervisor.Done` | One successful execution, not all executions |
| P02 | Arming respects local prerequisites | `A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])` | Selected local rule, not general flight readiness |
| P03 | Starting respects arming | `A[] forall (i : drone_id) (started[i] imply armed[i])` | Abstract START effect, not completed flight |
| P04 | GCS success requires every START acceptance | `A[] (Supervisor.Done imply forall (i : drone_id) cmdAccepted[i][START])` | Checks supervisor evidence |
| P05 | No deadlock before an outcome | `A[] (deadlock imply (Supervisor.Done || Supervisor.Aborted))` | Does not prove cleanup or progress after Aborted |
| P06 | Every admitted packet leaves the link | `Link.Transmitting --> Link.Idle` | Separately tests a blocked delivery, including after an outcome |
| P07 | Service outcomes respect their time window | `A[] ((Link.Delivered || Link.Lost) imply (Link.t >= D_MIN && Link.t <= D_MAX))` | Service after admission, not total coordination time |
| P08 | Timeout exhaustion is reachable | `E<> CommandClient(0).Failed` | A missing confirmation outcome, not proof of non-execution |
| P09 | Retry is reachable | `E<> (CommandClient(0).retries > 0)` | Counter may retain a value after an operation |
| P10 | ARM executed despite failure to confirm | `E<> (cmdFailed[0][ARM] && armed[0])` | Demonstrates possible uncertainty |
| P11 | ARM unconfirmed and not executed | `E<> (cmdFailed[0][ARM] && !armed[0])` | Inspect later trace behaviour; not a permanent-state claim |
| P12 | Network loss is reachable | `E<> Link.Lost` | Expected false with transmission loss disabled |

These are starter queries. Some safety properties directly reflect guards and are useful regression checks. the evaluation should also include nontrivial progress and uncertainty analysis.


## 4. E01 — Fleet scaling

**Question:** How do more concurrent drone sessions affect coordination outcomes and verification effort?

**Configurations:** N = 1, 2, 3, 4. Attempt more only if earlier cases fit the resource limit and is verifiable with verifier. Keep other reference parameters fixed and heartbeat inactive.

**Implementation:** generate the explicit MissionSender/MissionReceiver instances and system composition for each N. Changing N alone is insufficient. Automatically instantiated command templates follow the bounded drone type. Update per-drone queries to the active fleet.

**Check:** P01–P08 and mission integrity. Inspect whether larger fleets permit retries or failure without loss. Do not assume such failure must occur.

**Collect:** per-query truth result, runtime, explored/stored states as separately reported, peak memory, completion status and one relevant trace if behaviour changes. Also pictures if applicable and added properties if insighful.

**Report outputs:** runtime and state count against N, property-outcome table, and explanation of any change in failure reachability. 

## 5. E02 — Delay and timeout interaction

**Question:** Can a reliable network still cause retries or timeout exhaustion under an insufficient acknowledgement timeout?

**Configurations:** D_MIN = 1; D_MAX in {2, 3, 5}; ACK_TIMEOUT in {6, 14, 24}; MAX_RETRY = 2; LOSSY = false. Nine configurations; N = 3 and no heartbeat.

**Check:** P01, P08, P09 and core safety. Capture a trace for a configuration where retries/failure are possible and compare it with one where they are not. If no outcomes differ, report that and expand selected values only with a stated reason.

**Metrics:** property outcomes, retry reachability, optional maximum retry-counter value, verification cost and illustrative event timing. `sup: CommandClient(0).retries` is supported, but measures the highest reachable counter, not a retry probability or total fleet retransmissions.

**Report outputs:** heatmap of retry/failure reachability over delay and timeout, with unfinished searches marked separately.

## 6. E03 — Where loss occurs

**Question:** Can the same client failure correspond to different actual drone states depending on whether the request or its reply is lost?

**Before** Compare reliable version  and version under loss with lossy activated before that. 
**Small extension:** replace the single loss switch in an experiment copy with `DROP_COMMANDS` and `DROP_ACKS`. The loss branch still acts after admission and after D_MIN. Its eligible kind condition must match the selected switches. Do not introduce mission loss.

| Mode | Commands may be lost | Accepted/denied replies may be lost |
|---|---|---|
| Reliable | no | no |
| Request loss | yes | no |
| Reply loss | no | yes |
| Both | yes | yes |

**Check:** P01, P08, P10–P12 and core safety. For ARM uncertainty, compare failure with armed true versus false. A state with armed false may still have an outstanding command, so inspect what happens afterwards before claiming the operation never executes.

**Report outputs:** a four-mode outcome table and two short explained traces. Separate command acceptance from physical completion; see [MAVLink command protocol](https://mavlink.io/en/services/command.html).

## 7. E04 — Retry limits and bounded loss

**Priority:** optional extension after reliable and unrestricted-loss checks work.

**Question:** Under a stronger communication assumption, do retries recover coordination or still leave failure reachable?

Unrestricted loss can defeat every finite retry budget. Merely sweeping retries under that assumption may leave both success and failure reachable in every configuration. That is a limitation result, not evidence that retries have no practical benefit.

**Simple extension:** at most K command-protocol transmission losses across the whole coordination attempt. Add a network loss counter, increment it only on a loss outcome, and disable loss after K. The clients never observe this counter. The bound applies globally to command requests and replies; it is not a per-command/per-drone bound and is not the standalone model's consecutive-loss assumption.

**Configurations:** K in {0, 1, 2}, MAX_RETRY in {0, 1, 2}. Choose a delay/timeout configuration from E02 with no demonstrated timing-only failure. Begin with one drone, then repeat selected fleet configurations.

**Check:** P01, P08, P10 and candidate universal progress/success properties under stated assumptions. Review any counterexample before concluding why a guarantee fails. Do not presume MAX_RETRY >= K proves fleet success; timeout, scheduling and outstanding messages matter.

**Report outputs:** loss-budget/retry outcome matrix, recovery or failure trace, and explicit definition of the stronger environmental assumption.

## 8. E05 — Heartbeat traffic and modelling cost

**Question:** What does explicit recurring background traffic add to behaviour and verification cost? Can lower frequency or staggered initial releases help?

Generate variants from version 08, preserving its command-client fix. Do not directly attribute all differences between historical 06B and 08 to heartbeat. The current source resets its period on network admission; it is self-timed and can wait Pending, not a fixed-rate queued source.

### A. Activation ablation

Compare heartbeat inactive versus active with HB_PERIOD = 20. Start with one/two drones and attempt three. Check P01, one common safety property, P08 and heartbeat reception reachability in active variants. Use a common finite limit for expensive checks. Here it is very insighful what verification ressources are needed and whetger we are able to verifiy the core properties.


**Collect:** property results, run completion status, runtime/state/memory cost, sender settings and an explained traffic trace. 

**Report outputs:** matched cost table, period/offset comparison and a discussion separating modelled traffic effects from verifier effort. 



## 9. Repository layout for evidence

Suggested layout; these folders are not created by this document:

```text
experiments/
  E02_delay_timeout/
    README.md
    queries.q
    configurations
results/
  E02_delay_timeout/
    dmax3_timeout14/
      model.xml
      query_P01
      query_P01_result
      traces/
    summary
```

Each experiment README states the question, hypotheses, independent variables, controls, exact implementation changes, query IDs, resource limits, commands and interpretation limits. Each configuration saves its actual generated model, not just a filename referring to a moving working copy.

## 10. Result recording protocol

Save one row per query invocation, with a separate run ID for repetitions. Recommended columns:

```text
experiment_id, configuration_id, repetition,
git_commit, model_sha256, query_sha256, property_id,
N, mission_size, d_min, d_max, ack_timeout, max_retry,
loss_mode, loss_budget, heartbeat_mode, heartbeat_period, heartbeat_offsets,
tool_version, search_options, trace_enabled,
result, wall_seconds, explored_states, stored_states, peak_memory_bytes,
time_limit_seconds, log_path, trace_path
```


## 11. From records to the report

For each experiment write: question -> controlled change -> actual property outcomes -> representative trace/plot -> explanation -> limitations. Present assumptions separately from findings. Use configuration IDs to connect every table/figure to its evidence directory.

A useful final report contains a common property matrix, scaling plots per query, a delay/timeout heatmap, loss-location traces and a matched heartbeat cost comparison etc, feel free to think about results presentation. Mark incomplete configurations visibly and include them in the discussion. State whether an experiment changes the environment, client policy, scheduling or instrumentation.

