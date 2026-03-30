# 中型项目并行开发分析

> 本文聚焦于从小型项目流程升级到中型项目时，并行化带来的新问题和应对策略。

## 适用范围（初步定义）

- 4-8 个业务模块
- 2-5 人开发（每人可驱动 1-3 个 agent 并行）
- 单仓库，需要多 agent 并行
- 同时活跃的 Implementer agent: 2-5 个

---

## 1. 并行开发模式

### 1.1 核心问题

小型项目中，Implementer agent 是串行执行的——一个 Task 完成、Review 通过后再启动下一个。中型项目需要多个 Implementer agent 同时工作在不同模块上，这带来三个根本性变化：

1. **文件系统冲突**：多个 agent 同时修改同一文件系统中的文件
2. **Git 状态冲突**：多个 agent 同时 commit/push，Git 操作互相干扰
3. **语义冲突**：两个 agent 各自通过了自己的测试，合并后却互相破坏

### 1.2 Git Worktree 方案（推荐）

**核心策略：每个并行 agent 运行在独立的 Git Worktree 中。**

```
project/                          # 主工作树，技术负责人使用
├── .git/                         # 唯一的 .git 目录
├── CLAUDE.md
├── docs/
│   ├── architecture.md
│   ├── api-contracts.md
│   └── task-board.md
└── src/

../project-worktree-module-a/     # Worktree A: Implementer Agent A
├── (指向 project/.git)
└── (feature/module-a 分支的完整文件)

../project-worktree-module-b/     # Worktree B: Implementer Agent B
├── (指向 project/.git)
└── (feature/module-b 分支的完整文件)
```

操作流程：

```bash
# 技术负责人创建 worktree（在 Step 5 开始前）
cd project
git branch feature/module-a
git branch feature/module-b
git worktree add ../project-worktree-module-a feature/module-a
git worktree add ../project-worktree-module-b feature/module-b

# 各 agent 在各自 worktree 中独立工作
# Agent A 在 ../project-worktree-module-a/ 中 commit
# Agent B 在 ../project-worktree-module-b/ 中 commit

# 完成后合并
cd project
git merge feature/module-a
git merge feature/module-b

# 清理
git worktree remove ../project-worktree-module-a
git worktree remove ../project-worktree-module-b
```

**为什么不用其他方案：**

| 方案 | 问题 |
|------|------|
| 同目录多分支切换 | 多 agent 无法同时工作，需要排队 |
| git clone 多副本 | 没有共享 .git，分支管理割裂，合并麻烦 |
| 单分支多 agent | 文件冲突、commit 交叉，灾难性 |
| monorepo + 多 package | 过度工程，中型项目不需要 |

### 1.3 分支策略

```
main
 ├── develop                     # 集成分支（可选，见 1.4 讨论）
 │    ├── feature/shared-core    # 共享层（最先开发，最先合并）
 │    ├── feature/module-a       # 业务模块 A
 │    ├── feature/module-b       # 业务模块 B
 │    └── feature/module-c       # 业务模块 C
 └── (hotfix 略)
```

**分支规则：**

- 每个 **模块** 一个 feature 分支（不是每个 Task 一个——中型项目 Task 数量多，一个模块内的多个 Task 在同一分支上串行完成）
- 共享层（shared/infra）有自己的 feature 分支，且必须最先合并
- 合并策略：`--no-ff`（保留合并记录，方便追溯）
- 分支命名：`feature/{module-name}`

**与小型项目的差异：**

| 维度 | 小型项目 | 中型项目 |
|------|---------|---------|
| 分支粒度 | 每个 Task 一个分支 | 每个模块一个分支 |
| 合并频率 | Task 完成即合并 | 模块完成或阶段性合并 |
| 合并方向 | feature → main | feature → develop → main |
| 是否需要 worktree | 偶尔（测试并行时） | 必须（实现并行时） |

### 1.4 是否需要 develop 分支

**推荐使用 develop 分支**，原因：

1. main 始终保持可部署状态
2. develop 作为集成分支，可以发现模块间冲突而不污染 main
3. 集成测试在 develop 上运行，通过后再合并到 main

但如果团队很小（2 人）且 CI 完善，可以省略 develop，直接 feature → main。

### 1.5 文件冲突的预防

**架构层面预防（最重要）：**

- 模块目录物理隔离：`src/modules/module-a/` 和 `src/modules/module-b/` 不应该有交叉文件
- 共享层（shared/）的修改权限收紧：只有 shared 模块的 agent 可以修改，业务模块 agent 只能读
- 入口文件（app.ts / main.py）的修改由技术负责人手动做，不交给 agent

**Git 层面预防：**

- Worktree 隔离消除了物理文件冲突
- 合并时的语义冲突通过集成测试发现（见第 2 节）

**剩余高风险文件（需要人工协调的）：**

- `package.json` / `go.mod` — 多模块同时新增依赖
- 数据库 migration 文件 — 多模块同时新增 migration
- 路由注册文件 — 多模块同时注册新路由
- 配置文件 — 多模块需要不同的配置项

**应对策略：** 这些文件的修改集中在模块开发的开头和结尾，由技术负责人在合并时统一处理，不让 agent 自行修改。

---

## 2. 模块间集成

### 2.1 集成时机

```
Phase 1: 共享层开发（串行）
  shared/infra → 合并到 develop → 所有 worktree rebase

Phase 2: 业务模块并行开发（并行）
  module-a, module-b, module-c 各自在 worktree 中开发
  每个模块内部按 Task 串行推进

Phase 3: 逐模块集成（串行化的合并）
  module-a → 合并到 develop → 跑集成测试
  module-b → rebase develop → 合并到 develop → 跑集成测试
  module-c → rebase develop → 合并到 develop → 跑集成测试
  （顺序按依赖关系：被依赖的先合并）

Phase 4: 全量集成测试 + E2E
  在 develop 上跑全部测试
  通过 → 合并到 main
```

**关键决策：逐模块合并，而非 big-bang 一次性合并。** 每合并一个模块就跑一次集成测试，问题定位范围小。

### 2.2 接口兼容性的提前发现

**静态手段（开发阶段）：**

1. **TypeScript / 强类型语言**：共享类型定义在 `shared/types/` 中，各模块 import 使用。类型变更在编译期被所有消费者发现。
2. **接口版本号**：api-contracts.md 中每个接口标注版本号。接口变更时版本号递增，消费方看到版本不匹配就知道需要更新。
3. **契约测试作为守护**：每个模块的契约测试在合并前重新运行。如果 shared 层接口变了，依赖它的模块的契约测试会失败。

**动态手段（集成阶段）：**

1. **集成测试**：在 develop 分支上，使用真实模块交互（不 mock），验证模块间调用是否正常。
2. **CI 自动检测**：每次向 develop 合并时，CI 跑全量测试。

### 2.3 集成测试的责任归属

| 测试类型 | 谁写 | 在哪跑 | 什么时候 |
|---------|------|-------|---------|
| 模块内契约测试 | Tester agent | 各自 worktree | 实现阶段（持续） |
| 模块内单元测试 | Implementer agent | 各自 worktree | 实现阶段（按需） |
| 跨模块集成测试 | Implementer agent（调用方模块的 agent）| develop 分支 | 模块合并后 |
| E2E 测试 | Tester agent | develop 分支 | 所有模块合并后 |

**跨模块集成测试的触发时机：** 当模块 B 依赖模块 A，且模块 A 已合并到 develop 时，模块 B 的 agent 在 rebase develop 后编写并运行跨模块集成测试。

---

## 3. 共享状态和依赖管理

### 3.1 task-board.md 的并发修改

**问题：** 小型项目中，task-board.md 由技术负责人独占更新。中型项目中，如果多个 agent 同时完成 Task 并需要更新状态，怎么办？

**方案：维持技术负责人独占更新的策略，但优化流程。**

具体做法：
1. Agent 完成 Task 后，在自己的 worktree 中创建一个状态报告文件，而不是直接修改 task-board.md
2. 技术负责人定期（或收到通知后）汇总状态报告，统一更新 task-board.md

```
project/
├── docs/
│   ├── task-board.md              # 只有技术负责人修改
│   └── status-reports/            # agent 写入状态报告
│       ├── module-a-impl-003.md   # "Impl-003 完成，所有测试通过"
│       └── module-b-impl-005.md   # "Impl-005 阻塞，原因: ..."
```

**替代方案（如果项目更大）：** 把 task-board 从 markdown 迁移到 GitHub Issues / Linear / 数据库，用 API 更新避免文件冲突。但中型项目通常 markdown 足够。

### 3.2 共享代码的修改协调

**核心原则：shared/ 和 infra/ 在 Phase 1 完成基础版本后，业务模块开发阶段（Phase 2）尽量不修改。**

但现实中总会有遗漏需要补充 shared 代码。处理流程：

```
场景: Module-B 的 agent 发现需要一个 shared/utils/date-format.ts

1. Agent 停下来，报告需求（不自行创建文件）
2. 技术负责人评估：
   a. 这个工具函数确实需要放 shared → 在主工作树创建，各 worktree rebase
   b. 这个工具函数只有 module-b 用 → 放在 module-b 内部
   c. 这个工具函数 module-a 也需要但已经在 module-a 内部写了 →
      标记为"合并时提取到 shared"，当前各自实现
3. 只有技术负责人有权修改 shared/，agent 遵守只读约定
```

**CLAUDE.md 中需要新增的约定：**

```markdown
## 共享代码修改规则
- 不要直接修改 shared/ 或 infra/ 目录下的文件
- 如果需要新增共享工具函数，在状态报告中说明需求，等待技术负责人处理
- 如果需要使用 shared/ 中不存在的功能，先在本模块内部实现，标注 TODO: 提取到 shared
```

### 3.3 接口变更的通知机制

**场景：** Module-A 在实现过程中发现接口需要调整（比如返回值需要多一个字段），Module-B 依赖这个接口。

**流程：**

```
1. Module-A 的 agent 停下来，在状态报告中说明接口变更需求
2. 技术负责人评估影响范围（查看 api-contracts.md 的依赖关系）
3. 更新 api-contracts.md（在主工作树）
4. 通知受影响模块的 agent（通过更新 task-board.md 标记"需更新"）
5. 受影响模块的 worktree rebase 获取最新文档
6. 受影响模块的 Tester agent 更新契约测试
7. 按变更传播规则继续：文档 → 测试 → 实现
```

**关键工具：api-contracts.md 中的依赖矩阵。**

```markdown
## 接口依赖矩阵

| 接口 | 提供方 | 消费方 | 变更影响 |
|------|--------|--------|---------|
| UserService.getById | module-a | module-b, module-c | 高：两个消费方 |
| OrderService.create | module-b | module-c | 中：一个消费方 |
| formatDate | shared | module-a, module-b, module-c | 高：所有模块 |
```

这张表让技术负责人在评估变更影响时不需要在脑中维护依赖关系。

---

## 4. 上下文管理

### 4.1 核心挑战

中型项目的 architecture.md 和 api-contracts.md 可能达到 1000-3000 行。如果每个 agent 都加载全部内容，上下文窗口中大部分空间被无关信息占据，降低 agent 的执行质量。

### 4.2 分层 CLAUDE.md 策略

```
project/
├── CLAUDE.md                        # 全局 CLAUDE.md（所有 agent 加载）
├── src/
│   └── modules/
│       ├── module-a/
│       │   └── CLAUDE.md            # Module-A 专属上下文
│       ├── module-b/
│       │   └── CLAUDE.md            # Module-B 专属上下文
│       └── shared/
│           └── CLAUDE.md            # Shared 层专属上下文
├── docs/
│   ├── architecture.md              # 完整架构文档
│   ├── architecture-module-a.md     # Module-A 架构摘要（从 architecture.md 提取）
│   ├── architecture-module-b.md     # Module-B 架构摘要
│   ├── api-contracts.md             # 完整接口契约
│   ├── api-contracts-module-a.md    # Module-A 相关接口（从 api-contracts.md 提取）
│   └── api-contracts-module-b.md    # Module-B 相关接口
```

**全局 CLAUDE.md 内容（精简版，< 100 行）：**

```markdown
# Project: {项目名}

## 一句话描述
## Tech Stack
## 常用命令
## 项目结构（只列顶层目录和模块名，不展开）
## 代码规范
## Git 规则
## 共享代码修改规则
## 不要做的事
## 错误处理规则

## 模块文档索引
- Module-A: src/modules/module-a/CLAUDE.md
- Module-B: src/modules/module-b/CLAUDE.md
- Shared: src/modules/shared/CLAUDE.md
```

**模块级 CLAUDE.md 内容（每个 < 50 行）：**

```markdown
# Module-A: {模块名}

## 职责
{一句话}

## 依赖的模块
- shared: 使用 formatDate, validateId
- module-b: 调用 OrderService.getByUserId（接口定义见 api-contracts-module-b.md）

## 被依赖的模块
- module-c: 调用本模块的 UserService.getById

## 当前模块的接口文档
docs/api-contracts-module-a.md

## 当前模块的架构文档
docs/architecture-module-a.md

## 模块内目录结构
src/modules/module-a/
├── controller.ts
├── service.ts
├── repository.ts
├── types.ts
└── index.ts

## 模块特有的约定
- {约定1}
- {约定2}
```

### 4.3 文档拆分策略

**api-contracts.md 的拆分：**

保留完整版 `api-contracts.md` 作为 single source of truth。同时为每个模块生成一个子文件，内容包含：
1. 本模块提供的所有接口定义
2. 本模块消费的其他模块接口的签名（只有函数签名和返回类型，不包含完整业务规则）
3. 相关的数据模型定义

拆分可以手动做，也可以让一个工具 agent 完成。关键是：完整版有变更时，子文件必须同步更新。

**architecture.md 的拆分：**

类似策略。每个模块的摘要包含：
1. 本模块的设计细节（完整）
2. 依赖模块的公开接口（只有签名）
3. 相关的数据模型
4. 全局的技术选型和架构约定

### 4.4 跨模块 agent 的信息需求

一个 Module-B 的 Implementer agent 需要知道多少 Module-A 的信息？

**需要知道的：**
- Module-A 提供的公开接口签名和返回类型
- Module-A 的错误码定义（用于处理调用失败的情况）
- Module-A 相关的数据模型定义

**不需要知道的：**
- Module-A 的内部实现逻辑
- Module-A 的内部目录结构
- Module-A 的单元测试
- Module-A 的技术负债和 TODO

**信息量估算：**
- 需要知道的部分通常 < 100 行（接口签名 + 错误码 + 数据模型）
- 这些内容写在 api-contracts-module-b.md 的"消费的外部接口"一节中

---

## 5. 任务调度

### 5.1 依赖关系与并行调度

**Task 依赖图示例：**

```
Phase 1 (串行):
  Impl-001: shared/core     ←  无依赖，最先执行

Phase 2 (并行):
  Impl-002: module-a         ←  依赖 Impl-001
  Impl-003: module-b         ←  依赖 Impl-001
  Impl-004: module-c/part1   ←  依赖 Impl-001
                                  ↑ 三个可并行

Phase 3 (部分并行):
  Impl-005: module-c/part2   ←  依赖 Impl-002 + Impl-004
  Impl-006: module-d         ←  依赖 Impl-003
                                  ↑ 两个可并行（互不依赖）

Phase 4 (串行):
  Impl-007: integration      ←  依赖所有模块
```

**task-board.md 中的调度信息扩展：**

```markdown
## 并行调度计划

| Phase | 可并行任务 | 预计最长耗时 | 需要的 worktree 数 |
|-------|-----------|------------|-------------------|
| 1 | Impl-001 | 1 天 | 1 |
| 2 | Impl-002, Impl-003, Impl-004 | 3 天 | 3 |
| 3 | Impl-005, Impl-006 | 2 天 | 2 |
| 4 | Impl-007 | 1 天 | 1 |

关键路径: Impl-001 → Impl-002 → Impl-005 → Impl-007 (7天)
```

### 5.2 阻塞处理

**当一个 Task 被阻塞时：**

```
场景: Impl-005 阻塞（等待 Impl-002 的一个接口变更）

1. Impl-005 的 agent 在状态报告中声明阻塞原因
2. 技术负责人查看 task-board：
   a. 是否有其他未启动的 Task 可以先做？
      → 有：启动那个 Task（如果 worktree 数允许）
   b. 阻塞原因是否可以临时绕过？
      → 是：让 Impl-005 先用 mock 继续，标记 TODO 后续替换
   c. 阻塞原因必须等待？
      → 是：暂停 Impl-005 的 worktree，释放资源给其他 Task
3. 更新 task-board.md 的状态和阻塞原因
```

**可被前置的 Task 类型（不需要等待阻塞解除的工作）：**
- 其他无依赖模块的实现
- 已完成模块的 Review
- 文档更新和补充
- 测试补充（为后续模块预写契约测试）

### 5.3 技术负责人的调度工作量

**小型项目：** 技术负责人的调度工作几乎为零——任务串行执行，一个完成启动下一个。

**中型项目：** 技术负责人需要频繁做以下决策：

| 调度活动 | 频率 | 耗时 |
|---------|------|------|
| 查看 agent 状态报告 | 每个 Task 完成时 | 5-10 分钟 |
| 更新 task-board.md | 每个 Task 完成时 | 5 分钟 |
| 创建/销毁 worktree | 每个 Phase 切换时 | 10 分钟 |
| 合并分支 + 解冲突 | 每个模块完成时 | 15-30 分钟 |
| 处理阻塞 / 调整计划 | 不定期 | 10-20 分钟 |
| 协调 shared 层变更 | 不定期 | 10-15 分钟 |

**工作量评估：** 如果有 3-4 个 agent 并行，技术负责人大约 30-50% 的时间用于调度协调。这是可控的，但如果超过 5 个并行 agent，调度开销会急剧上升。

### 5.4 是否需要自动化调度

**中型项目：不需要全自动调度，但可以半自动化。**

值得自动化的部分：
1. **Worktree 创建脚本**：根据 task-board.md 中的 Phase 定义，一键创建所有需要的 worktree 和分支
2. **状态汇总脚本**：扫描 `docs/status-reports/` 目录，生成进度报告
3. **合并前检查脚本**：合并分支前自动运行全量测试，检测冲突
4. **依赖图可视化**：根据 task-board.md 生成任务依赖图，高亮关键路径

不值得自动化的部分：
1. 阻塞决策（需要人类判断：绕过还是等待？）
2. 接口变更评估（需要理解业务影响）
3. 代码冲突解决（自动合并的结果不可信）

**何时升级到全自动调度（大型项目的信号）：**
- 并行 agent > 5 个
- 技术负责人 > 70% 时间用于调度
- 模块间的接口变更频繁发生（每周 > 3 次）
- 开始需要"调度 agent"来 review task-board 并推荐下一步行动

---

## 6. 从小型到中型的变化总结

| 维度 | 小型项目 | 中型项目 | 变化原因 |
|------|---------|---------|---------|
| 并行度 | 基本串行 | 2-5 agent 并行 | 项目周期压缩需求 |
| 文件隔离 | 无需（串行不冲突） | Git Worktree | 并行带来文件冲突 |
| 分支策略 | Task 粒度 feature branch | 模块粒度 feature branch + develop | 分支数量多需要集成分支 |
| 文档结构 | 单文件 | 完整版 + 模块子文件 | 上下文窗口限制 |
| CLAUDE.md | 单层 | 全局 + 模块级 | 不同模块需要不同上下文 |
| task-board | 技术负责人独占 | 技术负责人独占 + agent 状态报告 | 并行更新需求 |
| 共享代码修改 | 随需修改 | 技术负责人审批制 | 多 agent 同时修改的冲突风险 |
| 接口变更通知 | 直接更新文档 | 影响评估 + 依赖矩阵 + 传播流程 | 变更影响范围扩大 |
| 集成测试 | 可选 | 必须（逐模块集成） | 模块间交互复杂度上升 |
| 技术负责人角色 | 轻量协调 | 重度调度（30-50% 时间） | 并行协调开销 |
| 调度方式 | 手动，几乎不需要 | 半手动 + 脚本辅助 | 任务依赖复杂化 |

---

## 7. 尚需进一步设计的问题

以上分析建立了中型项目并行开发的概念框架。以下问题需要在编写具体 workflow.md 时详细设计：

1. **Worktree 中的 CLAUDE.md 同步**：主工作树更新了 CLAUDE.md 后，各 worktree 如何获取？ rebase 还是 cherry-pick？
2. **文档拆分的自动化**：从完整版 api-contracts.md 生成模块子文件，是手动维护还是用脚本/agent 自动生成？
3. **Review 的并行化**：多个模块同时完成时，Reviewer agent 是否也需要并行？Review 的上下文需要包含其他模块的变更吗？
4. **回退策略**：某个模块在集成时发现严重问题需要大改，如何不影响其他模块的进度？
5. **技术负责人的操作手册**：需要一份详细的"每日操作 checklist"，包括查看状态、创建 worktree、合并分支、处理冲突的标准流程
6. **PM Agent 的引入条件**：在什么条件下引入一个调度 agent 来辅助技术负责人？prompt 如何设计？
7. **模块级 agent-prompts**：Implementer agent 的 prompt 需要调整，指明只读取模块级文档而非全局文档
8. **CI 策略的升级**：develop 分支需要什么级别的 CI 检查？与小型项目的 CI 策略有何不同？
