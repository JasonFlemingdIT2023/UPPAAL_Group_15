# Results

24 activation checks, 8 settings checks, 4 diagnostics, 1 DFS safety check, 3 extended BFS checks and 1 decisive check reused from E06.

| File or directory | Contents |
| --- | --- |
| [records.csv](records.csv) | Parameters, verdict, runtime, state counts and available evidence for each query. |
| [analysis](analysis/) | Summaries, matrices and trace data used by the report and figures. |
| [Extended verification](analysis/activation_followup.json) | Original BFS, extended BFS and evidence for the final verdicts. |
| [traces](traces/) | UPPAAL witnesses or counterexamples for diagnostic properties. |

## Figures

- Matched heartbeat activation comparison · [PNG](figs/E05_activation.png) · [SVG](figs/E05_activation.svg)
- Period and first-release offset · [PNG](figs/E05_settings.png) · [SVG](figs/E05_settings.svg)
- Three-drone failure trace without packet loss · [PNG](figs/E05_failure_timeline.png) · [SVG](figs/E05_failure_timeline.svg)

[Models, queries and reproduction](../code/README.md)
