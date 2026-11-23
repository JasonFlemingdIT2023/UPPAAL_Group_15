# AI usage log

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
