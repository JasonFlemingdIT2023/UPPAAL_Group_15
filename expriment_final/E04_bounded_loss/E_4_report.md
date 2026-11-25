# E04 有界丢包与重试 / Bounded loss and retries

在单机和三机的 18 个主配置中，ACK_TIMEOUT=24 时，P25 在 R≥K 的 12 个配置成立。R<K 的 6 个配置同时允许成功和确认失败。K 是整个协调过程的丢包上限，R 是每条命令首次发送后的重试上限。 [矩阵数据](results/analysis/outcome_matrix.json)

Across the 18 single-drone and three-drone configurations with ACK_TIMEOUT=24, P25 held in the 12 configurations with R≥K. The six configurations with R<K allowed both success and confirmation failure. K caps losses across the whole coordination attempt, and R caps retries after each initial command. [Matrix data](results/analysis/outcome_matrix.json)

![有界丢包结果矩阵 / Bounded-loss outcomes](results/figs/E04_outcome_matrix.png)

单机见证中，前两次请求分别于 t=1 和 t=25 丢失。R=2 的第三次尝试收到 ARM ACK，随后在 t=52 到达 Done。R=1 的对照在 t=48 耗尽等待预算。P28 还表明 K=2、R=1 存在丢满两包后成功的另一条执行，因此该配置同时具有可恢复路径和失败路径。 [恢复与失败轨迹](results/figs/E04_recovery_traces.png)

In a single-drone witness, the first two requests were lost at t=1 and t=25. With R=2, the third attempt received the ARM ACK and reached Done at t=52. With R=1, a matched sequence exhausted its wait budget at t=48. P28 also found a successful execution at K=2, R=1 that used the full loss budget. That configuration admits both recovery and failure. [Recovery and failure traces](results/figs/E04_recovery_traces.png)

短超时对照把 ACK_TIMEOUT 改为 14 后，即使 K=R=0，三机配置也允许确认失败。无限制丢包对照中 R=0、1、2 的 P25 均不成立。P26 的初始 Idle 反例表明启动仍由模型环境决定，P25 的完成保证从 Prepared 开始。 [对照和诊断记录](results/records.csv)

With timeout 14, the three-drone control admitted confirmation failure even at K=R=0. P25 failed for R=0, 1 and 2 under unrestricted loss. The initial Idle counterexample to P26 shows that startup remains a choice in the model environment. P25 guarantees completion once Prepared is reached. [Controls and diagnostics](results/records.csv)
