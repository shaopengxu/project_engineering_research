# 小项目开发流程规范

## 适用范围

- 3 个以内**业务**模块（技术模块如 shared/infra 不计入）
- 1-2 人开发（程序员主导）
- 开发周期 1-4 周
- 单仓库，无需多 agent 并行

### 典型适用项目

| 项目类型 | 业务模块举例 | 规模参考 |
|---------|------------|---------|
| CLI 工具 | 命令解析、业务逻辑、数据持久化 | 4-8 个命令，1-2 周 |
| REST API 服务 | 2-3 个资源的 CRUD + 资源间关联 | 10-15 个端点，2-3 周 |
| SDK / 工具库 | 核心功能、配置管理、输出格式化 | 10-20 个公开函数，1-2 周 |
| 消息消费者 | 事件处理、数据转换、存储写入 | 3-5 种事件类型，1-2 周 |
| 单页应用（无自建后端） | 2-3 个页面的状态管理和交互 | 3-5 个页面，2-3 周 |
| 浏览器扩展 | 内容脚本、后台逻辑、存储同步 | 1-2 周 |
| 自动化脚本 / 数据管道 | 数据采集、转换清洗、输出导出 | 2-3 个数据源，1 周 |

### 边界案例判断

- **"3 个业务模块"怎么数**：如果一个模块能独立开发、独立测试、用一句话说清职责，它就是一个业务模块。shared/infra/utils 等基础设施不算。
- **模块数刚好 3 个但交互复杂**：如果模块间有多对多关系或复杂的状态流转（如审批流、状态机），考虑升级到 medium-project。
- **模块数只有 1 个但代码量大**：单模块的复杂项目（如编译器前端、算法引擎）仍然适用，但 api-contracts 侧重模块的公开接口而非内部实现。

## 不适用场景

- 探索性原型（不确定做什么）→ 先做 spike 验证方向，再回来走流程
- 纯 UI 还原（无业务逻辑）→ 不需要架构设计和契约测试
- 修 bug / 小改动 → 直接改，不需要走完整流程
- 超过 3 个业务模块或需要多人并行 → 使用 medium-project 流程

## 角色定义

| 角色 | 职责 |
|------|------|
| 产品经理 | 定义需求，验收功能 |
| 技术负责人 | 技术选型，review 架构，编写 CLAUDE.md |
| Architect agent | 根据 PRD 设计架构和接口 |
| Tester agent | 根据接口契约编写测试代码 |
| Implementer agent | 根据文档和测试实现功能 |
| Reviewer agent | 对照文档 review 代码和测试 |

> 小项目中，产品经理和技术负责人可以是同一个人。

## 文档清单

| 文档 | 谁写 | 谁 Review | 是否必须 |
|------|------|-----------|---------|
| PRD (prd.md) | 产品经理 | 产品经理 | 必须 |
| CLAUDE.md | 技术负责人 | 技术负责人 | 必须 |
| 架构文档 (architecture.md) | Architect agent | 技术负责人 | 必须 |
| 接口契约 (api-contracts.md) | Architect agent | 技术负责人 | 必须 |
| 任务看板 (task-board.md) | 技术负责人 | 无需 review | 必须 |
| 测试代码 | Tester agent | 技术负责人 | 必须 |
| 业务代码 | Implementer agent | Reviewer agent | 必须 |

## 开发流程

```
Step 1: 初始化
├── 技术负责人: git init + 确定 git 策略
├── 产品经理: 编写 PRD（含验收标准）
└── 技术负责人: 编写 CLAUDE.md

Step 2: 架构设计
├── 会话1 [Architect agent]: 读 PRD → 产出 architecture.md + api-contracts.md
└── 技术负责人: review 架构文档
    ├── 通过 → 进入 Step 3
    └── 不通过 → 新会话，Architect agent 根据反馈修订

Step 3: 环境初始化 + 拆分任务
├── 技术负责人: 项目脚手架初始化（依赖安装、配置文件、目录结构）
└── 技术负责人: 根据架构文档拆 Task → 写入 task-board.md
    拆分原则：
    ├── 被依赖模块优先（shared/infra → 业务模块）
    ├── 每个 Task 对应明确的契约测试集（task-board 中标注"需通过测试"）
    ├── 有依赖关系的 Task 不能并行
    ├── 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
    └── 如果拆不到这个粒度，说明模块划分可能需要回退到 Step 2 调整

Step 4: 契约测试先行（按模块拆分，每个模块一个会话）  ← 见下方"术语说明"
├── 会话2 [Tester agent]: 读 api-contracts.md + architecture.md → 写模块A的契约测试
├── 会话3 [Tester agent]: 读 api-contracts.md + architecture.md → 写模块B的契约测试
├── ...（模块间无依赖的测试可并行）
└── 技术负责人: review 测试代码
    ├── 通过 → 进入 Step 5
    └── 不通过 → Tester agent 在新会话中根据反馈修改

Step 5: 实现 + Review（按 Task 循环推进）
└── 循环 [按 Task 依赖顺序]:
    ├── 会话N [Implementer agent]: 读文档 + 契约测试 → 写代码 → 契约测试通过
    │   └── 实现过程中为复杂内部逻辑补充单元测试，为跨模块交互补充集成测试
    ├── 会话N+1 [Reviewer agent]: 对照文档 + 测试 review 业务代码
    │   ├── LGTM → 更新 task-board，进入下一个 Task
    │   ├── MUST FIX / SHOULD FIX → Implementer agent 在新会话中修复 → 重新 Review
    │   └── 涉及架构/接口变更 → 回退到 Step 2 修订文档，按变更传播规则更新测试和相关 Task
    └── 技术负责人: 更新 task-board.md

Step 6: E2E 测试（如需要）
├── Tester agent: 根据 PRD 验收标准编写 E2E 测试，覆盖核心用户流程
├── 技术负责人: 确认 E2E 测试通过
└── 如不需要自动化 E2E → 跳过，由 Step 7 产品经理手动验收覆盖

Step 7: 验收
└── 产品经理: 对照 PRD 验收标准逐项确认
```

## 术语说明

> **契约测试（Specification Test）**：本文中的"契约测试"指基于 api-contracts.md 定义验证接口输入输出的**规格测试**，即"接口文档说什么，测试就验什么"。这**不是** Pact 风格的消费者驱动契约测试（Consumer-Driven Contract Testing）。选择"契约测试"这个名字是因为测试的依据是接口契约文档，但本质上更接近 Specification Test / Conformance Test。

## 文档变更传播规则

当 Review 或实现过程中发现需要修改已定稿的文档时：

1. **api-contracts.md 变更**
   - 标记受影响的契约测试任务为"需更新"
   - Tester agent 在新会话中更新测试代码
   - 已通过 Review 的实现如涉及变更接口，标记为"需更新"

2. **architecture.md 变更**
   - 评估是否影响模块划分和依赖关系
   - 标记受影响的实现任务为"需更新"
   - 更新 CLAUDE.md 中的项目结构（如有变化）

3. **变更记录**
   - 在 task-board.md 的完成记录中注明变更原因和受影响范围
   - commit message 标注：`docs: {变更内容}，影响范围: {受影响的任务ID列表}`

4. **变更后的执行顺序**
   - 先更新文档 → 再更新测试 → 最后更新实现
   - 按模块依赖顺序处理，被依赖的模块优先

## 测试策略

| 测试层级 | 谁写 | 什么时候写 | 依据 |
|---------|------|----------|------|
| 契约测试 | Tester agent | Step 4，实现之前 | api-contracts.md |
| 单元测试 | Implementer agent | Step 5，实现过程中 | 遇到复杂内部逻辑时补充 |
| 集成测试 | Implementer agent | Step 5，实现过程中 | 涉及跨模块调用或外部依赖时补充 |
| E2E 测试 | Tester agent | Step 6，所有 Task Review 通过后 | PRD 验收标准 |

- **契约测试**：验证接口的输入输出是否符合 api-contracts.md 的定义，在实现之前编写，是 TDD 的驱动力（术语详见"术语说明"一节）。
  - **Step 4 完成时的预期状态**：测试代码能编译/加载，但执行时全部失败（因为实现代码还不存在）。这是 TDD 的正常状态——先红后绿。
  - **技术负责人 Review 测试时**：审查的是测试用例的覆盖度和正确性，不是执行结果。
- **单元测试 / 集成测试**：Implementer agent 在实现过程中按需补充，不需要提前规划到 task-board
- **E2E 测试**：所有 Task Review 通过后，根据 PRD 验收标准覆盖核心用户流程；小项目中如不需要自动化，可跳过由产品经理手动验收代替

### Mock 策略

| 测试层级 | 模块间依赖 | 外部依赖（数据库、第三方 API） |
|---------|-----------|---------------------------|
| 契约测试 | Mock / Stub | Mock |
| 单元测试 | Mock / Stub | Mock |
| 集成测试 | 真实调用 | 真实连接或测试容器 |
| E2E 测试 | 真实调用 | 真实连接 |

- 契约测试阶段模块间互相独立，被依赖模块未实现时使用 Mock
- 集成测试使用真实模块交互，验证模块间协作是否正确

### 测试 Review Checklist（技术负责人在 Step 4 使用）

- [ ] 每条业务规则是否有对应测试用例（对照 api-contracts.md 逐条检查）
- [ ] 是否覆盖了正常流程和异常流程（错误码、边界值、空输入等）
- [ ] 测试之间是否真的独立（无共享状态、不依赖执行顺序）
- [ ] 测试注释是否标注了对应的业务规则来源
- [ ] 测试文件路径是否与 task-board.md 中规划的一致
- [ ] Mock/Stub 的使用是否符合 Mock 策略表的规定

## 会话管理

### 基本原则

- **每个角色、每个任务使用独立的新会话**。不要在一个会话中让 agent 切换角色或跨 Task 工作。
- 原因：AI agent 的上下文窗口有限，混合多个角色或任务的上下文会导致 agent 迷失方向、遗忘约定。
- CLAUDE.md 在每个会话开始时自动加载，是 agent 获取项目上下文的主要入口。

### 什么时候必须开新会话

1. **切换角色时** — 比如从 Tester agent 切换到 Implementer agent
2. **切换 Task 时** — 即使是同一个角色，不同 Task 也应该用新会话
3. **Review 不通过需要修复时** — 修复应在新会话中进行，避免 Review 的上下文干扰实现
4. **agent 表现异常时** — 如反复犯同一个错误、忽略 CLAUDE.md 的约定、输出质量明显下降

### 什么时候可以继续当前会话

- 当前 Task 的实现还没完成，且 agent 表现正常
- 正在调试一个具体的测试失败，上下文连续性有价值

### 多会话并行

- 模块间无依赖的契约测试（Step 4）可以在多个终端中并行执行
- 使用 Git Worktree 隔离并行会话，避免文件冲突：`git worktree add ../project-module-a feature/module-a`

## 目录结构

```
project/
├── CLAUDE.md
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── api-contracts.md
│   └── task-board.md
├── src/
│   └── (按架构文档组织)
└── tests/
    └── (按模块组织)
```

## Git 策略

- 分支模型：main + feature branches
- 每个 Task 一个 feature 分支
- commit 粒度：每个有意义的改动一个 commit
- commit message 格式：`<type>: <描述为什么改>`
- type: feat / fix / docs / refactor / test

## 速查：每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准（全部满足才能进入下一步） |
|------|--------|------|------|------|
| 1 | 人 | — | PRD, CLAUDE.md | PRD 包含所有模块的功能需求和验收标准；CLAUDE.md 包含技术栈和常用命令 |
| 2 | Architect Agent | PRD | architecture.md, api-contracts.md | 技术负责人确认：每个 PRD 功能点都能映射到至少一个接口；模块依赖单向无环；数据模型完整 |
| 3 | 人 | architecture.md | task-board.md, 项目脚手架 | 脚手架能运行（`npm install` 或等价命令成功）；task-board 中每个实现任务都标注了"需通过测试" |
| 4 | Tester Agent | api-contracts.md, architecture.md | 契约测试代码 | 测试代码能编译/加载；执行时失败（因实现不存在）；技术负责人确认：每条业务规则有对应测试、覆盖正常和异常流程 |
| 5 | Implementer + Reviewer Agent | 文档 + 测试 | 业务代码（逐 Task） | 当前 Task 的所有契约测试通过；Reviewer 输出 LGTM（无 MUST FIX / SHOULD FIX） |
| 6 | Tester Agent | PRD 验收标准 | E2E 测试 | E2E 测试全部通过；覆盖 PRD 中每条验收标准 |
| 7 | 产品经理 | PRD | 验收确认 | PRD 验收标准逐项确认通过 |

## 增量开发（已有项目加新功能）

本流程不仅适用于从零开始的项目。在已有项目中增加新模块或新功能时，按以下方式裁剪：

| 场景 | 起始步骤 | 可跳过 |
|------|---------|--------|
| 新增业务模块 | Step 2（更新 architecture.md 和 api-contracts.md） | Step 1 的 git init 和 CLAUDE.md 初始化；Step 3 的脚手架初始化 |
| 已有模块增加接口 | Step 2（仅更新 api-contracts.md 中对应模块） | Step 1 全部；Step 3 的脚手架初始化 |
| 重构不改接口 | Step 5（直接实现 + Review） | Step 2, 4（接口没变，契约测试应该已存在且不需要改） |
| 修复 bug | 不走流程 | 直接改代码、补测试、提交 |

关键原则：**变了什么文档，就从那个文档对应的步骤开始往后走**。改了接口 → 从 Step 4 更新测试开始；只改实现 → 从 Step 5 开始。

## 常见故障与恢复

### Agent 会话中途崩溃

1. 检查 git 状态：`git status` 和 `git log` 确认最后一次 commit 的内容
2. 如果有未提交的改动且质量可接受 → 提交后在新会话中继续下一个 Task
3. 如果有未提交的改动但质量不确定 → `git stash` 保存现场，在新会话中重新开始当前 Task，完成后对比 stash 内容
4. 如果没有未提交的改动 → 直接在新会话中重新开始当前 Task

### 实现过程中发现架构有问题

1. 停止当前 Task 的实现
2. 在 task-board.md 中记录问题和受影响的 Task
3. 回退到 Step 2：在新会话中让 Architect agent 修订文档
4. 按变更传播规则处理：文档 → 测试 → 实现

### 契约测试与 api-contracts.md 不一致

1. 以 api-contracts.md 为准（文档是 single source of truth）
2. 在新会话中让 Tester agent 修正测试
3. 如果是 api-contracts.md 本身有问题 → 先修文档，再修测试

### 多个 Task 间出现意外的依赖冲突

1. 检查是否存在未在 task-board.md 中声明的隐式依赖
2. 更新 task-board.md 的依赖关系
3. 调整执行顺序，确保被依赖的 Task 先完成

## CI 集成建议

小项目不一定需要 CI，但如果配置了 CI，建议按以下策略处理：

- **Step 4 期间**：契约测试预期失败，不要将其加入 CI 必过检查
- **Step 5 每个 Task 完成后**：将该 Task 对应的契约测试加入 CI 必过检查（逐步开启，而非一次性全部开启）
- **Step 6 之后**：E2E 测试加入 CI 必过检查
- **CI 最小配置**：`lint` + `已完成 Task 的契约测试` + `单元测试`
