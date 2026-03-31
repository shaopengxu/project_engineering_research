# 中型项目开发流程规范

### 适用项目

全栈应用：前端 SPA + 后端 API + 管理后台，10-30 个页面 + 20-40 个端点。

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
| 模块设计 + 接口契约 (module-design/{module}.md) | Architect agent | 技术负责人 | 必须 |
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
├── 新会话 [Architect agent]: 读 PRD → 产出 CLAUDE.md 基础部分建议
│   └── 一句话描述、Tech Stack、项目文档、代码规范、Git 规则、共享代码修改规则、不要做的事、错误处理规则
└── 技术负责人: review 并确认 CLAUDE.md 基础部分

Step 2: 系统架构设计
├── 新会话 [Architect agent]: 读 PRD → 产出 architecture.md（系统级）
│   ├── 模块划分与职责定义
│   ├── 模块依赖关系图（有向无环）
│   ├── 跨模块数据流
│   ├── 部署架构概要
│   └── 补充 CLAUDE.md: 项目结构概览、架构约定、不要做的事（架构相关）
└── 技术负责人: review
    ├── 通过 → 进入 Step 3
    └── 不通过 → 新会话修订

Step 3: 模块详细设计 + 接口契约
├── 后端模块（按依赖顺序串行）：
│   ├── 新会话 [Architect agent]: → module-design/module-a.md（含接口契约五要素）
│   ├── 新会话 [Architect agent]: → module-design/module-b.md
│   └── ...
├── 前端模块（后端模块全部完成后）：
│   ├── 新会话 [Architect agent]: → module-design/web-app.md（页面、路由、组件、调用的后端接口）
│   ├── 新会话 [Architect agent]: → module-design/admin.md
│   └── ...
├── 最后一个模块完成后：补充 architecture.md 的接口依赖矩阵 + 需求追溯表 + 接口通用约定 + 部署概要
└── 技术负责人: review 所有模块设计
    ├── 通过 → 进入 Step 3
    └── 不通过 → 对应模块新会话修订

Step 4: 环境初始化 + 任务拆分
├── 新会话 [Architect agent]: 读架构 + 模块设计文档
│   ├── 初始化脚手架（含模块目录结构、导出桩文件）
│   ├── 创建 GitHub Issues（含依赖关系）
│   ├── 规划集成测试用例（识别 L2 关键路径）
│   └── 回填 CLAUDE.md: 常用命令、测试环境
│
│   任务拆分原则：
│   ├── infra 独立为最高优先级 Task
│   ├── 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
│   ├── 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
│   ├── Task 间依赖关系标注为 DAG（在 Issue body 中声明 Depends on）
│   ├── 每个 Task 标注需通过的测试
│   └── 强类型语言：为每个模块创建导出桩文件（只声明签名，函数体抛 Not implemented）
│
│   模块内 Task 拆分策略：
│   ├── 按层拆分（CRUD 密集型）: repository → service → controller
│   ├── 按功能拆分（功能丰富型）: 注册登录 → 个人资料 → 权限管理
│   └── 拆不到粒度 → 说明模块划分需要回退到 Step 2 调整
│
└── 技术负责人: review 脚手架、Issues
    ├── 通过 → 进入 Step 5
    └── 不通过 → 新会话修订

Step 5: 契约测试 + 实现 + Review（按模块串行推进）
└── 循环 [按依赖顺序逐模块执行]：infra → 被依赖的后端模块 → 依赖方后端模块 → 前端模块
    │
    ├── 5a. infra 模块处理：
    │   ├── 新会话 [Implementer agent]: 实现 infra（数据库连接、配置、错误处理、响应格式）
    │   ├── 验收标准：依赖安装成功、lint 通过、数据库连接成功、错误处理中间件可用
    │   └── 技术负责人: review 后继续
    │
    ├── 5b. 后端模块：基于接口契约的规格测试
    │   ├──  新会话 [Tester agent]: 写当前模块的后端的测试
    │   └── 技术负责人: review 测试代码
    │       ├── 通过 → 继续实现
    │       └── 不通过 → Tester agent 新会话修改
    │
    ├── 5c. 前端模块：API 调用层测试 + 页面渲染测试
    │   ├──  新会话 [Tester agent]: 写当前模块的前端的测试
    │   └── 技术负责人: review 测试代码
    │       ├── 通过 → 继续实现
    │       └── 不通过 → Tester agent 新会话修改
    │
    ├── 循环 [按 Task 依赖顺序逐 Task 执行]:
    │   ├── 5d. 新会话 [Implementer agent]: 实现当前 Task
    │   │   ├── 契约测试通过
    │   │   ├── L1 集成测试通过（后端：controller→service→repository；前端：页面→hooks→API）
    │   │   ├── commit message 包含 Task 标识：`[#issue-number]`
    │   │   └── 完成后 gh issue comment 报告
    │   ├── 5e. 新会话 [Reviewer agent]: 根据 commit message 中的 `[#issue-number]` 定位相关提交，对照文档 + 测试 review
    │   │   ├── LGTM → 进入下一个 Task
    │   │   ├── MUST FIX / SHOULD FIX → 5f. Implementer 新会话修复 → 重新 Review
    │   │   └── 涉及接口变更 → 停止，按变更传播规则处理
    │   └── 技术负责人: 更新 Issue 状态
    │
    ├── 5g. 当前模块所有 Task 完成 → 模块级 Review
    ├── 5h. L2 关键路径集成测试（当被依赖模块已实现完成时）
    │   └── 新会话 [Implementer agent]: 编写跨模块集成测试（真实调用，不 Mock 其他模块）
    └── 技术负责人: 确认当前模块完成，推进下一个模块

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

> **契约测试（Specification Test）**：基于 module-design/{module}.md 中的接口契约验证接口输入输出的规格测试，即"接口文档说什么，测试就验什么"。这**不是** Pact 风格的消费者驱动契约测试（CDCT）。
>
> **L1 集成测试（模块内）**：验证模块内部各层（如 controller → service → repository）的真实串联，使用真实依赖（如内存数据库），不 Mock 模块内部组件。
>
> **L2 集成测试（跨模块 / 关键路径）**：验证关键业务路径上多个模块的真实协作（如 下单 → 扣库存 → 创建支付单），不 Mock 其他模块。在当前模块完成且被依赖模块已实现后，开独立会话编写。
>
> **consumers 字段**：接口契约中每个接口标注的消费方列表，用于变更影响评估。

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
| Module | 单选 | infra, {module-a}, {module-b}, web-app, admin, ... |
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
gh issue create --title "[infra] 初始化基础设施" \
  --body "..." --label "type:infra,module:infra" \
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
- commit message 格式：`<type>(<module>): <描述为什么改> [#issue-number]`
- type: feat / fix / docs / refactor / test
- 示例：`feat(order): 实现订单创建接口 [#12]`、`fix(infra): 修正错误处理中间件 [#3]`
- 不要把无关改动放在同一个 commit
- Task 标识 `[#issue-number]` 用于 Reviewer agent 定位相关提交

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

**architecture.md**：系统级内容（模块划分、依赖关系图、部署架构、跨模块数据流、接口通用约定、接口依赖矩阵、需求追溯表）。

**module-design/{module}.md**：每个模块的内部设计（分层、数据模型）+ 该模块的完整接口契约（五要素）。

### 跨模块 agent 的信息边界

Module-B 的 agent 关于 Module-A **需要知道的**：

- 公开接口签名和返回类型
- 错误码定义
- 相关数据模型

**不需要知道的**：

- 内部实现逻辑、目录结构、单元测试、技术债

这些信息通过 `module-design/{module-a}.md` 中的"接口契约"和"消费的外部接口"部分提供。

## 文档变更传播规则

核心原则：**先更新文档 → 再更新测试 → 最后更新实现。** 按模块依赖顺序处理，被依赖的模块优先。

### 接口契约变更

1. 查看 architecture.md 的**接口依赖矩阵**，识别所有受影响的消费方模块
2. 更新提供方的 module-design/{module}.md 中的接口定义
3. 更新消费方的 module-design 中的"消费的外部接口"
4. 同步更新 architecture.md 的接口依赖矩阵（如影响范围变化）
5. 在受影响模块的 GitHub Issue 中 comment 变更通知
6. Tester agent 新会话更新契约测试
7. 已完成的实现如涉及变更接口，标记 Issue 为"需更新"

### architecture.md 变更

1. 评估是否影响模块划分和依赖关系
2. 更新受影响的 module-design/{module}.md
3. 更新 CLAUDE.md 中的项目结构（如有变化）

### 变更记录

- 在相关 GitHub Issue 中 comment 变更原因和影响范围
- commit message 标注：`docs(<module>): {变更内容}，影响范围: #{issue-list}`

## 测试策略

### 测试分层

#### 后端模块测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| 契约测试 | Tester agent | Step 5（模块实现前） | module-design/{module}.md 接口契约 | 必须 |
| 单元测试 | Implementer agent | Step 5（实现中） | 复杂内部逻辑 | 按需 |
| L1 模块内集成 | Implementer agent | Step 5（实现中） | controller → service → repository 串联 | **必须** |
| L2 关键路径集成 | Implementer agent | Step 5（模块完成后独立会话） | 跨模块真实调用 | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |

#### 前端模块测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| API 调用层测试 | Tester agent | Step 5（模块实现前） | module-design 中"调用的后端接口" | 必须 |
| 页面渲染测试 | Tester agent | Step 5（模块实现前） | module-design 中"页面与路由" | 必须 |
| 页面集成测试 | Implementer agent | Step 5（实现中） | 页面 → hooks → API 层串联（mock 后端） | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |

> **前端契约测试说明**：前端的"契约测试"等价物是 API 调用层测试 + 页面渲染测试。API 调用层测试验证请求参数和响应处理与 module-design 中后端接口定义一致；页面渲染测试验证页面组件能正确渲染 mock 数据并响应用户交互。

### Mock 策略

#### 后端

| 测试层级 | 模块间依赖 | 外部依赖（数据库、第三方 API） |
|---------|-----------|---------------------------|
| 契约测试 | Mock / Stub | Mock（内存数据库可替代） |
| 单元测试 | Mock / Stub | Mock |
| L1 模块内集成 | Mock 其他模块 | 真实连接或测试容器 |
| L2 跨模块集成 | **真实调用** | 真实连接或测试容器 |
| E2E 测试 | **真实调用** | 真实连接 |

#### 前端

| 测试层级 | 后端 API | 浏览器环境 |
|---------|---------|-----------|
| API 调用层测试 | Mock（MSW 或手动 mock） | jsdom |
| 页面渲染测试 | Mock（MSW 或手动 mock） | jsdom |
| 页面集成测试 | Mock（MSW 或手动 mock） | jsdom |
| E2E 测试 | **真实调用** | 真实浏览器（Playwright） |

### L2 集成测试的触发时机

当模块 B 依赖模块 A，且模块 A 已实现完成：

1. 模块 B 完成所有 Task 和模块级 Review 后，开独立会话编写跨模块集成测试
2. 使用真实的模块 A（不 Mock）
3. 串行开发天然保证被依赖模块先完成，无需额外协调

### infra 模块说明

infra 是技术基础设施模块，不属于业务模块，因此不走契约测试流程。

**infra 包含的内容**：
- 数据库连接和 Prisma Client 初始化
- 配置管理（环境变量加载）
- 全局错误处理中间件
- 标准响应格式工具函数
- 通用中间件（认证、日志等）

**infra 的验收标准**：
- 依赖安装成功，lint 通过
- 数据库连接成功（开发环境和测试环境）
- 错误处理中间件能正确捕获和格式化错误
- 标准响应格式工具函数可用
- 所有后续模块可以正常导入和使用 infra 提供的功能

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

### 契约测试预期状态

测试代码能编译/加载，但执行时全部失败（因为实现不存在）— 这是 TDD 的正常状态（先红后绿）。强类型语言通过 Step 4 的导出桩文件解决编译问题。

## Review 机制

### 分层 Review

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| Task Review | 每个 Task 完成 | Reviewer Agent | 功能正确性、代码规范、测试覆盖 |
| 模块 Review | 模块所有 Task 完成 | Reviewer Agent（模块级 prompt） | 模块内一致性、命名/风格统一、接口覆盖完整性 |
| 跨模块 Review | 涉及跨模块变更时 | 技术负责人 | 接口一致性、依赖方向、infra 修改合理性 |
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

- **模块 agent 只加载必要文档**：CLAUDE.md + module-design/{module}.md
- 需要了解其他模块接口时，只读对应 module-design 的"接口契约"部分

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
│   ├── architecture.md              # 系统级架构（含接口通用约定、依赖矩阵、需求追溯表）
│   ├── module-design/               # 模块详细设计 + 接口契约
│   │   ├── module-a.md
│   │   └── module-b.md
├── server/                          # 后端
│   ├── modules/
│   │   ├── module-a/
│   │   │   ├── controller.ts
│   │   │   ├── service.ts
│   │   │   ├── repository.ts
│   │   │   ├── types.ts
│   │   │   └── index.ts             # 导出桩（Step 4 创建）
│   │   └── module-b/
│   │       └── ...
│   ├── infra/                       # 基础设施（数据库、配置、错误处理、响应格式）
│   └── app.ts
├── web/                             # 前端 SPA
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   ├── api/
│   └── stores/
├── admin/                           # 管理后台（结构同 web/）
│   └── ...
└── tests/
    ├── contracts/                   # 契约测试（按模块）
    ├── unit/                        # 单元测试（按模块）
    ├── integration/                 # 集成测试
    │   ├── {module-a}/              # L1 模块内
    │   └── paths/                   # L2 关键路径
    ├── e2e/                         # E2E 测试
    └── fixtures/                    # 共享测试数据
```

## 数据库迁移策略

- 使用 Prisma Migrate 管理数据库 schema 变更
- 统一一个 `prisma/schema.prisma` 文件，所有模块的数据模型集中定义
- Step 4 脚手架阶段：根据 module-design 中的数据模型创建初始 schema，运行 `npx prisma migrate dev --name init`
- Step 5 实现阶段：模块实现中如需调整数据模型，先更新 module-design 文档，再更新 schema.prisma，最后运行 `npx prisma migrate dev --name <描述>`
- 每次 migration 生成后立即 commit，commit message: `docs(infra): migration <描述> [#issue-number]`
- 测试环境使用独立数据库，通过 `DATABASE_URL` 环境变量区分

## 开发环境配置

Step 4 脚手架阶段需完成以下环境配置：

- **环境变量**：创建 `.env.example` 文件，列出所有必需的环境变量（`DATABASE_URL`、`PORT` 等），`.env` 加入 `.gitignore`
- **数据库**：本地 PostgreSQL 实例，在 README.md 或 `.env.example` 中说明连接方式
- **测试数据库**：独立的 PostgreSQL 测试库，测试前自动 migrate，测试后数据隔离（事务回滚或 truncate）
- **启动验证**：脚手架完成后确保 `npm install` + `npm run dev:server` + `npm run dev:web` 均可正常启动
- **TypeScript 配置**：根目录 `tsconfig.json` + 各端独立 tsconfig（server、web、admin）

## 迭代管理

### 何时需要多迭代

- 4-5 个模块：通常 1 个迭代
- 6-8 个模块：建议 2-3 个迭代
- 判断标准：模块间有明确的优先级差异，或产品经理希望尽早验证核心流程

### 迭代划分

使用 **GitHub Milestones** 管理迭代：

```
Milestone 1: 核心模块
  后端: infra + user + product
  前端: web-app（用户注册/登录 + 商品列表页面）
  → Step 2-7 完整走一遍
  → 实现顺序: infra → user → product → web-app（相关页面）
  → 产品经理验收核心流程

Milestone 2: 交易模块
  后端: order + payment + inventory
  前端: web-app（下单/支付页面）+ admin（订单管理页面）
  → Step 2（增量：只设计新模块，review 对已有模块的影响）→ Step 4-7
  → 实现顺序: inventory → order → payment → web-app（新页面）→ admin
  → 产品经理验收交易流程

Milestone 3: 辅助模块
  后端: notification + coupon + analytics
  前端: admin（剩余管理页面）
  → 同上（增量模式）
  → 最终全量验收
```

> **前端模块时序**：每个迭代内，前端模块在其依赖的后端模块全部完成后再实现。前端模块可按迭代拆分（只实现与本迭代后端模块对应的页面），不必等所有后端模块完成。

### 迭代间的关系

- 后续迭代的 Step 2 只设计本迭代新增模块，但必须 review 对已有模块的影响
- 已有模块的接口如需变更，按变更传播规则处理
- 每个迭代结束时保持 main 可部署

## 速查：每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准 |
|------|--------|------|------|---------|
| 1 | 人 + Architect | — | PRD, CLAUDE.md（基础）, GitHub Project | PRD 按模块组织含验收标准；CLAUDE.md 基础部分确认；Project 已创建 |
| 2 | Architect | PRD, CLAUDE.md | architecture.md | 模块划分清晰；依赖单向无环；数据流完整 |
| 3 | Architect | architecture.md, PRD | module-design/*.md | 每模块内部设计 + 接口契约完整；数据模型清晰 |
| 4 | Architect | 架构 + 模块设计 | 脚手架, Issues | 脚手架能运行；Issues 含依赖关系 |
| 5 | Tester + Impl + Reviewer | module-design + 测试 | 契约测试 + 业务代码 + L1/L2 集成测试 | 按模块串行：契约测试通过 → L1 通过 → 模块 Review 通过 → L2 通过 |
| 6 | Tester + 技术负责人 | PRD 验收标准 | E2E 测试, README.md | 核心路径 E2E 通过；README.md 完成 |
| 7 | 产品经理 | PRD | 验收确认 | 分批验收全部通过 |

## 增量开发（已有项目加新功能）

| 场景 | 起始步骤 | 说明 |
|------|---------|------|
| 新增业务模块 | Step 2（评估对现有架构影响） | 更新 architecture.md 依赖图，然后 3 → 4 → ... |
| 已有模块增加接口 | Step 3（更新 module-design/{module}.md） | 同时更新 architecture.md 依赖矩阵 |
| 跨多模块的新功能 | Step 2（影响评估） | 查接口依赖矩阵确定影响范围 → 3 → 5 |
| 模块内重构不改接口 | Step 5（实现阶段） | 契约测试不需要改（接口没变） |
| 修 bug | 不走流程 | 直接改 + 补测试 + 提交 |

关键原则：**变了什么文档，就从那个文档对应的步骤开始往后走。** 改了接口 → 从契约测试开始更新；只改实现 → 直接进入实现阶段。

## 常见故障与恢复

### Agent 会话崩溃

1. 检查 git 状态：`git status` + `git log` 确认最后 commit
2. 有未提交的改动且质量可接受 → 提交后新会话继续
3. 有未提交的改动但质量不确定 → `git stash`，新会话重新开始
4. 无未提交改动 → 新会话重新开始

### 实现过程中发现架构有问题

1. Agent 停止实现，在 Issue comment 中报告
2. 技术负责人评估影响范围
3. 回退到 Step 2/3：新会话修订架构文档
4. 按变更传播规则：文档 → 测试 → 实现

### infra 变更需求

1. Implementer agent 在 Issue comment 中说明需求
2. 技术负责人评估后确认或拒绝

### Agent 产出质量不达标

1. 给出具体修改要求（引用 Issue 编号、契约章节、代码行号）
2. 反复出现同类问题 → 在 CLAUDE.md 中增加针对性约束
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
