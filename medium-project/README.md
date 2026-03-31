# 中型项目 AI Agent 协作开发工作流

一套面向**中型全栈项目**的 AI Agent 协作开发流程，基于 Claude Code 的 skill 系统实现。

## 适用场景

- 前端 SPA + 后端 API + 管理后台
- 10-30 个页面，20-40 个端点
- 4-8 个业务模块

## 核心理念

- **文档驱动**：architecture.md → module-design → 契约测试 → 实现，先设计后编码
- **TDD**：契约测试在实现之前编写，先红后绿
- **角色隔离**：每个 skill 以 `context: fork` 在隔离子 agent 中运行，互不干扰
- **串行推进**：按模块依赖顺序逐个完成，确保被依赖模块先就绪
- **状态可追踪**：`docs/workflow-state.md` 记录当前阶段和模块进度

## 角色分工

| 角色 | 身份 | 职责 |
|------|------|------|
| 产品经理 | 人 | 编写 PRD，分批验收 |
| 技术负责人 | 人 | 技术选型，review，流转管理，调用 skill |
| Architect agent | AI | 架构设计、模块设计、脚手架、任务拆分 |
| Tester agent | AI | 契约测试、前端测试、E2E 测试 |
| Implementer agent | AI | 实现业务代码、集成测试 |
| Reviewer agent | AI | Task Review、模块 Review |

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
| `/mp-review-task` | Task Review | `<module> <issue-number>` |
| `/mp-review-fix` | Review 问题修复 | `<module> <issue-number>` |
| `/mp-review-module` | 模块级整体 Review | `<module>` |
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

完成后更新状态：
```
/mp-workflow-update Step 1 完成
```

### 3. 架构设计（Step 2）

```
/mp-architecture
```

技术负责人 review `docs/architecture.md`，通过后：
```
/mp-workflow-update Step 2 review 通过
```

### 4. 模块设计（Step 3）

```
# 后端模块（按依赖顺序）
/mp-module-design user
/mp-workflow-update user 模块设计 review 通过

/mp-module-design order
/mp-workflow-update order 模块设计 review 通过

# 前端模块
/mp-module-design web-app              # 整体设计
/mp-module-design web-app auth         # feature 级
/mp-module-design web-app product      # feature 级

# 汇总
/mp-module-design --summary
/mp-workflow-update Step 3 review 通过
```

### 5. 脚手架 + 任务拆分（Step 4）

```
/mp-scaffold
/mp-workflow-update 脚手架 review 通过

/mp-task-split
/mp-workflow-update Issues review 通过
```

### 6. 实现循环（Step 5）

```
# infra
/mp-impl-infra 1
/mp-workflow-update infra review 通过

# 每个模块重复以下循环：
/mp-test-contract user 5              # 写契约测试
/mp-workflow-update user 契约测试 review 通过

/mp-impl user 6                       # 实现 Task
/mp-review-task user 6                # Review
/mp-workflow-update Issue #6 review LGTM

# ... 更多 Task ...

/mp-review-module user                # 模块 Review
/mp-workflow-update user 模块 Review LGTM

/mp-test-integration 10               # L2 集成测试
/mp-workflow-update user L2 集成测试完成
```

### 7. E2E + 验收（Step 6-7）

```
/mp-test-e2e
/mp-workflow-update E2E 测试通过
```

产品经理分批验收。

## 随时查看进度

```
/mp-workflow
```

输出当前阶段、当前模块进度、下一步操作建议。

## 文件结构

```
medium-project/                         # 工作流定义
├── README.md                           # 本文件
├── workflow.md                         # 核心流程（角色、7 步流程、术语）
├── tech-lead-guide.md                  # 技术负责人操作指南
└── templates/
    └── CLAUDE.md                       # CLAUDE.md 模板

.claude/skills/                         # Skill 定义（15 个）
├── mp-workflow/                        # 流程查询
├── mp-workflow-update/                 # 状态更新
├── mp-architecture/                    # Step 2: 架构设计
│   ├── SKILL.md
│   └── architecture-template.md        # 架构文档模板
├── mp-module-design/                   # Step 3: 模块设计
│   ├── SKILL.md
│   └── module-design-template.md       # 模块设计模板
├── mp-scaffold/                        # Step 4a: 脚手架
├── mp-task-split/                      # Step 4b: 任务拆分
├── mp-impl-infra/                      # Step 5a: infra 实现
├── mp-test-contract/                   # Step 5b: 后端契约测试
├── mp-test-frontend/                   # Step 5b: 前端测试
├── mp-impl/                            # Step 5c: 业务实现
├── mp-review-task/                     # Step 5d: Task Review
├── mp-review-fix/                      # Step 5e: Review 修复
├── mp-review-module/                   # Step 5f: 模块 Review
├── mp-test-integration/                # Step 5g: L2 集成测试
└── mp-test-e2e/                        # Step 6: E2E 测试
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
    ├── contracts/                      # 契约测试
    ├── integration/                    # L1 + L2 集成测试
    ├── e2e/                            # E2E 测试
    └── fixtures/                       # 共享测试数据
```
