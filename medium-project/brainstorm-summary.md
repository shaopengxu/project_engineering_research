# 中型项目开发流程 — 头脑风暴总结

## 一、中型项目的定义

| 维度 | 小型项目 | 中型项目 |
|------|---------|---------|
| 业务模块 | ≤ 3 个 | 4-8 个 |
| 开发人数 | 1-2 人 | 2-4 人 |
| 开发周期 | 1-4 周 | 4-12 周 |
| 代码量 | < 10K 行 | 10K-50K 行 |
| 仓库 | 单仓库 | 单仓库或 monorepo |
| 模块关系 | 树形（单向依赖链） | 图状（多对多、事件级联） |
| Agent 并行 | 不需要 | 需要 2-4 个 agent 并行 |

### 典型中型项目

- 多资源 REST API（用户 + 订单 + 支付 + 库存 + 通知）
- 全栈应用（前端 SPA + 后端 API + 管理后台）
- 多租户 SaaS 后端
- 数据处理管道（采集 + 清洗 + 转换 + 存储 + API）
- 微信小程序 + 后端服务
- 开发者工具链（CLI + SDK + 文档生成器）

---

## 二、核心矛盾：小项目的三个根本假设在中型项目中失效

### 假设 1："一个 agent 能理解全局"

小项目的全部文档（PRD + architecture + api-contracts + CLAUDE.md）加起来不到 2000 行，一个 agent 会话能轻松装下。中型项目的文档量是 2-3 倍，加上 8 个模块的代码，单个 agent **无法同时持有全局上下文**。

**崩溃表现**：Architect agent 设计 8 个模块的架构时顾此失彼；Implementer agent 不了解其他模块的约定导致接口不兼容。

### 假设 2："串行执行就够了"

小项目逐 Task 串行推进，不需要并行。中型项目 20-40 个 Task 串行执行要几个月，必须多人/多 agent 并行。但并行带来了文件冲突、共享状态竞争、跨模块变更通知等一系列小项目不存在的问题。

**崩溃表现**：task-board.md 成为并发写入瓶颈；两个 agent 同时改 shared/ 导致冲突；一个模块改了接口，另一个模块的 agent 不知道。

### 假设 3："一次性交付"

小项目 1-4 周一口气做完，不需要中间迭代。中型项目 4-12 周的周期内，需求会变、优先级会调、甚至人员会换。没有迭代机制，项目后期发现方向偏了就来不及了。

**崩溃表现**：第 6 周发现第 2 周的架构决策有问题，但已经 5 个模块基于它实现了；产品经理 12 周后才第一次验收，发现核心流程不对。

---

## 三、各维度的变化方向

### 3.1 架构设计：从"一次产出"到"分层设计"

**问题**：小项目一个 Architect agent 会话产出所有文档，中型项目的信息量超出单次会话能力。

**方向**：

```
小项目：
  Architect agent → architecture.md + api-contracts.md（一次完成）

中型项目：
  Step 2a: System Architect agent → architecture.md（系统级：模块划分、模块间通信、数据流向）
  Step 2b: Module Designer agent × N → module-design/{module}.md（每个模块独立会话）
  Step 2c: API Designer agent → api-contracts.md（基于 2a + 2b 定义所有模块间接口）
```

- architecture.md 只关注系统级：模块划分、依赖关系图、部署架构、跨模块数据流
- 每个模块的详细设计（内部分层、关键类、模块内数据模型）下沉到 module-design/{module}.md
- api-contracts.md 仍然是所有模块间接口的 single source of truth，但新增 **consumers 字段**（谁在消费这个接口）和**接口依赖矩阵**

### 3.2 文档体系：从"扁平"到"分层"

**小项目文档**：

```
docs/
├── prd.md
├── architecture.md
├── api-contracts.md
└── task-board.md
```

**中型项目文档**：

```
docs/
├── prd.md                        # 不变
├── architecture.md               # 收缩为系统级
├── api-contracts.md              # 新增 consumers 字段和接口依赖矩阵
├── module-design/                # 新增：模块级详细设计
│   ├── user.md
│   ├── order.md
│   └── ...
├── task-board.md                 # 结构升级（见 3.5）
└── decision-log.md               # 新增：架构决策记录（轻量级 ADR）
```

**CLAUDE.md 分层**：

```
CLAUDE.md                         # 全局（< 100 行）：技术栈、Git 规则、架构概览、全局约定
src/modules/user/CLAUDE.md        # 模块级（< 50 行）：该模块的职责、接口、依赖、特殊规范
src/modules/order/CLAUDE.md
...
```

agent 处理某个模块时，只加载全局 CLAUDE.md + 该模块的 CLAUDE.md + 相关的 api-contracts 部分，而非全部文档。

### 3.3 角色演进：新增角色 + 职责调整

**新增角色**：

| 角色 | 职责 | 为什么需要 |
|------|------|-----------|
| Tech Lead Agent | 跨模块协调：接口变更影响评估、并行 Task 冲突检测 | 技术负责人的跨模块协调工作量在中型项目中成为瓶颈 |
| Integration Tester Agent | 编写模块间集成测试（真实调用，不 Mock） | 小项目的集成测试"按需补充"在中型项目中不够 |

**现有角色调整**：

| 角色 | 小项目 | 中型项目 |
|------|--------|---------|
| Architect Agent | 一次产出所有架构文档 | 分阶段：系统架构 → 模块设计 → 接口契约 |
| Tester Agent | 契约测试 + 可选 E2E | 契约测试 + 集成测试规划 + 必须的 E2E |
| Reviewer Agent | 逐 Task review | 逐 Task review + 模块完成后跨模块 review |
| 技术负责人（人） | 全部 review + 任务拆分 + 状态流转 | 系统级 review + 跨模块 review；模块级 review 可委托给 Reviewer Agent |

**人类角色瓶颈缓解**：

- 技术负责人：分层 review（只做系统级和跨模块），模块内 review 委托 agent
- 产品经理：分批验收（每完成一组模块验收一批），而非最后一次性验收
- 引入"模块负责人"概念：如果有多个开发者，每人负责 1-2 个模块

### 3.4 流程步骤：从 7 步到 ~10 步

```
Step 1: 初始化（同小项目）
├── PRD, CLAUDE.md

Step 2a: 系统架构设计（新增拆分）
├── System Architect agent → architecture.md（系统级）
└── 技术负责人 Review

Step 2b: 模块详细设计（新增）
├── Module Designer agent × N → module-design/{module}.md（可并行）
└── 技术负责人 / 模块负责人 Review

Step 2c: 接口契约定义（新增拆分）
├── API Designer agent → api-contracts.md（含 consumers + 依赖矩阵 + 追溯表）
└── 技术负责人 Review

Step 3: 环境初始化 + 拆分任务
├── 脚手架初始化
├── 任务拆分为 DAG（标注并行/串行关系和关键路径）
└── 集成测试规划（识别关键路径，规划 L2 集成测试用例）

Step 4: 契约测试先行（可多模块并行）
├── Tester agent × N → 契约测试代码（每个模块独立会话，可 worktree 并行）
└── 技术负责人 Review

Step 5: 实现 + Review（多模块并行推进）
├── 共享层（shared/infra）串行先行
├── 业务模块并行实现（每个模块一个 worktree）
├── 每个 Task: 契约测试通过 + L1 模块内集成测试通过
├── Reviewer agent 逐 Task review
├── 关键路径模块就绪时 → 插入 L2 集成测试 Task
└── 技术负责人做跨模块 review（接口变更时）

Step 6: E2E 测试（核心路径必须）
├── 分阶段编写：某条关键路径的模块完成后即可开始
└── 不等所有模块完成，边做边测

Step 7: 验收（分批）
├── 产品经理按模块组分批验收
└── 最终全量验收
```

### 3.5 多 Agent 并行协作

**Git 策略**：

```
小项目：main + feature branches（每 Task 一个分支）

中型项目：main + develop + module branches
├── develop: 集成分支，所有已完成模块合入此处
├── module/{name}: 每个模块一个长期分支
├── feature/{task-id}: 每个 Task 一个短期分支（从 module 分支创建）
└── 合并顺序：feature → module → develop → main
```

**并行隔离**：Git Worktree，每个并行 agent 一个独立工作目录。

**共享状态管理**：

- task-board.md 由技术负责人独占更新，agent 通过状态报告文件（`docs/status-reports/{task-id}.md`）异步汇报
- shared/ 代码的修改需要技术负责人审批，不允许 Implementer agent 直接改
- 接口变更通知依赖 api-contracts.md 中的 consumers 字段自动判断影响范围

**任务调度**：

- task-board.md 新增"并行调度计划"和"关键路径"标注
- 阻塞处理优先级：找可替代 Task → 用 mock 绕过 → 暂停等待
- 技术负责人约 30-50% 时间用于调度协调

### 3.6 测试策略升级

**测试分层变化**：

| 测试层级 | 小项目 | 中型项目 | 变化原因 |
|---------|--------|---------|---------|
| 契约测试 | 必须 | 必须 + consumers 显式化 | 接口更多，变更影响范围需要自动判断 |
| 单元测试 | 按需 | 按需（不变） | |
| L1 模块内集成 | 按需 | **必须** | 模块内 controller→service→repository 的真实串联需要验证 |
| L2 关键路径集成 | 不存在 | **必须** | 多模块协作的核心路径必须验证真实调用 |
| E2E 测试 | 可选 | **核心路径必须** | 模块间交互路径多，手动验收无法覆盖 |
| 回归测试 | 不需要 | **按影响范围分级执行** | 全量测试时间变长，需要精准回归 |

**测试目录结构升级**：

```
tests/
├── contracts/          # 契约测试（按模块组织）
├── unit/               # 单元测试（按模块组织）
├── integration/        # 集成测试（L1 按模块、L2 按路径）
├── e2e/                # E2E 测试（按用户流程）
└── fixtures/           # 共享测试数据（工厂函数，非硬编码）
```

**CI 分层流水线**：

```
Layer 1 (每次 push, < 2min):     lint + 受影响模块的契约/单元测试
Layer 2 (PR 创建/更新, < 10min): 全量契约 + 单元 + L1/L2 集成测试
Layer 3 (合入 main, < 30min):    Layer 2 + E2E 测试
```

### 3.7 Review 机制分层

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| Task Review | 每个 Task 完成 | Reviewer Agent | 功能正确性、代码规范 |
| 模块 Review | 模块所有 Task 完成 | Reviewer Agent（新 prompt） | 模块内一致性 |
| 跨模块 Review | 涉及跨模块变更 | 技术负责人 | 接口一致性、依赖方向 |
| 架构 Review | 架构变更提议 | 技术负责人 + 相关开发者 | 决策合理性和影响范围 |

---

## 四、新增模板清单

| 模板 | 用途 | 对应步骤 |
|------|------|---------|
| module-design/{module}.md | 模块详细设计 | Step 2b |
| decision-log.md | 架构决策记录 | 贯穿全流程 |
| 模块级 CLAUDE.md | 模块级 agent 配置 | Step 3 |
| integration-test-plan（在 task-board 中） | 集成测试规划 | Step 3 |
| status-report 模板 | agent 异步状态汇报 | Step 5 |
| 新增 agent prompts | System Architect / Module Designer / Integration Tester / 跨模块 Reviewer / Tech Lead | 各步骤 |

---

## 五、优先级排序

如果从小项目流程演进到中型项目流程，建议按以下优先级逐步引入：

| 优先级 | 变化项 | 理由 |
|--------|-------|------|
| **P0** | 架构设计分层（系统 → 模块 → 接口） | 支撑所有后续变化的基础 |
| **P0** | CLAUDE.md 分层（全局 + 模块级） | 解决 agent 上下文溢出问题 |
| **P0** | 并行 Task 编排 + Git Worktree 策略 | 多人并行开发的基本保障 |
| **P1** | 集成测试从"按需"升级为"L1/L2 必须" | 模块间接口兼容性的核心保障 |
| **P1** | api-contracts.md 增加 consumers + 依赖矩阵 | 变更传播从"人脑判断"变为"查文档" |
| **P1** | Review 分层（Task / 模块 / 跨模块） | 多模块项目的质量门禁 |
| **P2** | E2E 测试升级为核心路径必须 | 验收质量保障 |
| **P2** | CI 分层流水线 | 反馈速度保障 |
| **P2** | decision-log.md | 长周期项目的决策追溯 |
| **P3** | Tech Lead Agent 角色 | 可先由人承担，后续再 agent 化 |
| **P3** | 分批验收机制 | 降低最终验收风险 |

---

## 六、待决问题

1. **模块详细设计文档 vs 代码注释**：module-design/{module}.md 是否会成为维护负担？还是应该只在 architecture.md 中多写一些，把模块细节留给代码？

2. **并行度的上限**：2-4 个 agent 并行时技术负责人可控；如果 4+ 个 agent 并行，调度复杂度是否需要自动化工具支撑？

3. **task-board.md 的可扩展性**：20-40 个 Task 的 Markdown 文件是否仍然合适？是否需要更结构化的格式（YAML/JSON）或外部工具？

4. **Consumer-Driven Contract Testing**：当前结论是单仓不需要 Pact 风格 CDCT。如果未来演进到多仓部署，什么时候是引入 Pact 的正确时机？

5. **增量开发的起始点判断**：中型项目中一个功能可能横跨 3 个模块，如何判断增量开发应该从哪个步骤开始、影响哪些模块？

6. **module-design 和 api-contracts 的边界**：模块内部接口（如 service 层暴露给 controller 层的函数）放在 module-design 里还是 api-contracts 里？

7. **迭代/里程碑机制**：12 周的项目是否需要引入 2-3 周一个迭代的节奏？如果引入，流程的 7 个步骤如何映射到迭代中？

8. **Monorepo 场景**：如果中型项目采用 monorepo（如 Turborepo/Nx），模块级 CLAUDE.md、模块级测试、CI 策略是否需要额外适配？
