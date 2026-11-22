# AI usage log

## Network timing (20 November 2026)

I used AI to help turn my network requirements into the first UPPAAL XML and test harness, including the clock guard and delay limit.

## Packet loss (21 November 2026)

I used AI to help work through the loss settings and the separate counters for each test flow, so delivery on one flow doesn't reset the other's counter.

## Checking results (22 November 2026)

I used AI to run the queries and help explain why producer 1 can wait up to 9 time units before its packet enters the shared link. AI also helped draft the network section.

## Wording and comments (22 November 2026)

I used AI to go over the wording of my network docs and report draft and to clean up the comments in `network_model.xml`, `network_queries.q` and `run_network_checks.py`. My prompt asked it to make the text consistent with the rest of the group's files, check every result against the saved logs and CSV, and not change the model or invent results. Only comments and wording changed. The model, the queries and the saved results are the same. I still have to rerun the checks with the updated model file.
