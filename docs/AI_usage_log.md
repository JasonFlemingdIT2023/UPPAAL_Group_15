# AI usage log

## E06 original-scheduling heartbeat follow-up (26 November 2026 - Chen, Codex assisted)

Chen asked why eventual heartbeat admission was inconclusive under original scheduling and requested further verification. Codex checked the original UPPAAL verdicts, ran direct follow-ups, and verified packet progress (P06) and matching mission receivers (P46). It documented the finite-traffic argument that establishes P30–P32 for the tested three-drone configuration. Codex also expanded the six bilingual experiment reports and embedded the figures directly. The E06 results now report the matched P03 search counts and distinguish direct query outcomes from the proof of heartbeat progress.

## E06 completion proof (26 November 2026 - Chen, Codex assisted)

At Chen's request, Codex extended the full N=3 P25 query budget to 1,200 seconds and investigated a passive completion timer. It then verified a full-model Prepared-boundary invariant and an exact universal-completion query on a continuation abstraction covering arbitrary heartbeat phases and residual in-flight heartbeat service. The documented state mapping establishes N=3 Prepared-to-Done for the existing configuration. After completing the proof audit, it intentionally stopped the still-unresolved direct query at approximately 814 seconds and retained an interruption record. Scripts audit unchanged original protocol templates, input/output hashes and raw verdicts. Timer attempts and a rejected bootstrap formulation are recorded separately. The original 100-query results remain historical evidence; reports and the outcome figure now include the compositional proof. Neither model 08 nor model 09 was changed. Human review is pending.

## E06 ACK-priority improvement (25 November 2026 - Chen, Codex assisted)

At Chen's request, Codex added ACK-priority network admission to copies of the current final model and exported models/09_ack_priority.xml. It used a passive pending-flag control, verified flag/location correspondence, ran exact small-scale comparisons and concrete N=3 witnesses, and used UPPAAL's conservative convex-hull approximation for definitive safety/heartbeat-progress proofs after exact searches reached their budgets. The analyzed set has 100 records: 87 decisive, three timeouts and ten inconclusive approximation answers. N=3 Prepared-to-Done is still unresolved. Original version 08 remains unchanged. Code-generation/parser development attempts and one unfinished query are retained separately. Reports and figures were generated from audited logs and traces; human review remains pending. No remote push was performed.

## E04 bounded-loss experiments (25 November 2026 - Chen, Codex assisted)

At Chen's request, Codex added a global loss-budget counter only to generated network copies, parameterized retry limits, and executed 392 actual UPPAAL queries (342 matrix checks plus 50 controls/diagnostics), all resolved. It verified conditional success after Prepared, distinguished existential recovery from universal success, inspected startup and timing counterexamples, and generated audited matrices, event tables and figures. Independent checks covered unchanged protocol templates, the single counter update on loss, K=0/reliable agreement and byte-equivalent generation for 25 prior configurations. No original model modification, scheduling improvement or remote push was performed. Results remain subject to human review; no general guarantee outside the tested assumptions is claimed.

## E05 heartbeat experiments (25 November 2026 - Chen, Codex assisted)

At Chen's request, Codex generated matched heartbeat off/on copies of version 08 for N=1,2,3, added N=2 period and first-release-offset controls, and executed 37 real UPPAAL queries. It kept four timeouts visible as unknown, used separate DFS witnesses to establish N=3 success and no-loss confirmation failure, and retained the additional DFS safety timeout. It audited hashes, exact model pairing, previous experiment generation and raw verdicts; extracted the failure packet timeline; and produced three figures plus docs/experiment_results_E05.md. Single-run verifier costs are distinguished from system performance. The original source model was not modified; no policy improvement or remote push is claimed. Human review is pending.

## E01 fleet scaling (25 November 2026 - Chen, Codex assisted)

At Chen's request, Codex extended the runner for N=1..4 with explicit mission instances and size-aware integrity/retry queries, ran UPPAAL 5.1.0-beta6 for three repetitions (168 formal invocations), and generated one diagnostic witness. It audited recorded verdicts/hashes, checked N=3 against baseline and prior E02/E03 generation for regressions, and generated scaling figures and a results note. An initial empty-query-section tool error is retained and excluded. Source model unchanged; no remote push. Human review is pending. E05 and optional E04 are not claimed completed.

## E03 loss-location experiments (25 November 2026 - Chen, Codex assisted)

Codex extended the Python runner to generate separate request/ACK loss switches in experiment copies, ran the actual UPPAAL 5.1.0-beta6 verifier, and collected 88 main checks, 21 original-switch controls and four diagnostic traces. It added P18-P22 to distinguish transient unarmed states from settled outcomes and eventual execution, audited hashes/logs, and prepared the outcome plot and explanatory report. An initial XML-escaping assertion stopped generation before verification and is excluded from results. No source-model modification or external push was performed. Human review remains pending.

## Baseline and E02 experiments (24 November 2026 - Chen, Codex assisted)

At Chen's request, Codex implemented a sequential experiment runner and analysis script following `experiment_plan_and_results.md`, executed baseline P01-P16 and three repetitions of the nine-configuration E02 matrix, and collected additional diagnostic witnesses. It added P13-P17 checks, audited raw evidence, and generated figures and a Chinese results note. The original model was not edited. UPPAAL 5.1.0-beta6 was used after the local 5.0.0 failed license preflight. Failed Unicode-path and XML-trace-export attempts were preserved and excluded from conclusions. Results, assumptions and remaining work are documented in `experiment_results_baseline_E02.md`; these records are machine-checked, with human review still pending. No E01/E03/E04/E05 result is claimed.

## PacketNetwork diagram layout (23 November 2026 - Jason)

I asked AI to make the `PacketNetwork` diagram in `06B_simple_integration.xml` clearer by separating the edges and positioning their labels, without changing functionality or complexity. Only diagram coordinates and edge routing were changed.

Chat evidence - my prompt:

> Take a look over the current PacketNetwork Template and make it more structured regarding the Edges. Dont change anything regarding complexity or function. Just make the structure more clear and seperated and also the position of the Edge Declarations.

Answer:

>Rearranged PacketNetwork in [06B_simple_integration.xml](/Users/Win11Pro/Development/repos/FL_UPPAAL_Group_15/models/06B_simple_integration.xml):
>- Acceptance edges on the left; matching delivery edges on the right.
>- Mission, command and heartbeat edges grouped with spacing.
>- Edge labels aligned in separate rows.
>- Loss and return paths below the main diagram.
>Only positions and edge routing changed. I checked that all declarations, guards, synchronisations, updates and model structure remain unchanged.
>Reload the file in UPPAAL to see the layout.

## Network timing (20 November 2026)

I used AI to help turn my network requirements into the first UPPAAL XML and test harness, including the clock guard and delay limit.

## Packet loss (21 November 2026)

I used AI to help work through the loss settings and the separate counters for each test flow, so delivery on one flow doesn't reset the other's counter.

## Checking results (22 November 2026)

I used AI to run the queries and help explain why producer 1 can wait up to 9 time units before its packet enters the shared link. AI also helped draft the network section.

## Wording and comments (22 November 2026)

I used AI to go over the wording of my network docs and report draft and to clean up the comments in `network_model.xml`, `network_queries.q` and `run_network_checks.py`. My prompt asked it to make the text consistent with the rest of the group's files, check every result against the saved logs and CSV, and not change the model or invent results. Only comments and wording changed. The model, the queries and the saved results are the same. I still have to rerun the checks with the updated model file.
