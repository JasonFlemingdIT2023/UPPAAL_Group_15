# Experiments, requirements and property-testing ideas
Jason  
23 November 2026  
Main candidate: [08_final_version.xml](../models/08_final_version.xml)

Possible plan and ideas for the team.

## 1. Start with a main query suite

Use a separately maintained query suite for the main configuration. Thsi should represent main properties and requirements that should definetly be verififed.

## 2. Formulate a requirement before a query

Use one row per claim in the [property catalogue](property_catalog.md):

`ID | plain-language requirement | scope/assumptions | observable event/state | formula | actual result | model hash | evidence as picture or something else`

For each query explain what a satisfying result means and what it does not mean. `E<> P` finds one possible execution. `A[] P` covers reachable states. `P --> Q` asks for eventual response whenever P occurs. A finite search timeout is inconclusive. Everything should be reproducible.

## 3. Starter properties

A few examples: Succesfull coordination should be possible. Arming respects local prerequisities. Starting respects arming. No deadlock. Loss is reachable when allowed. A send command will receive an outcome. Client can exhaust retry budget, and so on.

## 4. Recommended small experiment matrix
Ideas: 

| Experiment | Configuration | Main question / evidence |
|---|---|---|
| E1: reliable reference | N=3, MISSION_SIZE=3, D_MIN=1, D_MAX=3, ACK_TIMEOUT=14, MAX_RETRY=2, LOSSY=false; no heartbeat | R1–R9 and R12/R13 as feasible; establish actual baseline results |
| E2: command loss | E1 with LOSSY=true | witness of accepted execution without confirmation; success remains possible but is not guaranteed |
| E3: latency sensitivity | D_MAX=2,3,5 with D_MIN=1 and fixed timeout | Does slower service permit more timeout/retry outcomes? No probability claim |
| E4: timeout sensitivity | ACK_TIMEOUT=6,14,24 with fixed delay/loss configuration | Which outcomes become reachable? Do not call the first passing value a universal optimum |
| E5: retry sensitivity | MAX_RETRY=0,1,2 under loss | Finite attempt budgets and uncertainty; unlimited loss can still defeat any finite budget |
| E6: scale | N=1,2,3 with explicit instances adjusted | Verification runtime/state growth and fleet interaction, small-N proofs do not imply larger-N proofs |
| E7: heartbeat ablation | Matched final-model copies with/without active heartbeat; optional finite-preparation variant | Verification cost and contention; same command fix, settings and query in each copy |

Also what happends when we include more drones. What happends regarding the staes etc. This are ideas, please think also of what could be suitable.




