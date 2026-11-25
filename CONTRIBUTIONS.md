MODELUPDATES

26.11.2026 - Chen (Codex-assisted E06 completion proof; human review pending)

Established N=3 Prepared-to-Done through a verified full-model boundary invariant, exact universal completion on a continuation abstraction, and a documented state-coverage argument. Extended the direct-query budget and retained auxiliary timer attempts separately. Added reproducible proof generators and evidence audits; updated E06 conclusions and the comparison figure. Models 08 and 09 unchanged. See docs/experiment_results_E06_completion.md.

25.11.2026 - Chen (Codex-assisted E06 ACK-priority improvement; human review pending)

Implemented a forward scheduling improvement in models/09_ack_priority.xml and matched experiment copies: pending command ACKs take the next available link slot. Added passive bookkeeping controls, exact witnesses and conservative over-approximation proofs. For N=3 with heartbeat, the tested priority model excludes retry exhaustion and retry increments, bounds post-admission reply waiting by six units, and proves each pending heartbeat gains admission. Prepared-to-Done remains unresolved for N=3. Audited 100 recorded queries and exported comparison figures; version 08 unchanged. See docs/experiment_results_E06.md.

25.11.2026 - Chen (Codex-assisted E04 execution; human review pending)

Completed the global bounded-loss/retry study: N=1,3 and K,R=0,1,2, with 342 main checks and 50 control/diagnostic invocations (392 total, all resolved). Added the network-only loss budget, conditional success checks, outcome matrix and recovery/failure traces. Reliable, unrestricted-loss, startup and short-timeout controls delimit the observed R>=K guarantee. Source model unchanged; see docs/experiment_results_E04.md.

25.11.2026 - Chen (Codex-assisted E05 execution; human review pending)

Completed matched heartbeat activation experiments for N=1,2,3 and N=2 period/first-offset comparisons. Recorded 37 UPPAAL invocations: 33 resolved and four timeouts, with raw evidence, audited cost figures and a packet timeline. DFS witnesses establish both success and retry exhaustion for N=3 with heartbeat and no loss; the P03 safety check remains unknown under the 120-second BFS/DFS budgets. Source model unchanged. See docs/experiment_results_E05.md.

25.11.2026 - Chen (Codex-assisted E01 execution; human review pending)

Completed N=1,2,3,4 fleet scaling with generated per-drone mission instances and size-aware queries: 168 formal checks (14 properties x 4 sizes x 3 runs), plus one N=4 late-ACK witness. Added audited per-query cost plots, explicit measurement limitations and docs/experiment_results_E01.md. Source model unchanged; previous E02/E03 model generation regression-checked.

25.11.2026 - Chen (Codex-assisted execution; human review pending)

Completed E03 loss-location study: four generated environments, P01-P22 checks, original-LOSSY regression control, four diagnostic witnesses, audited evidence and an outcome figure. 113 verifyta invocations completed using UPPAAL 5.1.0-beta6. Added explicit checks for settled unarmed outcomes and eventual ARM after confirmation failure. See docs/experiment_results_E03.md. Source 08 model unchanged.

24.11.2026 - Chen (Codex-assisted execution; human review pending)

Added reproducible baseline/E02 experiment runner, property suite, configuration inventory, raw per-query evidence, three E02 repetitions, diagnostic trace analysis and figures. Completed 16 baseline checks and 216 E02 invocations using UPPAAL 5.1.0-beta6, plus separate witness/supplementary checks. See docs/experiment_results_baseline_E02.md and experiments/coordination/README.md. Source model unchanged; other planned experiment groups remain pending.

VERSION 01: 17.10.2026 - Jason

Base Model Including first GCS stages, small Network with two main channel mechanisms and low level MAVLink Mission Protocl which comminicates Mission Size and First Mission Package.
