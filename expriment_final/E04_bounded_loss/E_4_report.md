# E04 有界丢包与重试 / Bounded loss and retries

## 设计 / Design

K 是所有无人机、两种命令和两类命令协议包共享的总预算。网络只在实际丢包时递增计数，计数不会随成功交付或切换命令重置。R 控制客户端每次命令交换可用的重试次数。主矩阵固定传输 1–3、心跳关闭、ACK 超时 24，并在 N=1 和 N=3 分别检查九组 K、R 组合。

K is shared by all drones, both commands and both command packet directions. The network increments its counter only on a loss, and the count carries across successful deliveries and command changes. R sets the retry limit per command exchange. The main study uses service times of 1–3, heartbeat off and ACK timeout 24. It checks nine K and R pairs for each of N=1 and N=3.

## 恢复与失败 / Recovery and failure

在单机和三机的 18 个主配置中，ACK_TIMEOUT=24 时，P25 在 R≥K 的 12 个配置成立。R<K 的 6 个配置同时允许成功和确认失败。K 是整个协调过程的丢包上限，R 是每条命令首次发送后的重试上限。 [矩阵数据](results/analysis/outcome_matrix.json)

Across the 18 single-drone and three-drone configurations with ACK_TIMEOUT=24, P25 held in the 12 configurations with R≥K. The six configurations with R<K allowed both success and confirmation failure. K caps losses across the whole coordination attempt, and R caps retries after each initial command. [Matrix data](results/analysis/outcome_matrix.json)

![有界丢包结果矩阵 / Bounded-loss outcomes](results/figs/E04_outcome_matrix.png)

单机见证中，前两次请求分别于 t=1 和 t=25 丢失。R=2 的第三次尝试收到 ARM ACK，随后在 t=52 到达 Done。R=1 的对照在 t=48 耗尽等待预算。P28 还表明 K=2、R=1 存在丢满两包后成功的另一条执行，因此该配置同时具有可恢复路径和失败路径。

In a single-drone witness, the first two requests were lost at t=1 and t=25. With R=2, the third attempt received the ARM ACK and reached Done at t=52. With R=1, a matched sequence exhausted its wait budget at t=48. P28 also found a successful execution at K=2, R=1 that used the full loss budget. That configuration admits both recovery and failure.

![有界丢包的恢复与失败见证 / Recovery and failure witnesses under bounded loss](results/figs/E04_recovery_traces.png)

图中第三条轨迹对应 K=1、R=0。服务端在 t=3 执行 ARM，ACK 在 t=4 丢失，客户端在 t=24 失败。这说明即便总丢包数只有一个，确认失败时无人机也可能已经执行命令。图中时间从首条 ARM 请求准入算起。

The third trace has K=1 and R=0. The server executed ARM at t=3, the ACK was lost at t=4, and the client failed at t=24. Even a single lost packet can therefore leave a drone armed when confirmation fails. Time in the plot begins at the first ARM request admission.

短超时对照把 ACK_TIMEOUT 改为 14 后，即使 K=R=0，三机配置也允许确认失败。无限制丢包对照中 R=0、1、2 的 P25 均不成立。P26 的初始 Idle 反例表明启动仍由模型环境决定，P25 的完成保证从 Prepared 开始。 [对照和诊断记录](results/records.csv)

With timeout 14, the three-drone control admitted confirmation failure even at K=R=0. P25 failed for R=0, 1 and 2 under unrestricted loss. The initial Idle counterexample to P26 shows that startup remains a choice in the model environment. P25 guarantees completion once Prepared is reached. [Controls and diagnostics](results/records.csv)

## 对照结论 / Control results

主矩阵中，P01 在全部 18 组成立，所以每组都有成功路径。P25 在 R≥K 时成立，P15 同时排除了全队任一确认失败。K=0 的结果与 24 次无计数器可靠链路对照一致。短超时对照说明，还需满足等待预算的时序条件才能得到完成保证。342 次主查询与 50 次对照和诊断均得到明确结果。

P01 held in all 18 cells, establishing a possible successful execution in every setting. With R≥K, P25 held and P15 excluded confirmation failure anywhere in the fleet. The K=0 verdicts agreed with 24 checks on a reliable link without a loss counter. The short-timeout control shows that completion also depends on the timing budget. All 342 main checks and 50 controls or diagnostics returned decisive results.
