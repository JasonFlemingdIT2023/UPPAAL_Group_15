# Results

100 original records, 4 completion follow-up queries and 1 stopped run, plus 7 original-heartbeat follow-up queries and 1 stopped run.

| File or directory | Contents |
| --- | --- |
| [records.csv](records.csv) | Parameters, verdict, runtime, state counts and available evidence for each query. |
| [analysis](analysis/) | Summaries, matrices and trace data used by the report and figures. |
| [traces](traces/) | UPPAAL witnesses or counterexamples for diagnostic properties. |
| [Prepared → Done](proof/Prepared_to_Done.md) | Completion proof for ACK priority and both verifier outputs. |
| [Original heartbeat progress](proof/Original_heartbeat_progress.md) | Proof of eventual admission under original scheduling and the P06/P46 outputs. |

## Figures

- Key properties under original and ACK-priority scheduling · [PNG](figs/E06_outcomes.png) · [SVG](figs/E06_outcomes.svg)
- Original failure and ACK-priority reply witnesses · [PNG](figs/E06_reply_comparison.png) · [SVG](figs/E06_reply_comparison.svg)

[Models, queries and reproduction](../code/README.md)
