# 技术负责人操作指南（中型项目）

## Skill 速查

| Step | Skill | 参数 |
|------|-------|------|
| 1. PRD Review | `/mp-review-prd` | — |
| 2. 系统架构 | `/mp-architecture` | — |
| 2. 架构 Review | `/mp-review-architecture` | — |
| 3. 模块设计 | `/mp-module-design` | `<module> [feature]` / `--summary` |
| 3. 模块设计 Review | `/mp-review-module-design` | `<module>` / `--summary` |
| 4a. 脚手架 | `/mp-scaffold` | — |
| 4a. 脚手架 Review | `/mp-review-scaffold` | — |
| 4b. 任务拆分 | `/mp-task-split` | — |
| 4b. Issues Review | `/mp-review-issues` | — |
| 5a. infra 实现 | `/mp-impl-infra` | `<issue-number>` |
| 5a. infra Review | `/mp-review-infra` | `<issue-number>` |
| 5b. 后端契约测试 | `/mp-test-contract` | `<module> <issue-number>` |
| 5b. 前端测试 | `/mp-test-frontend` | `<module> <feature> <issue-number>` |
| 5b. 契约测试 Review | `/mp-review-contract` | `<module> <issue-number> [feature]` |
| 5c. 实现 Task | `/mp-impl` | `<module> <issue-number> [feature]` |
| 5d. Task Review | `/mp-review-task` | `<module> <issue-number> [feature]` |
| 5e. Review 修复 | `/mp-review-fix` | `<module> <issue-number> [feature]` |
| 5f. 前端 Feature Review | `/mp-review-feature` | `<module> <feature>` |
| 5f. 后端模块 Review | `/mp-review-module` | `<module>` |
| 5f. 前端模块 Review | `/mp-review-module-frontend` | `<module>` |
| 5g. L2 集成测试 | `/mp-test-integration` | `<issue-number>` |
| 5g. L2 集成测试 Review | `/mp-review-integration` | `<issue-number>` |
| 6. E2E 测试 | `/mp-test-e2e` | — |
| 6. E2E Review | `/mp-review-e2e` | — |
| 7. 验收预检 | `/mp-review-acceptance` | — |

执行类 skill 以 `context: fork` 运行，无需手动开新会话。流程管控 skill（`mp-workflow`、`mp-workflow-update`）在主会话运行。

> **状态更新职责分离**：执行类 skill 完成后自动将状态推进到"等待 review"；Review 类 skill 只输出结论，不修改状态。技术负责人 review 后通过 `/mp-workflow-update` 推进状态闸门。

---

## 文档管理

### 文档清单

| 文档 | 谁写 | 谁 Review | 是否必须 |
|------|------|-----------|---------|
| PRD (prd.md) | 产品经理 | Reviewer agent + 技术负责人 | 必须 |
| CLAUDE.md | 技术负责人 + Architect agent | 技术负责人 | 必须 |
| README.md | 技术负责人 | 无需 review | 推荐 |
| 系统架构 (architecture.md) | Architect agent | Reviewer agent + 技术负责人 | 必须 |
| 模块设计 + 接口契约 (module-design/{module}.md) | Architect agent | Reviewer agent + 技术负责人 | 必须 |
| GitHub Issues | Architect agent + 技术负责人 | Reviewer agent + 技术负责人 | 必须 |
| 契约测试 + 集成测试 + E2E 测试 | Tester agent | Reviewer agent + 技术负责人 | 必须 |
| 单元测试 | Implementer agent | Reviewer agent | 按需 |
| 业务代码 | Implementer agent | Reviewer agent + 技术负责人 | 必须 |

> **CLAUDE.md vs README.md**：CLAUDE.md 面向 AI Agent，包含约定和禁止事项；README.md 面向人类开发者，包含快速上手指南。两者定位不同，不可互相替代。

### 文档分层策略

**全局 CLAUDE.md（< 100 行）** — 所有 agent 自动加载，是 agent 获取项目上下文的主要入口。

**architecture.md** — 系统级内容（模块划分、依赖关系图、部署架构、跨模块数据流、接口通用约定、接口依赖矩阵、需求追溯表）。

**module-design/{module}.md** — 每个模块的内部设计（分层、数据模型）+ 该模块的完整接口契约（五要素）。

**跨模块 agent 的信息边界**：

Module-B 的 agent 关于 Module-A **需要知道的**：公开接口签名和返回类型、错误码定义、相关数据模型。**不需要知道的**：内部实现逻辑、目录结构、单元测试、技术债。这些信息通过 `module-design/{module-a}.md` 中的"接口契约"和"消费的外部接口"部分提供。

### 文档变更传播规则

核心原则：**先更新文档 → 再更新测试 → 最后更新实现。** 按模块依赖顺序处理，被依赖的模块优先。

**接口契约变更**：

1. 查看 architecture.md 的**接口依赖矩阵**，识别所有受影响的消费方模块
2. 更新提供方的 module-design/{module}.md 中的接口定义
3. 更新消费方的 module-design 中的"消费的外部接口"
4. 同步更新 architecture.md 的接口依赖矩阵（如影响范围变化）
5. 在受影响模块的 GitHub Issue 中 comment 变更通知
6. Tester agent 新会话更新契约测试
7. 已完成的实现如涉及变更接口，标记 Issue 为"需更新"

**architecture.md 变更**：

1. 评估是否影响模块划分和依赖关系
2. 更新受影响的 module-design/{module}.md
3. 更新 CLAUDE.md 中的项目结构（如有变化）

**变更记录**：在相关 GitHub Issue 中 comment 变更原因和影响范围。commit message 标注：`docs(<module>): {变更内容}，影响范围: #{issue-list}`

---

## Review 指南

### 分层 Review

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| PRD Review | PRD 就绪后（Step 1 过程中） | Reviewer Agent + 技术负责人 | 需求完整性、验收标准可测性 |
| 架构 Review | 架构设计完成 | Reviewer Agent + 技术负责人 | 模块划分、依赖方向、数据流 |
| 模块设计 Review | 模块设计完成 | Reviewer Agent + 技术负责人 | 分层、数据模型、接口五要素 |
| 脚手架 Review | 脚手架完成 | Reviewer Agent + 技术负责人 | 依赖、lint、桩文件签名 |
| Issues Review | 任务拆分完成 | Reviewer Agent + 技术负责人 | 覆盖度、依赖关系、标签 |
| infra Review | infra 实现完成 | Reviewer Agent + 技术负责人 | 配置、安全、能跑通 |
| 契约测试 Review | 契约测试完成 | Reviewer Agent + 技术负责人 | 业务规则覆盖、错误码全覆盖 |
| Task Review | 每个 Task 完成 | Reviewer Agent + 技术负责人 | 功能正确性、代码规范、测试覆盖 |
| Feature Review | 前端 feature 所有 Task 完成 | Reviewer Agent + 技术负责人 | feature 内一致性、设计文档完整覆盖、交互流程覆盖 |
| 模块 Review | 模块所有 Task 完成（前端：所有 feature 通过 Feature Review 后） | Reviewer Agent + 技术负责人 | 模块内一致性、命名/风格统一、接口覆盖完整性 |
| L2 集成测试 Review | L2 集成测试完成 | Reviewer Agent + 技术负责人 | 关键路径覆盖、真实调用、异常流程 |
| E2E Review | E2E 测试完成 | Reviewer Agent + 技术负责人 | 验收标准覆盖、测试通过 |
| 验收预检 | 验收前 | Reviewer Agent + 产品经理 | 全量测试通过、验收标准全覆盖 |

**协作原则**：每个 review 环节均由 Reviewer Agent 先行检查并输出结论，技术负责人参考 Agent 结论后做最终判断。Agent review 使用与人相同的检查清单，不替代人的判断，而是辅助提升 review 效率和覆盖度。

### Review 输出标准

- **LGTM** — 通过，无需修改
- **MUST FIX** — 必须修复后重新 review
- **SHOULD FIX** — 建议修改，修改后重新 review
- **OPTIONAL** — 可选优化，不阻塞进度

### Review 深度分级

| Task 类型 | Review 深度 | 重点关注 |
|-----------|-----------|---------|
| 基础设施（infra） | 快速扫描 | 配置正确、依赖合理、能跑通 |
| 核心业务模块 | 逐条对照契约 | 业务规则覆盖、错误处理、边界条件 |
| 跨模块交互 | 重点检查 | 依赖方向、接口一致性、数据流转 |
| 模块级 Review | 一致性检查 | 命名风格、错误处理方式、职责分层 |

**可"信任 Agent + 测试"的场景**：简单 CRUD、测试全部通过且 Agent 未报告异常。
**必须人工逐行过的场景**：安全相关、复杂业务规则、跨模块数据一致性。

### Step 1 PRD Review Checklist

```
- [ ] 需求按模块组织，模块划分清晰
- [ ] 每个模块包含明确的验收标准（可测试、可量化）
- [ ] 非功能性需求已说明（性能、安全、可用性等）
- [ ] 功能点无遗漏（模块间交互场景已覆盖）
- [ ] 验收标准具体到可编写 E2E 测试（非模糊描述）
- [ ] 业务规则明确（状态流转、计算规则、权限控制等有具体说明）
- [ ] 用户角色和权限清晰定义
- [ ] 边界条件和异常场景有说明
```

### Step 2 架构 Review Checklist

```
- [ ] 技术选型与 CLAUDE.md Tech Stack 一致
- [ ] 模块划分符合单一职责，每个模块职责一句话说清
- [ ] 模块间依赖方向单向，无循环依赖
- [ ] 业务模块数量在 4-8 个（过多需拆迭代、过少则本流程过重）
- [ ] 目录结构与模块划分匹配（每个模块有对应目录）
- [ ] 关键业务路径的数据流完整
- [ ] infra 职责边界明确
- [ ] 跨模块数据关系清晰（关联管理方、外键策略）
- [ ] 架构决策有理由说明
- [ ] 日志约定完整（级别定义、格式规范、规则说明）
- [ ] 接口通用约定已定义（认证、响应格式、分页、状态码）
- [ ] 部署概要已说明（如影响模块设计）
```

### Step 3 模块设计 + 接口契约 Review Checklist

```
后端模块设计：
- [ ] 内部分层符合 architecture.md 约定
- [ ] 数据模型完整（字段、类型、约束）
- [ ] 公开接口清单与 architecture.md 一致
- [ ] 消费的外部接口在依赖关系中有体现
- [ ] 关键业务逻辑有详细说明（状态机、计算规则等）
- [ ] 没有设计其他模块的内容

后端接口契约（每个模块完成后检查）：
- [ ] 每个接口（含 HTTP 接口和内部 Service 接口）都有完整的五要素（输入、输出、业务规则、错误码、consumers）
- [ ] 接口签名与 module-design 中"公开接口清单"一致
- [ ] 错误码全局不重复（与已有模块不冲突）
- [ ] 接口风格与已有模块一致（遵循通用约定）

前端整体设计：
- [ ] Feature 划分与后端模块对应关系合理
- [ ] 路由结构完整，覆盖 PRD 所有页面
- [ ] 共享层设计合理（共享组件、hooks、stores 职责清晰，无重复）
- [ ] API Client 配置与后端接口通用约定一致（认证、响应格式、错误处理）
- [ ] 布局设计与 PRD 描述一致
- [ ] 核心类型定义与后端接口响应类型匹配
- [ ] 没有设计各 feature 的页面细节（应在 feature 级文档中）

前端 Feature 设计：
- [ ] 每个页面调用的后端接口在对应后端 module-design 中有定义
- [ ] 页面路由与整体设计的路由表一致
- [ ] 组件结构树描述到业务组件粒度
- [ ] 消费的后端接口汇总完整（无遗漏）
- [ ] 交互流程清晰，覆盖正常和异常场景
- [ ] UI 原型已引用（如 PRD 中有）
- [ ] 没有重复定义整体设计中的共享组件和全局状态

所有模块完成后检查：
- [ ] 需求追溯表中列出了 PRD 的每条业务规则和验收标准（无遗漏）
- [ ] 每一行的"对应接口定义"都已填写（不允许为空）
- [ ] 抽查 3-5 条：翻到对应接口定义，确认规则完整描述
- [ ] 接口依赖矩阵完整，覆盖所有跨模块调用
```

### Step 4 脚手架 + Issues Review Checklist

```
脚手架：
- [ ] 依赖安装成功
- [ ] lint 命令能跑通
- [ ] 测试框架能启动
- [ ] docker-compose.yml 已创建，docker compose up -d 能成功启动
- [ ] 后端模块导出桩文件存在且函数签名与 module-design 中的接口契约一致
- [ ] 前端 feature 桩文件存在（api/ 层桩文件 + 页面组件桩文件）
- [ ] .env.example 已创建，.env 已加入 .gitignore
- [ ] TypeScript 配置正确（根目录 + 各端独立 tsconfig）
- [ ] CLAUDE.md 已回填常用命令和测试环境配置（与实际脚手架配置一致）
- [ ] 前端 dev server 能启动（`npm run dev:web`；如有管理后台 `npm run dev:admin`）

GitHub Issues：
- [ ] 每个接口都有对应的契约测试 Issue
- [ ] 每个实现 Issue 标注了依赖（Depends on #N）
- [ ] 每个实现 Issue 标注了需通过的测试
- [ ] 共享层任务优先级最高
- [ ] 关键路径有 L2 集成测试 Issue
- [ ] Issues 按依赖顺序可串行推进
- [ ] 标签（type + module）正确
```

### Step 5 测试 Review Checklist

```
后端契约测试：
- [ ] 每条业务规则有对应测试用例（对照 module-design 接口契约逐条检查）
- [ ] 覆盖正常流程和异常流程（错误码全覆盖）
- [ ] 测试独立（无共享状态、不依赖执行顺序）
- [ ] 测试注释标注了业务规则来源
- [ ] 测试能编译/加载（允许执行失败）

前端契约测试（如涉及）：
- [ ] API 层测试验证请求格式和响应处理
- [ ] 页面渲染测试验证 mock 数据下的正确渲染
- [ ] 用户交互处理已验证
- [ ] 测试独立且注释标注来源
```

---

## GitHub Project 初始化（Step 1）

### 创建 Project

```bash
gh project create --title "{项目名称}" --owner "@me"
gh project list --owner "@me"   # 记录 Project Number
```

### 配置自定义字段

在 GitHub Web UI 中操作（Project → Settings → Custom fields）：

| 字段 | 类型 | 选项 |
|------|------|------|
| Status | 单选 | Todo, In Progress, Review, Done, Blocked |
| Module | 单选 | infra, {module-a}, {module-b}, web-app, admin, ... |
| Priority | 单选 | P0, P1, P2 |

### 创建标签

```bash
# 任务类型标签
gh label create "type:contract-test" --color "1d76db" --description "契约测试任务"
gh label create "type:impl" --color "0e8a16" --description "实现任务"
gh label create "type:integration-test" --color "5319e7" --description "集成测试任务"
gh label create "type:e2e" --color "d93f0b" --description "E2E 测试任务"
gh label create "type:infra" --color "c5def5" --description "基础设施任务"

# 模块标签（为每个模块创建）
gh label create "module:{name}" --color "fbca04" --description "{name} 模块"

# 阶段 Issue 标签
gh label create "type:prd-review" --color "0075ca" --description "PRD Review"
gh label create "type:architecture" --color "bfd4f2" --description "架构设计"
gh label create "type:design" --color "d4c5f9" --description "模块设计"
gh label create "type:scaffold" --color "c2e0c6" --description "脚手架"
gh label create "type:task-split" --color "fef2c0" --description "任务拆分"
gh label create "type:module-review" --color "f9d0c4" --description "模块级 Review"
gh label create "type:feature-review" --color "e6ccb3" --description "Feature 级 Review"
gh label create "type:acceptance" --color "0e8a16" --description "验收"
```

### 创建 Milestones

```bash
gh api repos/{owner}/{repo}/milestones -f title="Milestone 1: 核心模块" -f description="infra + {核心模块列表}"
gh api repos/{owner}/{repo}/milestones -f title="Milestone 2: 业务模块" -f description="{业务模块列表}"
```

### 配置 Project 自动化

在 GitHub Web UI 中操作（Project → Settings → Workflows）：
- 启用 **"Item closed"** → 设置 Status 为 **Done**（`/mp-workflow-update` 关闭 Issue 后自动同步 Board 状态）

### 配置 Project 视图

在 GitHub Web UI 中操作：
- **Board 视图**（默认）：按 Status 分列，用于日常追踪
- **Table 视图**：显示所有字段，按 Module 分组，用于全局概览
- **Roadmap 视图**（可选）：按 Milestone 时间线，用于向产品经理展示

---

## 流转管理

### 技术负责人管理命令

```bash
gh issue list --state open --label "type:impl"              # 查看待处理
gh issue list --state open --label "module:{module-name}"    # 按模块筛选
gh issue list --state open --search "阻塞 in:comments"       # 查看阻塞
gh issue close {NUMBER} --comment "Review 通过，Task 完成。"  # 关闭已完成
```

**状态管理原则**：Agent 通过 Issue comment 报告进展和 Review 结论。`/mp-workflow-update` 在状态推进时自动关闭已完成的 Task Issue 和阶段 Issue（配合 GitHub Project 自动化规则 "Item closed → Status = Done" 同步 Board 状态）。模块进度通过 GitHub Issues 状态推导。

### Task 流转

Reviewer 输出 LGTM 后，Task 即视为完成（代码已在 main 上）。

```
每个 Task Review 通过后：
- [ ] 检查是否解锁了下游依赖任务
- [ ] 如果涉及文档变更，按变更传播规则处理
- [ ] 后端模块：如果模块所有 Task 完成，触发模块级 Review
- [ ] 前端模块：如果 feature 所有 Task 完成，触发 Feature Review

前端 Feature 完成时：
- [ ] 确认该 feature 所有 Task 已完成
- [ ] 触发 Feature Review（`/mp-review-feature`）
- [ ] Feature Review 通过后，切换到下一个 feature 或触发前端模块 Review

模块完成时：
- [ ] 确认该模块所有 Task 已完成（前端模块：所有 feature 已通过 Feature Review）
- [ ] 触发模块级 Review
- [ ] 如有跨模块依赖且被依赖模块已完成，触发 L2 集成测试
- [ ] 跑全量测试确认无回归
```

### infra 变更处理

```
收到 Agent 的 infra 变更请求时：
1. 评估需求，确认后允许修改
2. 修改后确认：
   - [ ] 不影响已有模块
   - [ ] 后续 Task 自动使用最新代码
```

### 数据库迁移策略

- 统一一个 `prisma/schema.prisma` 文件，所有模块的数据模型集中定义
- Step 4 脚手架阶段：根据 module-design 中的数据模型创建初始 schema
- Step 5 实现阶段：模块实现中如需调整数据模型，先更新 module-design 文档，再更新 schema.prisma
- 每次 migration 生成后立即 commit
- 测试环境使用独立数据库，通过 `DATABASE_URL` 环境变量区分

---

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
  前端: web-app（auth feature + product feature）
  → Step 2-7 完整走一遍
  → 实现顺序: infra → user → product → web-app（相关页面）
  → 产品经理验收核心流程

Milestone 2: 交易模块
  后端: order + payment + inventory
  前端: web-app（order feature）+ admin（订单管理页面）
  → Step 2（增量：只设计新模块，review 对已有模块的影响）→ Step 4-7
  → 实现顺序: inventory → order → payment → web-app（新页面）→ admin
  → 产品经理验收交易流程

Milestone 3: 辅助模块
  后端: notification + coupon + analytics
  前端: admin（剩余管理页面）
  → 同上（增量模式）
  → 最终全量验收
```

> **前端模块时序**：每个迭代内，前端模块在其依赖的后端模块全部完成后再实现。前端按 feature 拆分设计文档和测试，每个迭代只设计和实现与本迭代后端模块对应的 feature，不必等所有后端模块完成。

### 迭代间的关系

- 后续迭代的 Step 2 只设计本迭代新增模块，但必须 review 对已有模块的影响
- 已有模块的接口如需变更，按变更传播规则处理
- 每个迭代结束时保持 main 可部署

### 增量开发（已有项目加新功能）

| 场景 | 起始步骤 | 说明 |
|------|---------|------|
| 新增业务模块 | Step 2（评估对现有架构影响） | 更新 architecture.md 依赖图，然后 3 → 4 → ... |
| 已有模块增加接口 | Step 3（更新 module-design/{module}.md） | 同时更新 architecture.md 依赖矩阵 |
| 跨多模块的新功能 | Step 2（影响评估） | 查接口依赖矩阵确定影响范围 → 3 → 5 |
| 模块内重构不改接口 | Step 5（实现阶段） | 契约测试不需要改（接口没变） |
| 修 bug | 不走流程 | 直接改 + 补测试 + 提交 |

关键原则：**变了什么文档，就从那个文档对应的步骤开始往后走。**

---

## 速查与参考

### 每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准 |
|------|--------|------|------|---------|
| 1 | 人 + Reviewer | — | PRD, CLAUDE.md（基础）, GitHub Project | PRD 按模块组织含验收标准；CLAUDE.md 基础部分确认（含 Tech Stack）；Project 已创建 |
| 2 | Architect | PRD, CLAUDE.md | architecture.md | 模块划分清晰；依赖单向无环；数据流完整 |
| 3 | Architect | architecture.md, PRD | module-design/*.md | 每模块内部设计 + 接口契约完整；数据模型清晰 |
| 4 | Architect | 架构 + 模块设计 | 脚手架, Issues | 脚手架能运行；Issues 含依赖关系 |
| 5 | Tester + Impl + Reviewer | module-design + 测试 | 契约测试 + 业务代码 + L1/L2 集成测试 | 按模块串行：契约测试 Issue closed → 实现 Issue closed → 模块 Review Issue closed → L2 Issue closed |
| 6 | Tester + 技术负责人 | PRD 验收标准 | E2E 测试, README.md | 核心路径 E2E 通过；README.md 完成 |
| 7 | 产品经理 | PRD | 验收确认 | 分批验收全部通过 |

### 常见故障与恢复

**Agent 会话崩溃**：检查 `git status` + `git log` → 有可接受的未提交改动则提交后新会话继续 → 质量不确定则 `git stash` 后重新开始 → 无未提交改动则直接重新开始。

**实现过程中发现架构有问题**：Agent 停止并报告 → 技术负责人评估影响 → 按下方「设计回退操作清单」处理。

**Agent 产出质量不达标**：给出具体修改要求 → 反复出现同类问题则在 CLAUDE.md 增加约束 → 仍不达标则拆更小的 Task 或手动完成。

### 设计回退操作清单

当实现过程中发现架构或模块设计需要修改时，按以下清单处理级联影响。

#### 回退到 Step 2（架构调整）

适用场景：模块划分变更、依赖方向调整、新增/删除模块。

```
1. 文档回退
   - [ ] 修订 architecture.md（模块划分、依赖关系图、依赖矩阵）
   - [ ] 识别受影响的 module-design 文件，逐个修订或删除
   - [ ] 更新 CLAUDE.md 中的项目结构和架构约定
   - [ ] 更新 architecture.md 的接口依赖矩阵和需求追溯表

2. GitHub Issues 清理
   - [ ] 关闭已失效的 Issues（comment 说明原因：`设计回退，Issue 作废`）
   - [ ] 保留仍有效的 Issues，在 comment 中标注设计变更影响
   - [ ] 后续 Step 4b 重新拆分任务时创建新 Issues

3. 测试代码清理
   - [ ] 删除或标记已失效模块的契约测试（tests/contracts/{旧模块}/）
   - [ ] 删除或标记已失效模块的集成测试（tests/integration/{旧模块}/）
   - [ ] 保留未受影响模块的测试，确认仍可编译

4. 实现代码处理
   - [ ] 已完成的未受影响模块：保留，跑测试确认无回归
   - [ ] 已完成但受影响的模块：评估是否可增量修改；如不可，git stash 或新分支保留参考后回退
   - [ ] 未完成的受影响模块：直接放弃当前进度

5. 脚手架调整
   - [ ] 更新目录结构（新增/删除模块目录）
   - [ ] 更新导出桩文件
   - [ ] 确认 lint 和测试框架仍可运行

6. workflow-state 重置
   - [ ] `/mp-workflow-update` 将 step 回退到 2，substep 设为 review
   - [ ] 关闭已失效模块的阶段 Issue（type:design 等），comment 说明原因
   - [ ] 新增模块在后续 Step 3/4 时由 Review skill 自动创建新的阶段 Issue
```

#### 回退到 Step 3（接口契约调整）

适用场景：已有模块的接口签名变更、错误码调整、业务规则修改。

```
1. 文档回退
   - [ ] 修订 module-design/{受影响模块}.md 中的接口契约
   - [ ] 查看 architecture.md 接口依赖矩阵，识别所有消费方模块
   - [ ] 更新消费方的 module-design 中"消费的外部接口"
   - [ ] 同步更新 architecture.md 接口依赖矩阵和需求追溯表

2. GitHub Issues 处理
   - [ ] 在受影响的 Issues 中 comment 变更内容和原因
   - [ ] 已完成但受影响的 Task：创建新 Issue 标记"需更新"
   - [ ] 未开始的 Task：更新 Issue 描述以反映新契约

3. 测试代码更新
   - [ ] 更新提供方的契约测试（tests/contracts/{提供方模块}/）
   - [ ] 更新消费方的契约测试（如涉及消费方接口变化）
   - [ ] 更新受影响的 L1 集成测试
   - [ ] 确认所有测试可编译（允许执行失败）

4. 实现代码处理
   - [ ] 提供方已实现：修改实现以匹配新契约，跑测试确认
   - [ ] 消费方已实现：修改调用代码以匹配新接口，跑测试确认
   - [ ] 未实现的模块：无需处理，后续按新契约实现

5. workflow-state 更新
   - [ ] substep 按实际进度调整
   - [ ] 重新打开受影响模块的阶段 Issue（或创建新的），comment 说明变更原因
```

#### 通用原则

- **先文档，再测试，最后实现** — 回退时也遵循此顺序
- **被依赖模块优先处理** — 按模块依赖顺序从上游到下游
- **每步 commit** — 回退过程中每个有意义的改动单独 commit，message 格式：`docs(<scope>): 设计回退 - {变更描述}`
- **不要静默删除** — 关闭 Issue / 删除测试时必须 comment 说明原因

### CI 集成建议

```
每次 push 到 main:
  lint + 全量契约测试 + 单元测试 + L1/L2 集成测试

定期 / 手动触发:
  全量测试 + E2E 测试
```

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
