# 中型项目 AI Agent 协作开发工作流

一套面向**中型全栈项目**的 AI Agent 协作开发流程，基于 Claude Code 的 skill 系统实现。

## 适用场景

- 前端 SPA + 后端 API + 管理后台
- 10-30 个页面，20-40 个端点
- 4-8 个业务模块

## 核心理念

- **文档驱动**：architecture.md → module-design → 契约测试 → 实现，先设计后编码
- **TDD**：契约测试在实现之前编写，先红后绿
- **短上下文**：主会话进行项目流程跟踪，真正做事在子会话（执行类 skill 以 `context: fork` 在隔离子 agent 中运行；流程管控 skill `mp-workflow` / `mp-workflow-update` 在主会话运行）
- **状态可追踪**：`docs/workflow-state.md` 记录当前阶段和模块进度
- **状态更新职责分离**：执行类 skill 只将状态推进到"等待 review"；review 通过/不通过的状态闸门一律由技术负责人通过 `/mp-workflow-update` 触发

## 角色分工

| 角色 | 身份 | 职责 |
|------|------|------|
| 产品经理 | 人 | 编写 PRD，分批验收 |
| 技术负责人 | 人 | 技术选型，review，流转管理，调用 skill |
| Architect agent | AI | 架构设计、模块设计、脚手架、任务拆分 |
| Tester agent | AI | 契约测试、前端测试、E2E 测试 |
| Implementer agent | AI | 实现业务代码、集成测试 |
| Reviewer agent | AI | 全阶段 Review（PRD / 架构 / 设计 / 脚手架 / Issues / infra / 契约测试 / Task / 模块 / L2 / E2E / 验收预检） |

技术负责人是唯一的操作者，通过调用不同的 `/mp-*` skill 驱动 AI agent 完成各阶段工作。

## 开发流程总览

```
Step 1  PRD 审查 + 初始化                    ← 技术负责人手动操作
Step 2  系统架构设计                          ← /mp-architecture
Step 3  模块详细设计 + 接口契约                ← /mp-module-design
Step 4  脚手架 + 任务拆分                     ← /mp-scaffold + /mp-task-split
Step 5  契约测试 → 实现 → Review（按模块串行）  ← 多个 skill 循环调用
Step 6  E2E 测试                             ← /mp-test-e2e
Step 7  验收                                 ← 产品经理手动操作
```

## Skill 清单

### 流程管控

| Skill | 用途 |
|-------|------|
| `/mp-workflow` | 查看当前阶段和下一步操作（只读） |
| `/mp-workflow-update` | 更新流程状态（如 "Step 2 review 通过了"） |

### Review（全阶段 Agent 辅助 Review）

| Skill | 用途 | 参数 |
|-------|------|------|
| `/mp-review-prd` | PRD Review | — |
| `/mp-review-architecture` | 架构 Review | — |
| `/mp-review-module-design` | 模块设计 + 接口契约 Review | `<module>` / `--summary` |
| `/mp-review-scaffold` | 脚手架 Review | — |
| `/mp-review-issues` | Issues Review | — |
| `/mp-review-infra` | infra 实现 Review | `<issue-number>` |
| `/mp-review-contract` | 契约测试 Review | `<module> <issue-number> [feature]` |
| `/mp-review-task` | Task 代码 Review | `<module> <issue-number> [feature]` |
| `/mp-review-fix` | Review 问题修复 | `<module> <issue-number> [feature]` |
| `/mp-review-feature` | 前端 Feature 级整体 Review | `<module> <feature>` |
| `/mp-review-module` | 后端模块级整体 Review | `<module>` |
| `/mp-review-module-frontend` | 前端模块级整体 Review | `<module>` |
| `/mp-review-integration` | L2 集成测试 Review | `<issue-number>` |
| `/mp-review-e2e` | E2E 测试 Review | — |
| `/mp-review-acceptance` | 验收预检 | — |

### 设计阶段（Step 2-3）

| Skill | 用途 | 参数 |
|-------|------|------|
| `/mp-architecture` | 系统架构设计 → `docs/architecture.md` | — |
| `/mp-module-design` | 模块详细设计 + 接口契约 | `<module> [feature]` / `--summary` |

### 初始化阶段（Step 4）

| Skill | 用途 | 参数 |
|-------|------|------|
| `/mp-scaffold` | 项目脚手架 + 回填 CLAUDE.md | — |
| `/mp-task-split` | 拆分任务 + 创建 GitHub Issues | — |

### 实现阶段（Step 5）

| Skill | 用途 | 参数 |
|-------|------|------|
| `/mp-impl-infra` | 实现 infra 基础设施 | `<issue-number>` |
| `/mp-test-contract` | 后端模块契约测试 | `<module> <issue-number>` |
| `/mp-test-frontend` | 前端 feature 测试 | `<module> <feature> <issue-number>` |
| `/mp-impl` | 实现业务 Task | `<module> <issue-number> [feature]` |
| `/mp-test-integration` | L2 跨模块集成测试 | `<issue-number>` |

### 测试阶段（Step 6）

| Skill | 用途 | 参数 |
|-------|------|------|
| `/mp-test-e2e` | E2E 测试 | — |

## 快速开始

### 1. 准备 PRD

产品经理编写 `docs/prd.md`，按模块组织需求，每个模块包含验收标准。

### 2. 初始化项目

```bash
# 创建仓库
git init && gh repo create {项目名} --private

# 初始化流程状态
/mp-workflow-update init
```

技术负责人审查 PRD，创建 GitHub Project（配置见 `tech-lead-guide.md`），填写 CLAUDE.md 基础信息。

```
/mp-review-prd                         # Agent 先 review PRD
# 技术负责人参考 Agent 结论，确认后：
/mp-workflow-update Step 1 完成
```

### 3. 架构设计（Step 2）

```
/mp-architecture
/mp-review-architecture                # Agent review 架构
# 技术负责人参考 Agent 结论，确认后：
/mp-workflow-update Step 2 review 通过
```

### 4. 模块设计（Step 3）

```
# 后端模块（按依赖顺序）
/mp-module-design user
/mp-review-module-design user          # Agent review 模块设计
/mp-workflow-update user 模块设计 review 通过

/mp-module-design order
/mp-review-module-design order
/mp-workflow-update order 模块设计 review 通过

# 前端模块
/mp-module-design web-app              # 整体设计
/mp-module-design web-app auth         # feature 级
/mp-module-design web-app product      # feature 级

# 汇总
/mp-module-design --summary
/mp-review-module-design --summary     # Agent 汇总检查
/mp-workflow-update Step 3 review 通过
```

### 5. 脚手架 + 任务拆分（Step 4）

```
/mp-scaffold
/mp-review-scaffold                    # Agent review 脚手架
/mp-workflow-update 脚手架 review 通过

/mp-task-split
/mp-review-issues                      # Agent review Issues
/mp-workflow-update Issues review 通过
```

### 6. 实现循环（Step 5）

```
# infra
/mp-impl-infra 1
/mp-review-infra 1                     # Agent review infra
/mp-workflow-update infra #1 review 通过

# 每个模块重复以下循环：
/mp-test-contract user 5              # 写契约测试
/mp-review-contract user 5            # Agent review 契约测试
/mp-workflow-update user 契约测试 #5 review 通过

/mp-impl user 6                       # 实现 Task（skill 自动设状态为"等待 review"）
/mp-review-task user 6                # Agent review Task（skill 只输出结论，不改状态）
/mp-workflow-update Issue #6 review LGTM  # 技术负责人确认后推进状态（自动关闭 Issue）

# ... 更多 Task ...

/mp-review-module user                # Agent 后端模块 Review
/mp-workflow-update user 模块 Review LGTM

/mp-test-integration 10               # L2 集成测试
/mp-review-integration 10             # Agent review L2 集成测试
/mp-workflow-update user L2 集成测试 #10 完成

# 前端模块（每个 feature 重复以下循环）：
/mp-test-frontend web-app auth 8      # 写前端测试
/mp-review-contract web-app 8 auth    # Agent review 前端测试
/mp-workflow-update web-app auth 契约测试 #8 review 通过

/mp-impl web-app 9 auth              # 实现 Task
/mp-review-task web-app 9 auth       # Agent review Task
/mp-workflow-update Issue #9 review LGTM

# ... auth feature 更多 Task ...

/mp-review-feature web-app auth       # Agent Feature Review
/mp-workflow-update web-app auth Feature Review LGTM

# ... 更多 feature（product 等）...

/mp-review-module-frontend web-app    # Agent 前端模块 Review（跨 feature 一致性）
/mp-workflow-update web-app 模块 Review LGTM

/mp-test-integration 15               # L2 集成测试
/mp-review-integration 15
/mp-workflow-update web-app L2 集成测试 #15 完成
```

### 7. E2E + 验收（Step 6-7）

```
/mp-test-e2e
/mp-review-e2e                         # Agent review E2E 测试
/mp-workflow-update E2E 测试通过

/mp-review-acceptance                  # Agent 验收预检
# 产品经理分批验收
/mp-workflow-update 验收通过
```

## 术语说明

- **契约测试（Specification Test）**：基于 module-design/{module}.md 中的接口契约验证接口输入输出的规格测试，即"接口文档说什么，测试就验什么"。这**不是** Pact 风格的消费者驱动契约测试（CDCT）。
- **L1 集成测试（模块内）**：验证模块内部各层（如 controller → service → repository）的真实串联，使用真实依赖（如内存数据库），不 Mock 模块内部组件。
- **L2 集成测试（跨模块 / 关键路径）**：验证关键业务路径上多个模块的真实协作（如 下单 → 扣库存 → 创建支付单），不 Mock 其他模块。
- **前端契约测试（API 层 + 页面渲染）**：由 `/mp-test-frontend` 编写，验证 API 请求/响应规格和页面渲染正确性，mock 粒度较粗（mock hooks 或 MSW）。
- **前端 L1 集成测试（端内串联）**：由 `/mp-impl` 在实现时编写，验证页面 → hooks → API 层的真实数据流转，仅在网络层使用 MSW mock。两者测试目标不同，不应重复。
- **consumers 字段**：接口契约中每个接口标注的消费方列表，用于变更影响评估。

## 随时查看进度

```
/mp-workflow
```

输出当前阶段、当前模块进度、下一步操作建议。

## 文件结构

```
medium-project/                         # 工作流定义
├── README.md                           # 本文件
├── tech-lead-guide.md                  # 技术负责人操作指南
└── skills/                             # Skill 定义（27 个）
    ├── mp-workflow/                     # 流程查询
    ├── mp-workflow-update/              # 状态更新
    ├── mp-review-prd/                  # Step 1: PRD Review
    ├── mp-architecture/                # Step 2: 架构设计
    ├── mp-review-architecture/         # Step 2: 架构 Review
    ├── mp-module-design/               # Step 3: 模块设计
    ├── mp-review-module-design/        # Step 3: 模块设计 Review
    ├── mp-scaffold/                    # Step 4a: 脚手架
    ├── mp-review-scaffold/             # Step 4a: 脚手架 Review
    ├── mp-task-split/                  # Step 4b: 任务拆分
    ├── mp-review-issues/               # Step 4b: Issues Review
    ├── mp-impl-infra/                  # Step 5a: infra 实现
    ├── mp-review-infra/                # Step 5a: infra Review
    ├── mp-test-contract/               # Step 5b: 后端契约测试
    ├── mp-test-frontend/               # Step 5b: 前端测试
    ├── mp-review-contract/             # Step 5b: 契约测试 Review
    ├── mp-impl/                        # Step 5c: 业务实现
    ├── mp-review-task/                 # Step 5d: Task Review
    ├── mp-review-feature/              # Step 5f: 前端 Feature Review
    ├── mp-review-fix/                  # Step 5e: Review 修复
    ├── mp-review-module/               # Step 5f: 后端模块 Review
    ├── mp-review-module-frontend/      # Step 5f: 前端模块 Review
    ├── mp-test-integration/            # Step 5g: L2 集成测试
    ├── mp-review-integration/          # Step 5g: L2 集成测试 Review
    ├── mp-test-e2e/                    # Step 6: E2E 测试
    ├── mp-review-e2e/                  # Step 6: E2E Review
    └── mp-review-acceptance/           # Step 7: 验收预检
```

## 目标项目结构

使用本工作流产出的项目结构：

```
project/
├── CLAUDE.md                           # AI Agent 上下文入口
├── docs/
│   ├── prd.md                          # 产品需求
│   ├── architecture.md                 # 系统架构
│   ├── module-design/                  # 模块设计 + 接口契约
│   └── workflow-state.md               # 流程状态追踪
├── server/                             # 后端 (Express + Prisma)
│   ├── modules/{module}/               # 业务模块（controller/service/repository）
│   └── infra/                          # 基础设施
├── web/                                # 前端 SPA (React)
│   ├── features/{feature}/             # 按业务域组织
│   └── shared/                         # 共享层
├── admin/                              # 管理后台
└── tests/
    ├── contracts/                      # 契约测试（按模块组织，前端按 feature 子目录）
    ├── unit/                           # 单元测试（按需）
    ├── integration/                    # L1 + L2 集成测试
    │   ├── {module}/                   # L1: 后端模块内集成
    │   ├── {module}/{feature}/         # L1: 前端按 feature 子目录
    │   └── paths/                      # L2: 关键路径集成
    ├── e2e/                            # E2E 测试
    └── fixtures/                       # 共享测试数据
```
