# 结果 / Results

24 次开关对照、8 次设置对照、4 条诊断见证、1 次 DFS 安全检查、3 次延长 BFS 补查及 1 条 E06 同模型的决定性核查。 / 24 activation checks, 8 settings checks, 4 diagnostics, 1 DFS safety check, 3 extended BFS checks and 1 decisive check reused from E06.

| 文件或目录 / File or directory | 内容 / Contents |
|---|---|
| [records.csv](records.csv) | 逐查询参数、结论、耗时、状态数和相关证据。 / Parameters, verdict, runtime, state counts and available evidence for each query. |
| [analysis](analysis/) | 报告与绘图使用的汇总、矩阵和轨迹摘要。 / Summaries, matrices and trace data used by the report and figures. |
| [延长验证 / Extended verification](analysis/activation_followup.json) | 原始 BFS、延长 BFS 与最终判定所用证据。 / Original BFS, extended BFS and evidence for the final verdicts. |
| [traces](traces/) | 对应诊断性质的 UPPAAL 见证或反例。 / UPPAAL witnesses or counterexamples for diagnostic properties. |

## 图 / Figures

- 心跳开关对照 / Matched heartbeat activation comparison · [PNG](figs/E05_activation.png) · [SVG](figs/E05_activation.svg)
- 周期与首次释放偏移 / Period and first-release offset · [PNG](figs/E05_settings.png) · [SVG](figs/E05_settings.svg)
- 三机无丢包失败轨迹 / Three-drone failure trace without packet loss · [PNG](figs/E05_failure_timeline.png) · [SVG](figs/E05_failure_timeline.svg)

[模型、查询与复现 / Models, queries and reproduction](../code/README.md)
