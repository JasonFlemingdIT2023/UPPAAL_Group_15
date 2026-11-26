# 结果 / Results

100 条原实验记录，完成性补充 4 条查询和 1 条停止记录，原调度心跳进展补充 7 条查询和 1 条停止记录。 / 100 original records, 4 completion follow-up queries and 1 stopped run, plus 7 original-heartbeat follow-up queries and 1 stopped run.

| 文件或目录 / File or directory | 内容 / Contents |
|---|---|
| [records.csv](records.csv) | 逐查询参数、结论、耗时、状态数和相关证据。 / Parameters, verdict, runtime, state counts and available evidence for each query. |
| [analysis](analysis/) | 报告与绘图使用的汇总、矩阵和轨迹摘要。 / Summaries, matrices and trace data used by the report and figures. |
| [traces](traces/) | 对应诊断性质的 UPPAAL 见证或反例。 / UPPAAL witnesses or counterexamples for diagnostic properties. |
| [Prepared → Done](proof/Prepared_to_Done.md) | ACK 优先模型的完成性质和两项验证输出。 / Completion proof for ACK priority and both verifier outputs. |
| [原调度心跳进展 / Original heartbeat progress](proof/Original_heartbeat_progress.md) | 原调度待发心跳最终准入的证明和 P06/P46 输出。 / Proof of eventual admission under original scheduling and the P06/P46 outputs. |

## 图 / Figures

- 原调度和 ACK 优先关键性质 / Key properties under original and ACK-priority scheduling · [PNG](figs/E06_outcomes.png) · [SVG](figs/E06_outcomes.svg)
- 原调度失败与优先调度回复见证 / Original failure and ACK-priority reply witnesses · [PNG](figs/E06_reply_comparison.png) · [SVG](figs/E06_reply_comparison.svg)

[模型、查询与复现 / Models, queries and reproduction](../code/README.md)
