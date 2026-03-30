# 中型项目开发流程规范

## 适用范围

- 4-8 个**业务**模块（技术模块如 shared/infra 不计入）
- 2-4 人开发
- 单仓库或 monorepo
- 需要 2-4 个 agent 并行

### 典型适用项目

| 项目类型 | 业务模块举例 | 规模参考 |
|---------|------------|---------|
| 多资源 REST API | 用户 + 订单 + 支付 + 库存 + 通知 | 20-50 个端点 |
| 全栈应用 | 前端 SPA + 后端 API + 管理后台 | 10-30 个页面 + 20-40 个端点 |
| 多租户 SaaS 后端 | 租户 + 用户 + 计费 + 配额 + 审计 | 30-60 个端点 |
| 数据处理管道 | 采集 + 清洗 + 转换 + 存储 + API | 5-8 个数据源 |
| 开发者工具链 | CLI + SDK + 文档生成器 + 插件系统 | 20-40 个公开函数 |

### 边界案例判断

- **从小型升级**：模块数 > 3，或模块间有多对多关系 / 复杂状态流转（审批流、状态机），或需要多人并行开发
- **降级到小型**：虽然模块数 4-5，但模块间几乎独立（纯扇出结构），且只有 1 人开发 → 可用小项目流程
- **升级到大型的信号**：模块数 > 8、需要 > 5 个 agent 并行、技术负责人 > 70% 时间用于协调、模块间接口变更频繁（每周 > 3 次）

## 不适用场景

- 探索性原型 → 先做 spike 验证方向
- 3 个以内业务模块 → 使用 small-project 流程
- 超过 8 个业务模块或多仓库 → 需要大型项目流程
- 纯 UI 还原 → 不需要此流程
- 修 bug / 小改动 → 直接改

## 角色定义

| 角色 | 职责 | 与小项目的变化 |
|------|------|--------------|
| 产品经理 | 定义需求，**分批验收** | 从最终一次性验收 → 按模块组分批验收 |
| 技术负责人 | 技术选型，系统级 + 跨模块 review，**并行调度协调**，共享层变更审批 | 新增并行调度（约 30-50% 时间用于协调） |
| System Architect agent | 系统级架构设计（模块划分、依赖关系、数据流） | 从全量设计 → 只负责系统级 |
| Module Designer agent | 模块详细设计（内部分层、数据模型） | **新增角色** |
| API Designer agent | 基于系统架构和模块设计，定义所有模块间接口契约 | **新增角色**（小项目由 Architect 一并完成） |
| Tester agent | 契约测试 + **集成测试规划** + E2E 测试 | 新增集成测试职责 |
| Implementer agent | 按模块实现功能，**只读 shared/**，通过 Issue comment 沟通 | 新增并行约束和共享层只读规则 |
| Reviewer agent | 逐 Task review + **模块完成后模块级 review** | 新增模块级 review |

> 产品经理和技术负责人通常是不同的人。如果模块数 ≤ 5 且只有 2 人开发，可以兼任。

## 文档清单

| 文档 | 谁写 | 谁 Review | 是否必须 |
|------|------|-----------|---------|
| PRD (prd.md) | 产品经理 | 产品经理 | 必须 |
| CLAUDE.md（全局） | 技术负责人 + Architect agent | 技术负责人 | 必须 |
| CLAUDE.md（模块级） | Architect agent | 技术负责人 | 必须 |
| README.md | 技术负责人 | 无需 review | 推荐 |
| 系统架构 (architecture.md) | System Architect agent | 技术负责人 | 必须 |
| 模块设计 (module-design/{module}.md) | Module Designer agent | 技术负责人 | 必须 |
| 接口契约 (api-contracts.md) | API Designer agent | 技术负责人 | 必须 |
| 接口契约子文件 (api-contracts-{module}.md) | Architect agent / 脚本 | 技术负责人 | 必须 |
| 架构决策记录 (decision-log.md) | 技术负责人 + agents | 无需 review | 推荐 |
| GitHub Issues | Architect agent + 技术负责人 | 技术负责人 | 必须 |
| 契约测试 + 集成测试 + E2E 测试 | Tester agent | 技术负责人 | 必须 |
| 单元测试 | Implementer agent | Reviewer agent | 按需 |
| 业务代码 | Implementer agent | Reviewer agent + 技术负责人（跨模块时） | 必须 |

> **CLAUDE.md vs README.md**：CLAUDE.md 面向 AI Agent，包含约定和禁止事项；README.md 面向人类开发者，包含快速上手指南。两者定位不同，不可互相替代。

## 开发流程

```
Step 1: 初始化
├── 技术负责人: git init + GitHub 仓库创建 + GitHub Project 创建
├── 产品经理: 编写 PRD（含验收标准，按模块组织）
├── 会话1 [Architect agent]: 读 PRD → 产出 CLAUDE.md 基础部分建议
│   └── 一句话描述、Tech Stack、项目文档、代码规范、Git 规则、不要做的事、错误处理规则
└── 技术负责人: review 并确认 CLAUDE.md 基础部分

Step 2a: 系统架构设计
├── 会话2 [System Architect agent]: 读 PRD → 产出 architecture.md（系统级）
│   ├── 模块划分与职责定义
│   ├── 模块依赖关系图（有向无环）
│   ├── 跨模块数据流
│   ├── 部署架构概要
│   └── 补充 CLAUDE.md: 项目结构概览、架构约定、不要做的事（架构相关）
└── 技术负责人: review
    ├── 通过 → 进入 Step 2b
    └── 不通过 → 新会话修订

Step 2b: 模块详细设计（可并行）
├── 会话3 [Module Designer agent]: 读 architecture.md + PRD → module-design/module-a.md
├── 会话4 [Module Designer agent]: 读 architecture.md + PRD → module-design/module-b.md
├── ...（各模块设计可并行执行，无依赖）
└── 技术负责人: review 所有模块设计
    ├── 通过 → 进入 Step 2c
    └── 不通过 → 对应模块新会话修订

Step 2c: 接口契约定义
├── 会话N [API Designer agent]: 读 architecture.md + 所有 module-design → api-contracts.md
│   ├── 所有模块间接口定义（含 consumers 字段）
│   ├── 接口依赖矩阵
│   └── 需求追溯表（PRD 功能点 → 接口映射）
└── 技术负责人: review
    ├── 通过 → 进入 Step 3
    └── 不通过 → 新会话修订

Step 3: 环境初始化 + 任务拆分
├── 会话N+1 [Architect agent]: 读架构 + 契约文档
│   ├── 初始化脚手架（含模块目录结构、导出桩文件）
│   ├── 创建模块级 CLAUDE.md
│   ├── 生成 api-contracts-{module}.md 子文件
│   ├── 创建 GitHub Issues（含依赖关系、Phase 标注）
│   ├── 规划并行调度（Phase 划分 + 关键路径标注）
│   ├── 规划集成测试用例（识别 L2 关键路径）
│   └── 回填 CLAUDE.md: 常用命令、测试环境
│
│   任务拆分原则：
│   ├── 共享层（shared/infra）独立为最高优先级 Task
│   ├── 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
│   ├── 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
│   ├── Task 间依赖关系标注为 DAG（在 Issue body 中声明 Depends on）
│   ├── 每个 Task 标注所属 Phase 和需通过的测试
│   └── 强类型语言：为每个模块创建导出桩文件（只声明签名，函数体抛 Not implemented）
│
│   模块内 Task 拆分策略：
│   ├── 按层拆分（CRUD 密集型）: repository → service → controller
│   ├── 按功能拆分（功能丰富型）: 注册登录 → 个人资料 → 权限管理
│   └── 拆不到粒度 → 说明模块划分需要回退到 Step 2a 调整
│
└── 技术负责人: review 脚手架、Issues、调度计划
    ├── 通过 → 进入 Step 4
    └── 不通过 → 新会话修订

Step 4: 契约测试先行（可多模块并行）
├── 技术负责人: 为并行模块创建 Git Worktree（见"并行开发与 Git 策略"一节）
├── 会话 [Tester agent]: 在 worktree 中写模块 A 的契约测试
├── 会话 [Tester agent]: 在 worktree 中写模块 B 的契约测试
├── ...（模块间无依赖的测试可并行）
├── 技术负责人: review 测试代码
│   ├── 通过 → 合并各 worktree 到 develop → 进入 Step 5
│   └── 不通过 → Tester agent 新会话修改
└── 技术负责人: 更新 GitHub Issues 状态

Step 5: 实现 + Review（多模块并行，分 Phase 推进）
│
├── Phase 1: 共享层串行先行
│   ├── 会话 [Implementer agent]: 实现 shared/infra
│   ├── 会话 [Reviewer agent]: review
│   └── 合并到 develop → 所有 worktree rebase
│
├── Phase 2: 业务模块并行实现
│   ├── 技术负责人: 为每个并行模块创建 worktree
│   └── 循环 [按 Task 依赖顺序，每个模块内串行，模块间并行]:
│       ├── 会话 [Implementer agent]: 在 worktree 中实现 Task
│       │   ├── 契约测试通过
│       │   ├── L1 模块内集成测试通过
│       │   └── 完成后 gh issue comment 报告
│       ├── 会话 [Reviewer agent]: 对照文档 + 测试 review
│       │   ├── LGTM → 技术负责人更新 Issue 状态，进入下一个 Task
│       │   ├── MUST FIX / SHOULD FIX → Implementer 新会话修复 → 重新 Review
│       │   └── 涉及接口变更 → 停止，按变更传播规则处理
│       └── 技术负责人: 管理调度、处理阻塞、协调 shared 变更请求
│
├── Phase 3: 逐模块集成
│   ├── 按依赖顺序逐模块合并到 develop（被依赖的先合并）
│   ├── 每合并一个模块 → 跑该模块相关的集成测试
│   ├── 合并后 → 相关模块的 Implementer 编写 L2 关键路径集成测试
│   └── 发现问题 → 在对应 worktree 中修复 → 重新合并
│
└── Phase 4: 全量验证
    ├── develop 上运行全量测试（契约 + 单元 + L1 + L2 集成）
    └── 全部通过 → 合并到 main

Step 6: E2E 测试
├── 关键路径模块就绪后即可开始（不必等所有模块完成）
├── 会话 [Tester agent]: 根据 PRD 验收标准编写 E2E 测试，覆盖核心用户流程
├── 技术负责人: 确认 E2E 测试通过
├── 技术负责人: 编写 README.md（推荐，基于 CLAUDE.md 和 architecture.md 整理）
└── 如不需要自动化 E2E → 跳过，由 Step 7 产品经理手动验收覆盖

Step 7: 验收（分批）
├── 产品经理: 按模块组分批验收
│   ├── 核心模块优先验收
│   └── 每批验收后可调整后续模块的优先级和需求
└── 最终全量验收
```

## 术语说明

> **契约测试（Specification Test）**：与小项目流程相同，指基于 api-contracts.md 验证接口输入输出的规格测试。这**不是** Pact 风格的消费者驱动契约测试（CDCT）。
>
> **L1 集成测试（模块内）**：验证模块内部各层（如 controller → service → repository）的真实串联，使用真实依赖（如内存数据库），不 Mock 模块内部组件。
>
> **L2 集成测试（跨模块 / 关键路径）**：验证关键业务路径上多个模块的真实协作（如 下单 → 扣库存 → 创建支付单），在 develop 分支上运行，不 Mock 其他模块。
>
> **Phase**：Step 5 内部的执行阶段。Phase 1 共享层串行 → Phase 2 业务模块并行 → Phase 3 逐模块集成 → Phase 4 全量验证。
>
> **consumers 字段**：api-contracts.md 中每个接口标注的消费方列表，用于变更影响评估。

## 任务管理：GitHub Projects

### 替代 task-board.md

中型项目使用 GitHub Projects + GitHub Issues 替代小项目的 task-board.md：

| 维度 | 小项目 (task-board.md) | 中型项目 (GitHub Projects) |
|------|----------------------|--------------------------|
| 存储 | Markdown 文件，技术负责人独占编辑 | GitHub Issues，多人可并行操作 |
| 依赖关系 | 文本描述（`依赖: Impl-001`） | Issue body 中 `Depends on #N` + Sub-issues |
| 程序化访问 | 无 API | `gh` CLI + GraphQL API |
| 可视化 | 无 | Board / Table / Roadmap 视图 |
| 状态更新 | 编辑文件 + git commit | 标签 / Project 字段 / Comment |
| 并发瓶颈 | 有（单文件锁） | 无 |

### GitHub Project 配置

**Project 自定义字段**：

| 字段 | 类型 | 选项 |
|------|------|------|
| Status | 单选 | Todo, In Progress, Review, Done, Blocked |
| Phase | 单选 | Phase 1 (Shared), Phase 2 (Parallel), Phase 3 (Integration), Phase 4 (E2E) |
| Module | 单选 | shared, {module-a}, {module-b}, ... |
| Priority | 单选 | P0, P1, P2 |

**Issue 标签**：

| 标签 | 用途 |
|------|------|
| `type:contract-test` | 契约测试任务 |
| `type:impl` | 实现任务 |
| `type:integration-test` | 集成测试任务 |
| `type:e2e` | E2E 测试任务 |
| `module:{name}` | 所属模块 |

**Issue body 模板**：

```markdown
## 任务描述
{一句话描述}

## 所属模块
{module name}

## 依赖
- Depends on #{issue-number}

## 需通过测试
- [ ] 契约测试: {test file/suite}
- [ ] L1 集成测试: {if applicable}

## 验收标准
- [ ] {criterion 1}
- [ ] {criterion 2}
```

### Agent 与 GitHub Issues 的交互

**技术负责人操作**：

```bash
# 创建 GitHub Project
gh project create --title "{项目名}" --owner "@me"

# 批量创建 Issues
gh issue create --title "[shared] 实现公共类型和工具函数" \
  --body "..." --label "type:impl,module:shared" \
  --milestone "Phase 1" --project "{项目名}"

gh issue create --title "[user] 实现用户注册接口" \
  --body "Depends on #1\n..." --label "type:impl,module:user" \
  --milestone "Phase 2" --project "{项目名}"

# 查看项目进度
gh issue list --state open --label "module:user"
gh issue list --state all --milestone "Phase 2"
```

**Agent 操作**：

```bash
# 报告任务完成
gh issue comment {NUMBER} --body "实现完成。所有契约测试通过，L1 集成测试通过。"

# 报告阻塞
gh issue comment {NUMBER} --body "阻塞：需要 #{dep-issue} 的接口完成后才能继续。"

# 报告接口变更需求
gh issue comment {NUMBER} --body "发现接口需要调整：{描述变更}。请技术负责人评估影响范围。"
```

**状态管理原则**：Agent 通过 Issue comment 报告进展，**技术负责人负责更新 Project Board 状态**，以保持对调度的控制权。

### 依赖关系管理

**依赖声明**：Issue body 中用 `Depends on #N` 标注前置依赖。

**Sub-issues 层级**：将模块的多个 Task 组织为父子关系：

```
#10 [user] 用户模块实现                ← 父 Issue（模块粒度）
  ├── #11 [user] 实现 repository 层
  ├── #12 [user] 实现 service 层      ← Depends on #11
  └── #13 [user] 实现 controller 层   ← Depends on #12
```

**关键路径**：在 Project 描述或固定 Issue 中记录关键路径和并行调度计划：

```markdown
## 并行调度计划

| Phase | 可并行任务 | 需要的 worktree 数 |
|-------|-----------|-------------------|
| 1 | #1 shared | 1 |
| 2 | #10 user, #20 product, #30 order | 3 |
| 3 | #40 payment (依赖 #30), #50 notification | 2 |

关键路径: #1 → #30 → #40
```

## 并行开发与 Git 策略

### Git Worktree

每个并行 agent 在独立的 Git Worktree 中工作，消除文件系统和 Git 状态冲突：

```
project/                          # 主工作树（技术负责人使用）
├── .git/                         # 唯一的 .git 目录
├── CLAUDE.md
├── docs/
└── src/

../project-wt-module-a/          # Worktree A: Implementer Agent A
├── (指向 project/.git)
└── (feature/module-a 分支的完整文件)

../project-wt-module-b/          # Worktree B: Implementer Agent B
├── (指向 project/.git)
└── (feature/module-b 分支的完整文件)
```

**技术负责人操作流程**：

```bash
# 创建 worktree（Step 4 或 Step 5 Phase 2 开始前）
cd project
git branch feature/module-a develop
git branch feature/module-b develop
git worktree add ../project-wt-module-a feature/module-a
git worktree add ../project-wt-module-b feature/module-b

# 共享层更新后，各 worktree rebase
cd ../project-wt-module-a && git rebase develop
cd ../project-wt-module-b && git rebase develop

# 模块完成后逐个合并（Phase 3）
cd project && git checkout develop
git merge --no-ff feature/module-a
# 跑集成测试 → 通过后继续
git merge --no-ff feature/module-b

# 清理
git worktree remove ../project-wt-module-a
git branch -d feature/module-a
```

### 分支策略

```
main                              # 始终可部署
 └── develop                      # 集成分支
      ├── feature/shared          # 共享层（Phase 1，最先合并）
      ├── feature/module-a        # 业务模块 A
      ├── feature/module-b        # 业务模块 B
      └── feature/module-c        # 业务模块 C
```

**分支规则**：

- 每个**模块**一个 feature 分支（不是每个 Task 一个——模块内多个 Task 在同一分支串行完成）
- 共享层有自己的 feature 分支，必须最先合并
- 合并策略：`--no-ff`（保留合并记录，方便追溯）
- 分支命名：`feature/{module-name}`

**与小项目的差异**：

| 维度 | 小型项目 | 中型项目 |
|------|---------|---------|
| 分支使用 | 直接在 main 开发 | feature → develop → main |
| 分支粒度 | 无分支 | 每个模块一个 feature 分支 |
| 集成分支 | 无 | develop |
| 合并策略 | 直接 commit | `--no-ff` 合并 |
| Worktree | 不需要 | 必须 |

### 模块集成流程

```
Phase 1: shared/infra → 合并到 develop → 所有 worktree rebase

Phase 2: 业务模块并行开发（各自 worktree，互不干扰）

Phase 3: 逐模块合并（按依赖顺序，被依赖的先合并）
  module-a → merge --no-ff develop → 跑集成测试 ✓
  module-b → rebase develop → merge --no-ff → 跑集成测试 ✓
  module-c → rebase develop → merge --no-ff → 跑集成测试 ✓

Phase 4: develop 全量测试通过 → merge --no-ff main
```

**关键原则：逐模块合并，不 big-bang。** 每合并一个模块跑一次集成测试，问题定位范围小。

### 提交规范

- commit 粒度：每个有意义的改动一个 commit
- commit message 格式：`<type>(<module>): <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 示例：`feat(order): 实现订单创建接口`、`fix(shared): 修正日期格式化时区问题`

### 共享代码修改规则

Phase 2 期间，shared/ 和 infra/ 遵守以下规则：

1. **Implementer agent 不直接修改 shared/ 或 infra/**
2. 如需新增共享工具函数 → 在 Issue comment 中说明需求，等技术负责人处理
3. 如需使用 shared/ 中不存在的功能 → 先在本模块内部实现，标注 `TODO: 提取到 shared`
4. 技术负责人评估后决定：
   - 确实需要放 shared → 在主工作树创建，各 worktree rebase
   - 只有一个模块用 → 放在模块内部
   - 多模块都需要但各自已实现 → 标记"合并时提取到 shared"

### 文件冲突预防

**架构层面**：模块目录物理隔离（`src/modules/a/` 和 `src/modules/b/` 无交叉文件）。

**高风险文件**（技术负责人在合并时统一处理，不让 agent 自行修改）：

- `package.json` / `go.mod` — 多模块同时新增依赖
- 数据库 migration 文件 — 多模块同时新增 migration
- 路由注册 / 入口文件 — 多模块同时注册路由
- 全局配置文件

### 接口变更通知

当模块实现中发现接口需要调整：

1. Agent 在 Issue comment 中说明变更需求，停止当前实现
2. 技术负责人查看 api-contracts.md 的**接口依赖矩阵**，评估影响范围
3. 更新 api-contracts.md + 对应的 api-contracts-{module}.md（在主工作树）
4. 为受影响模块的 Issue 添加 comment 通知变更
5. 受影响 worktree rebase 获取最新文档
6. 按变更传播规则执行：文档 → 测试 → 实现

## 文档分层策略

### CLAUDE.md 分层

**全局 CLAUDE.md（< 100 行）** — 所有 agent 自动加载：

```markdown
# Project: {项目名}
## 一句话描述
## Tech Stack
## 常用命令
## 项目结构（只列顶层目录和模块名，不展开）
## 代码规范
## Git 规则
## 共享代码修改规则（不要直接改 shared/，见规则说明）
## 不要做的事
## 错误处理规则
## 模块文档索引
- Module-A: src/modules/module-a/CLAUDE.md
- Module-B: src/modules/module-b/CLAUDE.md
- Shared: src/modules/shared/CLAUDE.md
```

**模块级 CLAUDE.md（< 50 行）** — 仅该模块的 agent 加载：

```markdown
# Module: {模块名}
## 职责（一句话）
## 依赖的模块（列出公开接口引用）
## 被依赖的模块（谁在调用本模块）
## 当前模块的接口文档: docs/api-contracts-{module}.md
## 当前模块的设计文档: docs/module-design/{module}.md
## 模块内目录结构
## 模块特有的约定
```

### 文档拆分

**api-contracts.md 拆分**：

保留完整版 `api-contracts.md` 作为 single source of truth。同时为每个模块生成子文件 `api-contracts-{module}.md`，内容包含：

1. 本模块提供的所有接口定义（完整，含业务规则和错误码）
2. 本模块消费的其他模块接口（只含函数签名和返回类型，不含完整业务规则）
3. 相关的数据模型定义

**完整版变更时，子文件必须同步更新。** 技术负责人或脚本负责同步。

**architecture.md 收缩**：

收缩为系统级内容（模块划分、依赖关系图、部署架构、跨模块数据流）。每个模块的详细设计（内部分层、关键类、模块内数据模型）下沉到 `module-design/{module}.md`。

### 跨模块 agent 的信息边界

Module-B 的 agent 关于 Module-A **需要知道的**：

- 公开接口签名和返回类型
- 错误码定义
- 相关数据模型

**不需要知道的**：

- 内部实现逻辑、目录结构、单元测试、技术债

这些信息通过 `api-contracts-{module-b}.md` 中的"消费的外部接口"一节提供，通常 < 100 行。

## 文档变更传播规则

核心原则与小项目相同：**先更新文档 → 再更新测试 → 最后更新实现。** 按模块依赖顺序处理，被依赖的模块优先。

### api-contracts.md 变更

1. 查看**接口依赖矩阵**，识别所有受影响的消费方模块
2. 更新 api-contracts.md 完整版
3. 同步更新相关 api-contracts-{module}.md 子文件
4. 在受影响模块的 GitHub Issue 中 comment 变更通知
5. Tester agent 新会话更新契约测试
6. 已完成的实现如涉及变更接口，标记 Issue 为"需更新"

### architecture.md 变更

1. 评估是否影响模块划分和依赖关系
2. 更新受影响的 module-design/{module}.md
3. 更新 CLAUDE.md 中的项目结构（如有变化）
4. 记录到 decision-log.md

### 变更记录

- 重大架构变更 → decision-log.md
- 在相关 GitHub Issue 中 comment 变更原因和影响范围
- commit message 标注：`docs(<module>): {变更内容}，影响范围: #{issue-list}`

## 测试策略

### 测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| 契约测试 | Tester agent | Step 4（实现前） | api-contracts.md | 必须 |
| 单元测试 | Implementer agent | Step 5（实现中） | 复杂内部逻辑 | 按需 |
| L1 模块内集成 | Implementer agent | Step 5（实现中） | controller → service → repository 串联 | **必须** |
| L2 关键路径集成 | Implementer agent（调用方） | Step 5 Phase 3（模块合并后） | 跨模块真实调用 | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |
| 回归测试 | CI 自动 | 每次合并 | 受影响模块的测试 | 按影响范围 |

**与小项目的核心差异**：L1 集成测试从"按需"升级为**必须**；新增 L2 关键路径集成测试。

### Mock 策略

| 测试层级 | 模块间依赖 | 外部依赖（数据库、第三方 API） |
|---------|-----------|---------------------------|
| 契约测试 | Mock / Stub | Mock（内存数据库可替代） |
| 单元测试 | Mock / Stub | Mock |
| L1 模块内集成 | Mock 其他模块 | 真实连接或测试容器 |
| L2 跨模块集成 | **真实调用** | 真实连接或测试容器 |
| E2E 测试 | **真实调用** | 真实连接 |

### L2 集成测试的触发时机

当模块 B 依赖模块 A，且模块 A 已合并到 develop：

1. 模块 B 的 worktree rebase develop（获取模块 A 的真实代码）
2. 模块 B 的 Implementer agent 编写跨模块集成测试
3. 在 develop 分支上运行，使用真实的模块 A（不 Mock）

### 测试目录结构

```
tests/
├── contracts/              # 契约测试（按模块组织）
│   ├── module-a/
│   └── module-b/
├── unit/                   # 单元测试（按模块组织）
├── integration/            # 集成测试
│   ├── module-a/           # L1: 模块内集成
│   ├── module-b/
│   └── paths/              # L2: 关键路径集成
│       ├── order-payment-flow.test.ts
│       └── user-order-flow.test.ts
├── e2e/                    # E2E 测试（按用户流程）
└── fixtures/               # 共享测试数据（工厂函数，非硬编码）
```

### 契约测试 Step 4 预期状态

与小项目相同：测试代码能编译/加载，但执行时全部失败（因为实现不存在）。强类型语言通过 Step 3 的导出桩文件解决编译问题。

## Review 机制

### 分层 Review

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| Task Review | 每个 Task 完成 | Reviewer Agent | 功能正确性、代码规范、测试覆盖 |
| 模块 Review | 模块所有 Task 完成 | Reviewer Agent（模块级 prompt） | 模块内一致性、命名/风格统一、接口覆盖完整性 |
| 跨模块 Review | 涉及跨模块变更时 | 技术负责人 | 接口一致性、依赖方向、shared 修改合理性 |
| 架构 Review | 架构变更提议时 | 技术负责人 | 决策合理性、影响范围、是否记录到 decision-log |

**分层原则**：技术负责人只做系统级和跨模块 review，模块内 review 委托 Reviewer Agent，降低技术负责人瓶颈。

### Review 输出标准

与小项目相同：

- **LGTM** — 通过，无需修改
- **MUST FIX** — 必须修复后重新 review
- **SHOULD FIX** — 建议修改，修改后重新 review
- **OPTIONAL** — 可选优化，不阻塞进度

## 会话管理

### 基本原则

与小项目相同：**每个角色、每个任务使用独立的新会话。**

### 中型项目特有规则

- **每个模块的 agent 在对应的 Worktree 中工作**，不跨 Worktree 操作
- **模块 agent 只加载必要文档**：全局 CLAUDE.md + 模块级 CLAUDE.md + api-contracts-{module}.md + module-design/{module}.md
- **不同模块的 agent 会话完全独立**，互不知道对方的进度（通过 GitHub Issues 间接协调）
- **技术负责人是唯一的信息枢纽**

### 并行会话管理

| Step | 可并行的会话 | 隔离方式 |
|------|------------|---------|
| Step 2b | 多个 Module Designer 会话 | 各自产出独立文件，无冲突 |
| Step 4 | 多个 Tester 会话 | 各自在独立 Worktree 中 |
| Step 5 Phase 2 | 多个 Implementer 会话 | 各自在独立 Worktree 中 |

并行时严格遵守 Worktree 隔离，不修改其他模块的文件。

### 什么时候必须开新会话

1. 切换角色时
2. 切换 Task 时（即使同一角色）
3. Review 不通过需要修复时
4. Agent 表现异常时
5. **切换 Worktree 时**（中型项目特有）

## 目录结构

```
project/
├── CLAUDE.md                        # 全局 CLAUDE.md（< 100 行）
├── README.md
├── docs/
│   ├── prd.md                       # PRD（> 500 行时可拆为 prd/ 目录）
│   ├── architecture.md              # 系统级架构
│   ├── api-contracts.md             # 完整接口契约（single source of truth）
│   ├── api-contracts-{module-a}.md  # 模块 A 接口子文件
│   ├── api-contracts-{module-b}.md  # 模块 B 接口子文件
│   ├── module-design/               # 模块详细设计
│   │   ├── module-a.md
│   │   └── module-b.md
│   └── decision-log.md              # 架构决策记录
├── src/
│   └── modules/
│       ├── module-a/
│       │   ├── CLAUDE.md            # 模块级 CLAUDE.md（< 50 行）
│       │   ├── controller.ts
│       │   ├── service.ts
│       │   ├── repository.ts
│       │   ├── types.ts
│       │   └── index.ts             # 导出桩（Step 3 创建）
│       ├── module-b/
│       │   ├── CLAUDE.md
│       │   └── ...
│       └── shared/
│           ├── CLAUDE.md
│           ├── types/
│           └── utils/
└── tests/
    ├── contracts/                   # 契约测试（按模块）
    ├── unit/                        # 单元测试（按模块）
    ├── integration/                 # 集成测试
    │   ├── {module-a}/              # L1 模块内
    │   └── paths/                   # L2 关键路径
    ├── e2e/                         # E2E 测试
    └── fixtures/                    # 共享测试数据
```

## 迭代管理

### 何时需要多迭代

- 4-5 个模块：通常 1 个迭代
- 6-8 个模块：建议 2-3 个迭代
- 判断标准：如果所有模块一起推进时关键路径过长，或模块间有明确的优先级差异

### 迭代划分

使用 **GitHub Milestones** 管理迭代：

```
Milestone 1: 核心模块
  包含: shared + user + product
  → Step 2a-7 完整走一遍
  → 产品经理验收核心流程

Milestone 2: 交易模块
  包含: order + payment + inventory
  → Step 2（增量：只设计新模块，review 对已有模块的影响）→ Step 3-7
  → 产品经理验收交易流程

Milestone 3: 辅助模块
  包含: notification + coupon + analytics
  → 同上（增量模式）
  → 最终全量验收
```

### 迭代间的关系

- 后续迭代的 Step 2 只设计本迭代新增模块，但必须 review 对已有模块的影响
- 已有模块的接口如需变更，按变更传播规则处理
- 每个迭代结束时 develop 合并到 main，保持 main 可部署

## 速查：每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准 |
|------|--------|------|------|---------|
| 1 | 人 + Architect | — | PRD, CLAUDE.md（基础）, GitHub Project | PRD 按模块组织含验收标准；CLAUDE.md 基础部分确认；Project 已创建 |
| 2a | System Architect | PRD, CLAUDE.md | architecture.md | 模块划分清晰；依赖单向无环；数据流完整 |
| 2b | Module Designer × N | architecture.md, PRD | module-design/*.md | 每模块内部设计完整；数据模型清晰 |
| 2c | API Designer | architecture + module-designs | api-contracts.md | 每个 PRD 功能映射到接口；consumers 完整；依赖矩阵完整；追溯表完整 |
| 3 | Architect | 架构 + 契约 | 脚手架, Issues, 模块 CLAUDE.md, 调度计划 | 脚手架能运行；Issues 含依赖 + Phase；模块 CLAUDE.md < 50 行；关键路径已标注 |
| 4 | Tester × N | api-contracts | 契约测试代码 | 测试能编译；执行时失败（TDD）；覆盖正常+异常流程 |
| 5 | Impl + Reviewer × N | 文档 + 测试 | 业务代码 | 契约测试 + L1 通过；逐模块合并 develop；L2 通过；全量测试通过 |
| 6 | Tester | PRD 验收标准 | E2E 测试 | 核心路径 E2E 通过 |
| 7 | 产品经理 | PRD | 验收确认 | 分批验收全部通过 |

## 增量开发（已有项目加新功能）

| 场景 | 起始步骤 | 说明 |
|------|---------|------|
| 新增业务模块 | Step 2a（评估对现有架构影响） | 可能只需更新 architecture.md 的依赖图，然后 2b → 2c → ... |
| 已有模块增加接口 | Step 2c（更新 api-contracts.md） | 同时更新依赖矩阵和子文件 |
| 跨多模块的新功能 | Step 2a（影响评估） | 查接口依赖矩阵确定影响范围 → 2c → 4 → 5 |
| 模块内重构不改接口 | Step 5 | 契约测试不需要改（接口没变） |
| 修 bug | 不走流程 | 直接改 + 补测试 + 提交 |

关键原则：**变了什么文档，就从那个文档对应的步骤开始往后走。** 改了接口 → 从 Step 4 更新测试开始；只改实现 → 从 Step 5 开始。

## 常见故障与恢复

### Agent 会话崩溃

1. 检查 Worktree 状态：`git worktree list` 确认 agent 在哪个 Worktree 中
2. 检查 git 状态：`git status` + `git log` 确认最后 commit
3. 有未提交的改动且质量可接受 → 提交后新会话继续
4. 有未提交的改动但质量不确定 → `git stash`，新会话重新开始
5. 无未提交改动 → 新会话重新开始

### 模块集成发现严重问题

1. 停止该模块的合并
2. 在对应 GitHub Issue 中 comment 问题描述
3. 其他不依赖该模块的 worktree **继续工作**（并行优势）
4. 该模块在自己的 worktree 中修复 → 重新合并
5. 如涉及架构问题 → 回退到 Step 2a，在 decision-log.md 记录

### 并行 agent 间的语义冲突

两个模块各自测试通过，合并后互相破坏：

1. 在 develop 上定位冲突原因
2. 接口理解不一致 → 更新 api-contracts.md → 按变更传播处理
3. 实现方式冲突 → decision-log.md 记录决策 → 修改其中一个模块

### 技术负责人成为瓶颈

1. 模块内 Review 委托 Reviewer Agent（只做跨模块 review）
2. 重复性操作脚本化（Worktree 创建/销毁、状态汇总）
3. 仍超负荷 → 引入"模块负责人"，每人负责 1-2 个模块的日常协调

### 共享层变更频繁

1. 检查 Phase 1 时 shared 层设计是否不充分 → 考虑回退补充
2. 高频变更的函数暂时放在模块内部，迭代结束时统一提取到 shared
3. 在 decision-log.md 记录"为什么当时没有预见到这个共享需求"

### 实现过程中发现架构有问题

1. Agent 停止实现，在 Issue comment 中报告
2. 技术负责人评估影响范围
3. 回退到 Step 2a/2b：新会话修订架构文档
4. 在 decision-log.md 记录变更原因
5. 按变更传播规则：文档 → 测试 → 实现

### Agent 产出质量不达标

1. 给出具体修改要求（引用 Issue 编号、契约章节、代码行号）
2. 反复出现同类问题 → 在对应模块的 CLAUDE.md 中增加针对性约束
3. 质量仍不达标 → 将 Task 拆得更小，或技术负责人手动完成关键部分

## CI 集成建议

### 分层流水线

```
Layer 1 (每次 push 到 feature/*, < 2min):
  lint + 当前模块的契约测试 + 单元测试

Layer 2 (PR 到 develop, < 10min):
  全量契约 + 单元 + L1 + L2 集成测试

Layer 3 (PR 到 main, < 30min):
  Layer 2 + E2E 测试
```

### 分支与 CI 的关系

| 分支 | 触发 CI | 检查级别 |
|------|--------|---------|
| feature/* | push | Layer 1 |
| develop | PR merge | Layer 2 |
| main | PR merge | Layer 3 |

### GitHub Actions 示例

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: ['feature/**']
  pull_request:
    branches: [develop, main]

jobs:
  lint-and-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --filter contracts unit

  integration:
    if: github.base_ref == 'develop' || github.base_ref == 'main'
    needs: lint-and-unit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test -- --filter integration

  e2e:
    if: github.base_ref == 'main'
    needs: integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test -- --filter e2e
```

> 以上为 Node.js 项目示例。其他技术栈替换对应的 setup 和命令即可。
