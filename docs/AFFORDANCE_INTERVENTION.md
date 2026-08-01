# Affordance 干预实验:结果与统一叙事(2026-08-01)

实验代码与全部 run 落盘在 `/data/home/yuhan/affordance_exp/`(自包含,vendored owf
metaharness 基座,commit a01e22d;详细决策日志见该目录 WORKLOG.md / PROTOCOL.md)。
本文档是给论文用的结果快照与叙事定案。

## 1. 设计

- 统一基座:同一 meta-loop / prompt 骨架 / 候选表示(自由 .mjs,core.runAgentNode)/
  SUT(deepseek-v4-flash)。3 域(realmath, bcplus, appworld)× 2 臂 × 2 proposer
  (codex gpt-5.6-terra;kimi CLI headless, kimi-k2.7-coding-highspeed)= 12 run,
  每 run 10 迭代,单 seed,manipulation check 全 PASS。
- **bare 臂**:rep contract 剥除 decomposition/Promise.all/hooks 提及(机制功能仍在,
  仅不告知);**afford 臂**:contract 原样 + OPTIMIZABLE DIMENSIONS 目录(prompt/预算/
  schema/拓扑操作符 CHAIN·ENSEMBLE·REVIEW·RECOVERY·ROUTER/hooks/glue,6 维完整定义,
  model 等标 FIXED)。两臂其余逐项相同。
- 判读(冻结于见数据前):域级三指标(冠军节点数 / 节点变化转移率 / 多节点最长连续)
  ≥2/3 afford 更高 → 域阳性;分数只报告不判读(单 seed)。

## 2. 主结果(臂间判定)

| 域 | codex | kimi |
|---|---|---|
| realmath | 阳性 3/3(冠军 2 节点 .680 vs bare .600) | 阳性 3/3(节点 2/3,转移 .1/.3,streak 8/10) |
| bcplus | 阳性 2/3(双臂冠军=种子 .607) | 阳性 3/3(节点 1/4,转移 .5/.8,冠军 .607 vs .640) |
| appworld | 节点阴性;hooks 候选池 0 vs 9/10 | 节点阴性(双臂全平);hooks 0/11 vs 10/11 |

- codex bare:0/30 候选多节点,83% 转移为纯 prompt/param;afford 46% 结构性。
- kimi bare:先验更宽,realmath/bcplus 自发多节点+hook,但臂间方向仍 afford 更高
  → 干预效应叠加在先验之上。
- appworld 两 proposer 同构:节点全平、hooks 完全由 afford 独占 → 各域走的维度不同。

## 3. 会话级溯源(关键控制)

- kimi bcplus_bare iter_001 完整轨迹:读 rollout journal → 诊断 no_answer → 主动
  find/Read `harness/executor/src/agent-node.ts`(拿到 hooks 全 API)→ 写 search+answer
  两段链。全部结构变体的动机 = 修某个观察到的失败类。
- **codex 也读了同一份源码**(agent-node.ts 独有符号 fireHook 出现在其 bare 各域 2-3 个
  会话)却 30 个 bare 候选零多节点;kimi 在 appworld bare 读了(×3)也保持单节点。
  → 约束不是信息访问,也不只是检查与否,而是 contract 的合法化/salience。
- 种子注释泄漏仅限 realmath("add nodes, add hooks" 一行);bcplus/appworld 种子干净。
  bare 的操作定义如实写为 "editable-but-undocumented",非零提及。

## 4. 采用梯度(核心图表素材)

| 结构类型 | 材料索引 | 采用者 |
|---|---|---|
| prompt/param 修补 | 失败直接索引 | 全部臂(bare 主体) |
| verify / rescue 追加 | 失败索引+先验模板(双重) | kimi bare, codex afford |
| 线性链拆分(search→answer) | 先验模板 | kimi bare |
| planner / critic / second / 分层 fallback | 仅目录 | 仅 afford |
| ensemble(Promise.all)/ router | 目录点名但无失败索引 | 无人 |

kimi bare 的 9 个多节点变体 = 单一失败索引模板族,分数全低于种子(.22–.54),冠军=种子;
afford 冠军 evidence_commit(primary/critic/recovery/fallback 四节点).640 超种子。

## 5. Heldout(test)结果(只报告,不进判读)

| 域(n) | baseline | codex bare | codex afford | kimi bare | kimi afford |
|---|---|---|---|---|---|
| realmath (169) | .426@164k | .491@73k | .538@112k | .538@106k | .538@**42k** |
| bcplus (780) | .606@331k (160 超预算) | =种子 | =种子 | =种子 | **.669**@199k (3 超预算) |
| appworld (372) | .774 | **.812** | .734 | .790 | .750 |

- bcplus:结构收益泛化正例(+.063,超预算 160→3,便宜 40%)。
- appworld:val 高分(.933/.844)全部回落,两 afford 冠军低于 baseline —— 45 题训练集
  过拟合;正演示了协议"分数不进判读"的必要性。

## 6. 统一命题(论文叙事定案)

**Meta-agent 的有效搜索空间由其"优化材料"张成,而非编辑权限。** 材料三来源:被检查的
证据(读取有界使其变薄,冻结集 access≠inspect 17/17)、接口词表(contract 点名什么)、
模型先验(模板库)。证据由当前设计生成,失败只以现有结构的坐标表达 —— 故未点名时优化
是**失败驱动的定点修补**(已有→验证 / 已有→rescue 循环,或先验线性拆分);planner、
独立 critic 这类维度的价值不体现在任何单条失败中,只有目录能把它们送进 proposal 分布。
干预不提供新能力或新信息(两 proposer 都读过源码),提供的是**材料与合法化**。

写作红线:(1) 命题写成分布式("编辑分布集中于被索引维度;显式定义使分布移动"),
不写"从不探索"(kimi bare 反例);(2) 分数不写成干预收益(appworld 反例);
(3) ensemble/router 无人采用如实报告为干预边界。

后续方向(讨论中):把上述机制形式化为搜索动力学(proposal 分布对材料的条件化、
失败信号在非实例化维度上无分量),待推导。
