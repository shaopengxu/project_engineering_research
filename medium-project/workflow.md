# 中型项目开发流程规范

## 适用范围

- 4-8 个**业务**模块（技术模块如 shared/infra 不计入）
- 以 AI agent 为主力开发，串行推进
- 单仓库或 monorepo

### 典型适用项目

全栈应用：前端 SPA + 后端 API + 管理后台，10-30 个页面 + 20-40 个端点。

### 边界案例判断

- **下限**：模块数 > 3，或模块间有多对多关系 / 复杂状态流转（审批流、状态机）
- **可能过重**：虽然模块数 4-5，但模块间几乎独立（纯扇出结构）→ 可简化流程
- **超出适用范围**：模块数 > 8

## 不适用场景

- 探索性原型 → 先做 spike 验证方向
- 3 个以内业务模块 → 本流程过重
- 超过 8 个业务模块或多仓库 → 本流程不足以支撑
- 纯 UI 还原 → 不需要此流程
- 修 bug / 小改动 → 直接改

## 角色定义

| 角色 | 职责 |
|------|------|
| 产品经理 | 定义需求，按模块组分批验收 |
| 技术负责人 | 技术选型，系统级 + 跨模块 review，任务流转管理 |
| Architect agent | 初始化 CLAUDE.md、系统级架构设计、模块详细设计 + 接口契约、脚手架搭建、任务拆分 |
| Tester agent | 契约测试 + 集成测试规划 + E2E 测试 |
| Implementer agent | 按模块实现功能，通过 Issue comment 沟通 |
| Reviewer agent | 逐 Task review + 模块完成后模块级 review |

## 文档清单

| 文档 | 谁写 | 谁 Review | 是否必须 |
|------|------|-----------|---------|
| PRD (prd.md) | 产品经理 | 产品经理 | 必须 |
| CLAUDE.md | 技术负责人 + Architect agent | 技术负责人 | 必须 |
| README.md | 技术负责人 | 无需 review | 推荐 |
| 系统架构 (architecture.md) | Architect agent | 技术负责人 | 必须 |
| 模块设计 (module-design/{module}.md) | Architect agent | 技术负责人 | 必须 |
| 接口契约 (api-contracts.md) | Architect agent（逐模块构建）| 技术负责人 | 必须 |
| 接口契约子文件 (api-contracts-{module}.md) | Architect agent / 脚本 | 技术负责人 | 必须 |
| GitHub Issues | Architect agent + 技术负责人 | 技术负责人 | 必须 |
| 契约测试 + 集成测试 + E2E 测试 | Tester agent | 技术负责人 | 必须 |
| 单元测试 | Implementer agent | Reviewer agent | 按需 |
| 业务代码 | Implementer agent | Reviewer agent + 技术负责人（跨模块时） | 必须 |

> **CLAUDE.md vs README.md**：CLAUDE.md 面向 AI Agent，包含约定和禁止事项；README.md 面向人类开发者，包含快速上手指南。两者定位不同，不可互相替代。

## 开发流程

```
Step 1: PRD 审查 + 初始化
├── 前置条件：产品经理已完成 PRD（含验收标准，按模块组织）
├── 技术负责人: 审查 PRD 是否满足开发需求
│   ├── 验收标准是否明确可测试
│   ├── 功能点按模块组织且无遗漏
│   ├── 非功能性需求已说明（性能、安全等）
│   ├── 不通过 → 退回产品经理修改，修改后重新审查
│   └── 通过 → 继续初始化
├── 技术负责人: git init + GitHub 仓库创建 + GitHub Project 创建
├── 会话1 [Architect agent]: 读 PRD → 产出 CLAUDE.md 基础部分建议
│   └── 一句话描述、Tech Stack、项目文档、代码规范、Git 规则、共享代码修改规则、不要做的事、错误处理规则
└── 技术负责人: review 并确认 CLAUDE.md 基础部分

Step 2a: 系统架构设计
├── 会话2 [Architect agent]: 读 PRD → 产出 architecture.md（系统级）
│   ├── 模块划分与职责定义
│   ├── 模块依赖关系图（有向无环）
│   ├── 跨模块数据流
│   ├── 部署架构概要
│   └── 补充 CLAUDE.md: 项目结构概览、架构约定、不要做的事（架构相关）
└── 技术负责人: review
    ├── 通过 → 进入 Step 2b
    └── 不通过 → 新会话修订

Step 2b: 模块详细设计 + 接口契约
├── 会话3 [Architect agent]: 读 architecture.md + PRD →
│   ├── module-design/module-a.md
│   ├── api-contracts.md 中 module-a 的接口定义（含五要素：输入、输出、业务规则、错误码、consumers）
│   └── 首个模块同时建立 api-contracts.md 通用约定（认证、响应格式、分页、状态码）
├── 会话4 [Architect agent]: 读 architecture.md + PRD + 已有 api-contracts.md →
│   ├── module-design/module-b.md
│   └── api-contracts.md 中 module-b 的接口定义
├── ...（各模块按依赖顺序串行，后续模块可参考已定义的接口）
├── 最后一个模块完成后：补充 api-contracts.md 的接口依赖矩阵 + 需求追溯表
└── 技术负责人: review 所有模块设计 + api-contracts.md
    ├── 通过 → 进入 Step 3
    └── 不通过 → 对应模块新会话修订

Step 3: 环境初始化 + 任务拆分
├── 会话N+1 [Architect agent]: 读架构 + 契约文档
│   ├── 初始化脚手架（含模块目录结构、导出桩文件）
│   ├── 生成 api-contracts-{module}.md 子文件
│   ├── 创建 GitHub Issues（含依赖关系）
│   ├── 规划集成测试用例（识别 L2 关键路径）
│   └── 回填 CLAUDE.md: 常用命令、测试环境
│
│   任务拆分原则：
│   ├── 共享层（shared/infra）独立为最高优先级 Task
│   ├── 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
│   ├── 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
│   ├── Task 间依赖关系标注为 DAG（在 Issue body 中声明 Depends on）
│   ├── 每个 Task 标注需通过的测试
│   └── 强类型语言：为每个模块创建导出桩文件（只声明签名，函数体抛 Not implemented）
│
│   模块内 Task 拆分策略：
│   ├── 按层拆分（CRUD 密集型）: repository → service → controller
│   ├── 按功能拆分（功能丰富型）: 注册登录 → 个人资料 → 权限管理
│   └── 拆不到粒度 → 说明模块划分需要回退到 Step 2a 调整
│
└── 技术负责人: review 脚手架、Issues
    ├── 通过 → 进入 Step 4
    └── 不通过 → 新会话修订

Step 4: 契约测试先行（按模块串行）
├── 会话 [Tester agent]: 写模块 A 的契约测试
├── 会话 [Tester agent]: 写模块 B 的契约测试
├── ...（每个模块一个会话，按依赖顺序串行推进）
├── 技术负责人: review 测试代码
│   ├── 通过 → 进入 Step 5
│   └── 不通过 → Tester agent 新会话修改
└── 技术负责人: 更新 GitHub Issues 状态

Step 5: 实现 + Review（按 Task 依赖顺序串行推进）
└── 循环 [按依赖顺序逐 Task 执行]:
    ├── 会话 [Implementer agent]: 实现当前 Task
    │   ├── 契约测试通过
    │   ├── L1 模块内集成测试通过
    │   ├── 被依赖模块已实现时 → 补充 L2 关键路径集成测试
    │   └── 完成后 gh issue comment 报告
    ├── 会话 [Reviewer agent]: 对照文档 + 测试 review
    │   ├── LGTM → 技术负责人更新 Issue 状态，进入下一个 Task
    │   ├── MUST FIX / SHOULD FIX → Implementer 新会话修复 → 重新 Review
    │   └── 涉及接口变更 → 停止，按变更传播规则处理
    └── 技术负责人: 更新 Issue 状态

    执行顺序：shared/infra → 被依赖的业务模块 → 依赖方业务模块
    L2 集成测试时机：当模块 B 依赖模块 A，且模块 A 已实现完成，
    模块 B 的 Implementer 在实现过程中编写跨模块集成测试（真实调用模块 A）

Step 6: E2E 测试
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

> **契约测试（Specification Test）**：基于 api-contracts.md 验证接口输入输出的规格测试，即"接口文档说什么，测试就验什么"。这**不是** Pact 风格的消费者驱动契约测试（CDCT）。
>
> **L1 集成测试（模块内）**：验证模块内部各层（如 controller → service → repository）的真实串联，使用真实依赖（如内存数据库），不 Mock 模块内部组件。
>
> **L2 集成测试（跨模块 / 关键路径）**：验证关键业务路径上多个模块的真实协作（如 下单 → 扣库存 → 创建支付单），不 Mock 其他模块。在被依赖模块实现完成后编写。
>
> **consumers 字段**：api-contracts.md 中每个接口标注的消费方列表，用于变更影响评估。

## 任务管理：GitHub Projects

使用 GitHub Projects + GitHub Issues 管理任务：

- **存储与状态追踪**：GitHub Issues，无并发瓶颈
- **依赖关系**：Issue body 中 `Depends on #N` + Sub-issues
- **程序化访问**：`gh` CLI + GraphQL API，AI agent 可直接操作
- **可视化**：Board（看板）/ Table（表格）/ Roadmap（时间线）视图
- **状态更新**：通过标签、Project 字段、Issue Comment

### GitHub Project 配置

**Project 自定义字段**：

| 字段 | 类型 | 选项 |
|------|------|------|
| Status | 单选 | Todo, In Progress, Review, Done, Blocked |
| Module | 单选 | shared, {module-a}, {module-b}, ... |
| Priority | 单选 | P0, P1, P2 |

**Issue 标签**：

| 标签 | 用途 |
|------|------|
| `type:contract-test` | 契约测试任务 |
| `type:impl` | 实现任务 |
| `type:integration-test` | 集成测试任务 |
| `type:e2e` | E2E 测试任务 |
| `type:infra` | 基础设施任务 |
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
  --project "{项目名}"

gh issue create --title "[user] 实现用户注册接口" \
  --body "Depends on #1\n..." --label "type:impl,module:user" \
  --project "{项目名}"

# 查看项目进度
gh issue list --state open --label "module:user"
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

**状态管理原则**：Agent 通过 Issue comment 报告进展，**技术负责人负责更新 Project Board 状态**。

### 依赖关系管理

**依赖声明**：Issue body 中用 `Depends on #N` 标注前置依赖。

**Sub-issues 层级**：将模块的多个 Task 组织为父子关系：

```
#10 [user] 用户模块实现                ← 父 Issue（模块粒度）
  ├── #11 [user] 实现 repository 层
  ├── #12 [user] 实现 service 层      ← Depends on #11
  └── #13 [user] 实现 controller 层   ← Depends on #12
```

## Git 策略

### 提交规范

- 直接在 main 分支开发，不使用 feature 分支
- commit 粒度：每个有意义的改动一个 commit
- commit message 格式：`<type>(<module>): <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 示例：`feat(order): 实现订单创建接口`、`fix(shared): 修正日期格式化时区问题`
- 不要把无关改动放在同一个 commit

### Task 完成流程

Reviewer 输出 LGTM 后，Task 即视为完成（代码已在 main 上），更新 GitHub Issue 状态即可。

## 文档分层策略

### CLAUDE.md 分层

**全局 CLAUDE.md（< 100 行）** — 所有 agent 自动加载：

```markdown
# Project: {项目名}
## 一句话描述
## Tech Stack
## 项目文档
## 常用命令
## 项目结构（只列顶层目录和模块名，不展开）
## 代码规范
## 架构约定
## 测试环境
## Git 规则
## 共享代码修改规则
## 不要做的事
## 错误处理规则
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

核心原则：**先更新文档 → 再更新测试 → 最后更新实现。** 按模块依赖顺序处理，被依赖的模块优先。

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

### 变更记录

- 在相关 GitHub Issue 中 comment 变更原因和影响范围
- commit message 标注：`docs(<module>): {变更内容}，影响范围: #{issue-list}`

## 测试策略

### 测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| 契约测试 | Tester agent | Step 4（实现前） | api-contracts.md | 必须 |
| 单元测试 | Implementer agent | Step 5（实现中） | 复杂内部逻辑 | 按需 |
| L1 模块内集成 | Implementer agent | Step 5（实现中） | controller → service → repository 串联 | **必须** |
| L2 关键路径集成 | Implementer agent（调用方） | Step 5（被依赖模块已实现后） | 跨模块真实调用 | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |

### Mock 策略

| 测试层级 | 模块间依赖 | 外部依赖（数据库、第三方 API） |
|---------|-----------|---------------------------|
| 契约测试 | Mock / Stub | Mock（内存数据库可替代） |
| 单元测试 | Mock / Stub | Mock |
| L1 模块内集成 | Mock 其他模块 | 真实连接或测试容器 |
| L2 跨模块集成 | **真实调用** | 真实连接或测试容器 |
| E2E 测试 | **真实调用** | 真实连接 |

### L2 集成测试的触发时机

当模块 B 依赖模块 A，且模块 A 已实现完成：

1. 模块 B 的 Implementer agent 在实现过程中编写跨模块集成测试
2. 使用真实的模块 A（不 Mock）
3. 串行开发天然保证被依赖模块先完成，无需额外协调

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

测试代码能编译/加载，但执行时全部失败（因为实现不存在）— 这是 TDD 的正常状态（先红后绿）。强类型语言通过 Step 3 的导出桩文件解决编译问题。

## Review 机制

### 分层 Review

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| Task Review | 每个 Task 完成 | Reviewer Agent | 功能正确性、代码规范、测试覆盖 |
| 模块 Review | 模块所有 Task 完成 | Reviewer Agent（模块级 prompt） | 模块内一致性、命名/风格统一、接口覆盖完整性 |
| 跨模块 Review | 涉及跨模块变更时 | 技术负责人 | 接口一致性、依赖方向、shared 修改合理性 |
| 架构 Review | 架构变更提议时 | 技术负责人 | 决策合理性、影响范围 |

**分层原则**：技术负责人只做系统级和跨模块 review，模块内 review 委托 Reviewer Agent。

### Review 输出标准

- **LGTM** — 通过，无需修改
- **MUST FIX** — 必须修复后重新 review
- **SHOULD FIX** — 建议修改，修改后重新 review
- **OPTIONAL** — 可选优化，不阻塞进度

## 会话管理

### 基本原则

**每个角色、每个任务使用独立的新会话。** 不在一个会话中让 agent 切换角色或跨 Task 工作。CLAUDE.md 在每个会话开始时自动加载，是 agent 获取项目上下文的主要入口。

### 上下文加载规则

- **模块 agent 只加载必要文档**：CLAUDE.md + api-contracts-{module}.md + module-design/{module}.md
- 不需要加载完整的 api-contracts.md 或其他模块的设计文档

### 什么时候必须开新会话

1. 切换角色时
2. 切换 Task 时（即使同一角色）
3. Review 不通过需要修复时
4. Agent 表现异常时

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
├── src/
│   └── modules/
│       ├── module-a/
│       │   ├── controller.ts
│       │   ├── service.ts
│       │   ├── repository.ts
│       │   ├── types.ts
│       │   └── index.ts             # 导出桩（Step 3 创建）
│       ├── module-b/
│       │   └── ...
│       └── shared/
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
- 判断标准：模块间有明确的优先级差异，或产品经理希望尽早验证核心流程

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
- 每个迭代结束时保持 main 可部署

## 速查：每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准 |
|------|--------|------|------|---------|
| 1 | 人 + Architect | — | PRD, CLAUDE.md（基础）, GitHub Project | PRD 按模块组织含验收标准；CLAUDE.md 基础部分确认；Project 已创建 |
| 2a | Architect | PRD, CLAUDE.md | architecture.md | 模块划分清晰；依赖单向无环；数据流完整 |
| 2b | Module Designer | architecture.md, PRD | module-design/*.md | 每模块内部设计完整；数据模型清晰 |
| 2c | API Designer | architecture + module-designs | api-contracts.md | 每个 PRD 功能映射到接口；consumers 完整；依赖矩阵完整；追溯表完整 |
| 3 | Architect | 架构 + 契约 | 脚手架, Issues, 模块 CLAUDE.md | 脚手架能运行；Issues 含依赖关系；模块 CLAUDE.md < 50 行 |
| 4 | Tester | api-contracts | 契约测试代码 | 测试能编译；执行时失败（TDD）；覆盖正常+异常流程 |
| 5 | Impl + Reviewer | 文档 + 测试 | 业务代码 | 契约测试 + L1 通过；L2 通过；全量测试通过 |
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

1. 检查 git 状态：`git status` + `git log` 确认最后 commit
2. 有未提交的改动且质量可接受 → 提交后新会话继续
3. 有未提交的改动但质量不确定 → `git stash`，新会话重新开始
4. 无未提交改动 → 新会话重新开始

### 实现过程中发现架构有问题

1. Agent 停止实现，在 Issue comment 中报告
2. 技术负责人评估影响范围
3. 回退到 Step 2a/2b：新会话修订架构文档
4. 按变更传播规则：文档 → 测试 → 实现

### 共享层变更需求

1. Implementer agent 在 Issue comment 中说明需求
2. 技术负责人评估：
   - 确实需要放 shared → 直接在 shared/ 中创建
   - 只有一个模块用 → 告知 agent 放在模块内部
   - 当前先放模块内部，后续提取 → 标注 `TODO: 提取到 shared`

### Agent 产出质量不达标

1. 给出具体修改要求（引用 Issue 编号、契约章节、代码行号）
2. 反复出现同类问题 → 在对应模块的 CLAUDE.md 中增加针对性约束
3. 质量仍不达标 → 将 Task 拆得更小，或技术负责人手动完成关键部分

## CI 集成建议

### 流水线策略

```
每次 push 到 main:
  lint + 全量契约测试 + 单元测试 + L1/L2 集成测试

定期 / 手动触发:
  全量测试 + E2E 测试
```

### GitHub Actions 示例

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

> 以上为 Node.js 项目示例。其他技术栈替换对应的 setup 和命令即可。测试命令应只运行已完成 Task 的测试（通过测试目录或标签过滤）。
