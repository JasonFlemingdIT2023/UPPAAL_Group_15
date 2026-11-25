# 实验部分 AI 使用记录 / AI assistance for the experiments

| 环节 / Stage | 用户提示摘录 / Prompt excerpts | AI 辅助工作 / Assistance |
|---|---|---|
| 确定实验路线 / Experiment planning | “请你思考怎么开展实验，怎么完成高质量的实验” | 读取小组实验计划，整理基线、查询、控制变量与证据保存要求。 / Read the group plan and organize the reference, queries, controls and evidence. |
| 执行计划实验 / Running the planned studies | “接下来要做什么实验，请你推进一下” · “现在请你做下一个实验E01” · “请你继续推进E05” · “现在请你做一下E04” | 编写模型生成和验证脚本，运行 UPPAAL，汇总逐查询结果并提取诊断轨迹。 / Write generation and verification scripts, run UPPAAL, aggregate verdicts and extract diagnostics. |
| 设计改进对照 / Scheduling experiment | “迟到 ACK 修复的消融实验就算了吧……应该往前改进” · “ok，请你做一下” | 保留迟到 ACK 处理，构建 ACK 优先与被动标记对照，检查确认失败、回复等待及心跳进展。 / Retain late-ACK handling, implement priority and passive-flag controls, and check confirmation failure, reply wait and heartbeat progress. |
| 继续完成性验证 / Completion proof | “所以现在增加验证时间就可以证明了对吧？是的话请你尝试证明” | 延长直接查询，构建 Prepared 边界及后续验证模型，归档两项 UPPAAL 结果与覆盖论证。 / Extend the direct check, build the boundary and continuation checks, and archive the two verdicts and coverage argument. |
| 整理交付 / Packaging | “所有的实验部分都得在expriment_final里有完整内容” · “报告的书写不要有防御性描述” | 整理代码、输入、验证记录、图表和双语报告，脱离原仓库试跑复现入口。 / Package code, inputs, verifier records, figures and bilingual reports, and test replay outside the source repository. |

报告中的结果可追溯至各实验的原始 UPPAAL 记录。E06 的两项机器检查和连接它们的状态覆盖论证见证明说明。 [E06 证明](E06_ack_priority/results/proof/Prepared_to_Done.md)

The reports trace their findings to the original UPPAAL records. The E06 proof documents the two machine checks and the state-coverage argument connecting them. [E06 proof](E06_ack_priority/results/proof/Prepared_to_Done.md)
