# 结果 / Results

16 次基线查询、216 次网格查询、5 条补充记录 / 16 reference queries, 216 grid queries and 5 supporting records.

| 文件或目录 / File or directory | 内容 / Contents |
|---|---|
| [records.csv](records.csv) | 逐查询参数、结论、耗时、状态数和相关证据。 / Parameters, verdict, runtime, state counts and available evidence for each query. |
| [analysis](analysis/) | 报告与绘图使用的汇总、矩阵和轨迹摘要。 / Summaries, matrices and trace data used by the report and figures. |
| [traces](traces/) | 对应诊断性质的 UPPAAL 见证或反例。 / UPPAAL witnesses or counterexamples for diagnostic properties. |

## 图 / Figures

- 重试触发和重试耗尽 / Reachability of retry triggers and exhaustion · [PNG](figs/E02_heatmaps.png) · [SVG](figs/E02_heatmaps.svg)
- 基线迟到 ACK / Late ACK in the reference configuration · [PNG](figs/baseline_late_ack.png) · [SVG](figs/baseline_late_ack.svg)
- 无丢包确认失败 / Confirmation failure on a reliable link · [PNG](figs/reliable_failure.png) · [SVG](figs/reliable_failure.svg)

[模型、查询与复现 / Models, queries and reproduction](../code/README.md)
