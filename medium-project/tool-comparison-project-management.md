# 中型项目管理工具调研与对比

> 调研日期：2026-03-30
> 上下文：从小型项目的纯 Markdown task-board（git 内管理）升级到中型项目（3-8 业务模块，2-5 开发者，含 AI agent 工作流）

---

## 一、调研背景与核心需求

### 当前小型项目方案

- 纯 Markdown `task-board.md` 存放在 git 仓库中
- 技术负责人独占更新，agent 通过 status-reports 异步汇报
- 任务依赖通过文本描述（"依赖: Impl-001"）
- 无可视化、无 API 访问、无自动化

### 中型项目的新需求

根据已有分析（`brainstorm-summary.md`、`parallel-development-analysis.md`），中型项目面临：

1. **20-40 个 Task** 的管理，纯 Markdown 的可读性和维护性下降（崩溃点 #7）
2. **2-5 个 agent 并行**，需要实时状态追踪，task-board 成为并发瓶颈
3. **任务依赖是 DAG（有向无环图）**，需要可视化关键路径
4. **AI agent 需要程序化读写任务状态**，必须有 API/CLI
5. **迭代管理**，需要按 Phase/Sprint 组织任务

### 评估维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 轻量性 | 高 | 不要企业级工具的复杂性 |
| API/CLI 可用性 | 高 | AI agent 必须能程序化操作 |
| 任务依赖与可视化 | 高 | DAG 依赖、关键路径、Gantt |
| Git/GitHub 集成 | 高 | 与代码工作流无缝衔接 |
| 并行工作流支持 | 中 | 多人/多 agent 同时操作 |
| 免费/低成本 | 中 | 小团队可负担 |
| 自托管选项 | 低 | 数据主权，可选 |
| 学习曲线 | 中 | 团队快速上手 |

---

## 二、工具分类与详细评估

### 类别 A：GitHub 原生方案

#### A1. GitHub Projects v2 + GitHub Issues

**概述**：GitHub 内置的项目管理功能，2025 年 1 月进入公开预览的新版本，新增了 sub-issues（子任务）、任务层级等功能。

**关键特性**：
- Sub-issues：支持父子任务层级，可将 checklist 项直接转为子 issue
- 多视图：Board（看板）、Table（表格）、Roadmap（时间线）
- 自定义字段：状态、优先级、迭代、数字、日期等
- 自动化：通过 GitHub Actions 实现工作流自动化（issue 创建时自动加入 Project、PR 合并时自动更新状态等）
- 标签和里程碑：原生支持

**API/CLI**：
- GraphQL API 完整支持 Projects v2 的增删改查
- `gh` CLI 工具可直接操作（`gh project`、`gh issue` 命令族）
- 第三方 CLI 扩展：`gh-pm` 提供更便捷的项目管理命令
- GitHub Actions 可实现复杂自动化流水线

**定价**：
- **Free**：完全免费，公开和私有仓库均可使用 Projects
- **Team**：$4/用户/月，增加高级权限控制
- GitHub Actions：Free 计划 2000 分钟/月（私有仓库）

**任务依赖处理**：
- Sub-issues 提供了任务层级（父子关系）
- 无原生的 blocking/blocked-by 依赖关系
- 无内置 Gantt 图（需第三方工具如 Ganttify）
- 可通过标签或自定义字段模拟依赖关系
- 第三方工具（Ganttify、GanttLab）可从 Issues 生成 Gantt 图

**AI agent 工作流适配**：
- 优势：`gh` CLI 是最成熟的 CLI 工具之一，所有 AI coding agent 都原生支持
- 优势：GraphQL API 灵活精确，适合自动化脚本
- 优势：与 PR、代码审查、CI/CD 天然一体化
- 劣势：依赖管理薄弱，agent 无法自动判断"哪些任务现在可以开始"
- 劣势：没有 sprint/cycle 的内建概念（需用 Milestone 或自定义字段模拟）

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 5 | 已内置，零额外工具 |
| API/CLI | 5 | `gh` CLI + GraphQL API，最成熟 |
| 任务依赖 | 2 | 无原生依赖，需第三方补充 |
| Git 集成 | 5 | 天然一体 |
| 并行支持 | 4 | 多人可同时操作，无文件冲突 |
| 成本 | 5 | 免费 |

---

### 类别 B：轻量级 SaaS 工具

#### B1. Linear

**概述**：面向产品开发团队的高速项目管理工具，以极快的 UI 响应速度和键盘驱动操作著称。2026 年 3 月发布了 Linear Agent（AI 原生功能）。

**关键特性**：
- Issues + Projects + Cycles（时间盒迭代）
- Issue Relations：支持 blocking、blocked-by、related、duplicate 关系
- Cycles：自动结转未完成任务到下一周期
- Roadmap：项目级时间线视图
- 2026 新功能：Linear Agent（AI 原生），可创建可复用 Skill，Code Intelligence 可感知代码库
- 100+ 集成：GitHub、Figma、Slack、Sentry 等
- AI 功能：自动分类 Bug、建议 Sprint 计划、生成发布说明

**API/CLI**：
- GraphQL API 完整覆盖所有操作
- Webhook 支持实时事件推送
- MCP Server：AI agent（Claude、ChatGPT、Cursor）可通过 MCP 或 API 直接操作
- 与 Cursor IDE 的深度集成：可在 IDE 中直接操作 Linear issue
- Linear Agent 支持自然语言交互

**定价**：
- **Free**：$0，最多 250 个活跃 issue，所有集成 + API + Webhook
- **Basic**：$8/用户/月（年付），功能齐全
- **Business**：$14/用户/月（年付），含 Agent Automations + Code Intelligence
- 5 人团队年费：$480-$840/年

**任务依赖处理**：
- 原生支持 blocking/blocked-by 关系
- 可过滤被阻塞的任务
- Project 级别的依赖关系和时间线可视化
- 局限：无高级调度（关键路径法）、无跨项目依赖的自动冲突检测、无 Gantt 基线

**AI agent 工作流适配**：
- 优势：MCP Server 是 AI agent 集成的黄金标准，Claude Code 等工具可直接操作
- 优势：Linear Agent 本身就是 AI-first 设计
- 优势：API 设计简洁一致，自动化脚本易写
- 优势：实时 Webhook 支持 agent 状态报告的即时推送
- 劣势：Free 计划 250 issue 上限，中型项目可能不够（40 个 Task + 历史 issue）
- 劣势：非开源，数据在 Linear 云端
- 劣势：Gantt/关键路径能力有限

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 5 | 极简设计，上手快 |
| API/CLI | 5 | GraphQL + MCP + Webhook，AI-first |
| 任务依赖 | 3 | 有 blocking 关系，但无关键路径分析 |
| Git 集成 | 4 | GitHub 集成好，但非原生 |
| 并行支持 | 5 | 多人并行无冲突，实时同步 |
| 成本 | 3 | Free 有限制，Basic 年费约 $480 |

#### B2. Shortcut

**概述**：面向工程团队的项目管理平台，支持完整的规划-构建-发布周期。

**关键特性**：
- Stories（任务）+ Epics + Objectives + Iterations
- Kanban 看板 + 拖拽排列
- 累积流量图、燃尽图
- GitHub/GitLab/Slack 集成

**API/CLI**：
- REST API 完整覆盖，"API 能做任何 UI 能做的事"
- Webhook 支持
- 试用用户即可完整使用 API

**定价**：
- **Free**：有免费版
- **Team**：$10/用户/月
- **Business**：$16/用户/月
- 50 人以下创业公司可获 12 个月免费

**任务依赖处理**：
- Stories 之间可设置 blocking 关系
- Epics 提供高层级组织
- 无 Gantt 图原生支持

**AI agent 工作流适配**：
- 优势：API 完整且文档清晰
- 优势：对创业公司有优惠
- 劣势：MCP/AI-native 集成不如 Linear 深入
- 劣势：比 Linear 稍重

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 4 | 比 Jira 轻，但比 Linear 略重 |
| API/CLI | 4 | REST API 完整 |
| 任务依赖 | 3 | 基本 blocking 支持 |
| Git 集成 | 4 | GitHub/GitLab 集成 |
| 并行支持 | 4 | 多人协作无问题 |
| 成本 | 3 | Team 计划 $10/用户/月 |

#### B3. Zenhub

**概述**：直接内嵌在 GitHub 中的项目管理层，不离开 GitHub 即可获得 Kanban、Sprint、报表等功能。

**关键特性**：
- 直接在 GitHub 界面中使用（浏览器扩展 + Web App）
- Kanban + Scrum 看板
- Epics、Sprint、燃尽图、速度图
- 多仓库统一管理
- AI 功能：AI 生成 Issue、自动 Sprint 规划

**API/CLI**：
- REST API 可用
- 与 GitHub API 互补

**定价**：
- 起步价 $12.50/用户/月
- 无免费计划

**任务依赖处理**：
- Issue 之间可设置依赖
- 通过 Epics 组织大型特性

**AI agent 工作流适配**：
- 优势：与 GitHub 深度一体，数据不离开 GitHub
- 劣势：无免费计划，定价较高
- 劣势：AI/MCP 集成不如 Linear

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 4 | GitHub 内使用，但需额外账号 |
| API/CLI | 3 | API 可用但不如 gh CLI 原生 |
| 任务依赖 | 3 | 基本依赖支持 |
| Git 集成 | 5 | 直接嵌入 GitHub |
| 并行支持 | 4 | 多人无冲突 |
| 成本 | 2 | 无免费计划，$12.50/用户/月 |

---

### 类别 C：开源自托管方案

#### C1. Plane

**概述**：开源的 Jira/Linear 替代品，2026 年发展迅速。提供 Community Edition（完全免费）和 Pro 计划。定位为"AI-native project management"。

**关键特性**：
- Work Items（自定义类型：Bug、Feature、Story 等）
- 5 种视图：List、Board、Calendar、Gantt、Spreadsheet（全部免费）
- Cycles（Sprint）+ Modules（Epic 级别容器）+ Milestones + Initiatives
- Workspace Wiki：富文本编辑器，支持嵌套页面、版本历史
- Intake：需求收集和分类
- 燃尽图、任务自动结转

**API/CLI**：
- REST API 完整覆盖
- Webhook 实时事件推送
- MCP Server：原生支持 AI agent 集成
- **plane CLI**：专为人类和 AI agent 设计的命令行工具，输出结构化 XML/JSON，支持 projects/issues/cycles/modules/pages/comments 等全部操作
- OAuth Apps 支持
- 可自托管 + 自带 LLM key（支持 OpenAI/Anthropic/本地 LLM）

**定价**：
- **Community Edition**：完全免费，无用户上限，AGPL v3.0 开源
  - 含：无限 Projects、Work Items、Cycles、Modules、Pages、5 种视图、Intake、Dashboard、API、Webhook
- **Pro**：$6/seat/月（云端或自托管同价）
  - 额外含：Workspace Wiki、时间追踪、自定义 Work Item 类型、Epics、Initiatives、SAML SSO
- **Enterprise**：定制价格

**任务依赖处理**：
- Gantt 视图原生支持（所有计划，含免费）
- 通过 Modules 组织跨 Cycle 的大型特性
- Work Items 之间可设置关系
- Gantt 图可视化时间线和依赖

**AI agent 工作流适配**：
- 优势：plane CLI 专为 AI agent 设计，结构化输出（XML/JSON），零额外解析成本
- 优势：MCP Server 原生支持
- 优势：自托管 = 完全控制数据 + 可用本地 LLM
- 优势：Community Edition 免费且功能强大（含 Gantt）
- 优势：路线图显示 "Plane Compose" 即将推出（YAML/Git 定义 projects-as-code）
- 劣势：自托管需要维护基础设施
- 劣势：相比 Linear 的 AI 功能成熟度，Plane 的 AI 仍在快速迭代中
- 劣势：社区规模较小（GitHub 38k+ stars，但比 Linear 的商业支持团队小）

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 4 | 功能丰富但不臃肿，自托管稍有运维成本 |
| API/CLI | 5 | REST API + plane CLI + MCP + Webhook |
| 任务依赖 | 4 | Gantt 视图 + 模块组织，免费计划即含 |
| Git 集成 | 3 | GitHub 集成可用，但不如 GitHub 原生或 Linear 深入 |
| 并行支持 | 4 | 多人并行无冲突 |
| 成本 | 5 | Community Edition 完全免费 |

#### C2. Huly

**概述**：All-in-One 开源平台，替代 Linear + Notion + Slack。活跃开发中（2026 年 3 月最新版 v0.7.382，GitHub 25.1k stars）。

**关键特性**：
- 项目管理：快速 Kanban 式 issue tracker
- 实时文档协作（类 Notion）
- 内建即时通讯（类 Slack）
- 日历 + 收件箱
- GitHub 同步

**定价**：
- 按存储和带宽收费，不按用户席位
- 自托管免费，但基础设施较重（MongoDB + Elasticsearch + 对象存储）

**任务依赖处理**：
- 基本的 issue 关系
- 无 Gantt 图原生支持

**AI agent 工作流适配**：
- 优势：不按席位收费，多 agent 无额外成本
- 劣势：自托管部署复杂，运维成本高
- 劣势：API/CLI 工具链不如 Plane 和 Linear 成熟
- 劣势：AI 集成不是核心方向

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 2 | 功能全但部署重 |
| API/CLI | 3 | API 可用但不够成熟 |
| 任务依赖 | 2 | 基本关系，无 Gantt |
| Git 集成 | 3 | GitHub 同步 |
| 并行支持 | 4 | 实时协作 |
| 成本 | 4 | 不按席位收费 |

---

### 类别 D：Markdown 增强方案（In-Repo）

#### D1. Backlog.md

**概述**：将 git 仓库中的 Markdown 文件作为任务管理的 single source of truth。专为 AI 驱动的 spec-driven 开发设计。零配置 CLI + Web 界面。

**关键特性**：
- 所有任务、文档、决策存为 Markdown + YAML metadata 文件
- 每次变更都是 Git commit
- 终端 Kanban 可视化
- Web 界面（现代化看板）
- 支持搜索、导出
- 100% 离线运行

**安装**：`bun add -g backlog.md` 或 `npm` 或 `brew`

**文件结构**：
```
backlog/
├── tasks/
│   ├── task-001.md    # YAML frontmatter + Markdown body
│   ├── task-002.md
│   └── ...
├── docs/
└── decisions/
```

**API/CLI**：
- CLI 工具：创建/更新/列表/移动任务
- 无 HTTP API（文件即数据库）
- AI agent 可直接读写 Markdown 文件（零 API 成本）

**定价**：完全免费，开源

**任务依赖处理**：
- YAML frontmatter 可定义依赖字段
- 无原生依赖可视化
- 无 Gantt 图

**AI agent 工作流适配**：
- 优势：AI agent 原生理解 Markdown，无需任何 API 集成
- 优势：与 Claude Code、Gemini CLI 等工具兼容
- 优势：Git 原生，版本历史完整
- 优势：零配置、零成本、零运维
- 劣势：多 agent 并行时仍存在 Git 文件冲突问题（与当前 task-board.md 相同的根本问题）
- 劣势：无实时协作，依赖 Git push/pull 同步
- 劣势：无服务端状态，无 Webhook
- 劣势：可视化有限，无 Gantt

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 5 | 极简，文件即一切 |
| API/CLI | 3 | CLI 可用，但无 HTTP API |
| 任务依赖 | 2 | 可手动定义，无可视化 |
| Git 集成 | 5 | Git 原生 |
| 并行支持 | 2 | 文件冲突问题未解决 |
| 成本 | 5 | 免费 |

#### D2. taskmd

**概述**：为 AI 编程 agent 时代设计的本地优先 Markdown 任务系统。

**关键特性**：
- YAML frontmatter + Markdown body 格式
- 元数据：id、title、status、priority、effort、type、dependencies、tags
- 本地优先，无服务器
- 便携性：跨项目可复用
- 停止使用后文件仍可读

**文件格式示例**：
```markdown
---
id: TASK-001
title: 实现用户认证模块
status: in-progress
priority: high
effort: medium
type: feature
dependencies: [TASK-000]
tags: [auth, module-user]
---
## 目标
实现 JWT 认证...

## 验收标准
- [ ] 登录接口通过契约测试
- [ ] Token 刷新逻辑正确
```

**API/CLI**：
- CLI 工具管理任务
- 无 HTTP API
- AI agent 直接读写文件

**定价**：免费，开源

**任务依赖处理**：
- `dependencies` 字段原生支持
- 无可视化

**AI agent 工作流适配**：
- 优势：为 AI agent 专门设计，格式标准化
- 优势：`dependencies` 字段可被脚本解析，生成 DAG
- 劣势：同 Backlog.md 的并行冲突问题
- 劣势：无可视化、无 Webhook

**评分**：

| 维度 | 评分 (1-5) | 说明 |
|------|-----------|------|
| 轻量性 | 5 | 极简 |
| API/CLI | 3 | CLI 可用 |
| 任务依赖 | 3 | 元数据支持依赖，可脚本解析 |
| Git 集成 | 5 | Git 原生 |
| 并行支持 | 2 | 文件冲突未解决 |
| 成本 | 5 | 免费 |

#### D3. MDTM（Markdown-Driven Task Management）

**概述**：Roo Commander / IntelliManage 使用的文件式任务管理系统，TOML frontmatter + Markdown。

**特点**：
- TOML 元数据（ID、标题、状态、类型、优先级、指派、链接）
- 文件即 single source of truth
- 与开发工作流无缝集成

**适用性**：与 taskmd 类似，优劣势基本一致。TOML vs YAML 是格式偏好问题。

---

### 类别 E：增强型混合方案

#### E1. GitHub Projects + 脚本层（推荐混合方案）

这不是一个现成工具，而是一个架构思路：以 GitHub Issues/Projects 为核心，通过自定义脚本层补足依赖管理和 AI agent 集成。

**架构**：
```
GitHub Issues    ← 任务数据的 source of truth
GitHub Projects  ← 看板视图、状态追踪
gh CLI / API     ← AI agent 的读写接口
自定义脚本       ← 依赖解析、关键路径分析、调度建议
仓库内 YAML      ← 依赖关系定义（补充 GitHub 不足）
```

**优势**：零额外成本、完整 CLI/API、与代码天然一体
**劣势**：需要投入开发脚本层的工作量

#### E2. Plane Community Edition + In-Repo Markdown

另一个混合思路：Plane CE 管理任务状态和可视化，仓库内 Markdown 保持文档性质的内容。

**架构**：
```
Plane CE (自托管)  ← 任务管理、Gantt、Cycles、看板
plane CLI          ← AI agent 操作 Plane
仓库内 Markdown    ← 架构文档、接口契约、CLAUDE.md（不变）
```

---

## 三、综合对比矩阵

| 工具 | 轻量性 | API/CLI | 任务依赖 | Git 集成 | 并行 | 成本 | AI 适配 | 总分 |
|------|--------|---------|---------|---------|------|------|---------|------|
| GitHub Projects | 5 | 5 | 2 | 5 | 4 | 5 | 4 | 30 |
| Linear | 5 | 5 | 3 | 4 | 5 | 3 | 5 | 30 |
| Shortcut | 4 | 4 | 3 | 4 | 4 | 3 | 3 | 25 |
| Zenhub | 4 | 3 | 3 | 5 | 4 | 2 | 3 | 24 |
| **Plane CE** | **4** | **5** | **4** | **3** | **4** | **5** | **5** | **30** |
| Huly | 2 | 3 | 2 | 3 | 4 | 4 | 2 | 20 |
| Backlog.md | 5 | 3 | 2 | 5 | 2 | 5 | 4 | 26 |
| taskmd | 5 | 3 | 3 | 5 | 2 | 5 | 4 | 27 |

---

## 四、方案推荐

### 推荐方案一（首选）：GitHub Projects + 轻量脚本层

**适用场景**：不想引入额外工具，最大化利用已有 GitHub 基础设施。

**理由**：
1. **零额外成本**，Free 计划完全够用
2. **`gh` CLI 是 AI agent 最成熟的接口**——所有主流 AI coding agent 已原生支持
3. **与 PR/代码审查/CI 天然一体**，不需要在两个系统间同步状态
4. **并发安全**——多 agent 同时创建/更新 issue 不会冲突（vs Markdown 文件冲突）
5. **Sub-issues 已可用**——支持任务层级拆分

**需要补足的**：
- 写一个简单脚本解析 issue 标签/自定义字段中的依赖关系，生成 DAG 和关键路径
- 用 GitHub Actions 自动化状态流转（如 PR 合并 → issue 自动关闭）
- 约定标签体系：`phase/1`、`module/user`、`blocked`、`blocking:ISSUE-NUM`

**迁移成本**：低。当前 task-board.md 中的任务直接转为 GitHub Issues。

**实施要点**：

```
# agent 创建任务
gh issue create --title "Impl-001: 实现用户认证" \
  --label "module/user,phase/2,priority/high" \
  --body "依赖: #1 (shared-core)\n需通过测试: Test-001, Test-002"

# agent 查询可执行任务（未被阻塞的）
gh issue list --label "phase/2" --state open --json number,title,labels

# agent 更新任务状态
gh issue edit 5 --add-label "status/in-progress"
gh issue comment 5 --body "开始实现，当前分支: feature/module-user"

# agent 完成任务
gh issue comment 5 --body "实现完成，所有契约测试通过。等待 Review。"
gh issue edit 5 --remove-label "status/in-progress" --add-label "status/review"
```

### 推荐方案二（备选）：Plane Community Edition

**适用场景**：需要开箱即用的 Gantt 图和依赖可视化，愿意承担自托管运维。

**理由**：
1. **免费且功能最全**——Gantt、Cycles、Modules、5 种视图全部免费
2. **plane CLI 专为 AI agent 设计**——结构化输出，零解析成本
3. **MCP Server 原生支持**——Claude Code 可直接操作
4. **自托管 = 数据主权**——适合对数据敏感的团队
5. **路线图中的 Plane Compose**（YAML/Git 定义项目）如果落地，将是最理想的 projects-as-code 方案

**需要注意的**：
- 自托管需要一台服务器（Docker 一键部署，但仍需维护）
- GitHub 集成不如方案一原生
- 两个系统间的数据同步需要设计

**迁移成本**：中。需要部署 Plane，迁移任务数据，团队学习新工具。

### 推荐方案三（最小变更）：增强版 Markdown（taskmd 风格）

**适用场景**：团队极度偏好 in-repo 管理，不想引入任何外部工具，且并行 agent 数量 <= 2。

**理由**：
1. **与当前方案一脉相承**——从单文件 task-board.md 升级为多文件 taskmd 格式
2. **零基础设施**——不需要任何服务
3. **AI agent 天然兼容**——直接读写文件

**局限**：
- 并行冲突问题未根本解决（多 agent 同时修改任务文件仍需协调）
- 无可视化（需要额外写脚本生成 DAG/Gantt）
- 无实时状态推送
- 随任务数量增长（40+），文件管理复杂度上升

**何时应该升级到方案一或二**：
- 并行 agent > 2 个
- 任务总数 > 30
- 需要 Gantt 或关键路径可视化
- 技术负责人 > 30% 时间用于手动同步状态

---

## 五、与中型项目流程的整合建议

无论选择哪个方案，以下原则不变：

### 5.1 task-board.md 的角色演变

| 方案 | task-board.md 的角色 |
|------|-------------------|
| GitHub Projects | 废弃 task-board.md，GitHub Issues 成为 source of truth |
| Plane CE | 废弃 task-board.md，Plane 成为 source of truth |
| 增强 Markdown | task-board.md 拆分为多个 task 文件（taskmd 格式） |

### 5.2 Agent 状态报告机制

| 方案 | agent 如何报告状态 |
|------|------------------|
| GitHub Projects | `gh issue comment` + `gh issue edit`（直接更新 issue） |
| Plane CE | `plane issue update`（通过 CLI 更新） |
| 增强 Markdown | 仍使用 status-reports/ 目录，技术负责人汇总 |

### 5.3 任务依赖与调度

| 方案 | 依赖管理方式 |
|------|------------|
| GitHub Projects | Issue body 或自定义字段记录依赖 + 脚本解析 DAG |
| Plane CE | Gantt 视图 + Module 组织 |
| 增强 Markdown | YAML frontmatter 的 dependencies 字段 + 脚本解析 |

### 5.4 与 brainstorm-summary.md 中 P0 项的关系

| P0 项 | GitHub Projects | Plane CE | 增强 Markdown |
|-------|----------------|---------|--------------|
| 架构设计分层 | 不影响，文档仍在 repo 内 | 不影响 | 不影响 |
| CLAUDE.md 分层 | 不影响 | 不影响 | 不影响 |
| 并行 Task 编排 | Issue labels/projects 管理 Phase | Cycles + Modules | YAML frontmatter |

---

## 六、决策建议

### 如果只选一个

**选 GitHub Projects**。理由：

1. 你的项目已经在 GitHub 上，零迁移成本
2. AI agent（Claude Code）对 `gh` CLI 的支持最成熟，无需额外集成
3. 解决了 task-board.md 的核心痛点（并发瓶颈、实时性、API 访问）
4. 免费
5. 任务依赖的不足可通过约 100-200 行脚本补足

### 如果追求功能完整

**选 Plane CE**。理由：

1. Gantt + Cycles + Modules 开箱即用
2. 免费且功能最全
3. AI agent 的 CLI/MCP 支持一流
4. 项目增长后可无缝升级到 Pro

### 如果追求最小改动

**留在 Markdown，但升级格式**。采用 taskmd 的 YAML frontmatter 规范，配合脚本辅助。但要有心理准备：当并行 agent 超过 2 个或任务超过 30 个时，需要迁移到方案一或二。

---

## 七、Sources

- [Linear Official Site](https://linear.app/)
- [Linear Pricing & Plans](https://linear.app/docs/billing-and-plans)
- [Linear Issue Relations](https://linear.app/docs/issue-relations)
- [Linear Project Dependencies](https://linear.app/docs/project-dependencies)
- [Linear Agent Announcement](https://linear.app/changelog/2026-03-24-introducing-linear-agent)
- [Linear Agent API Article](https://thenewstack.io/why-linear-built-an-api-for-agents/)
- [GitHub Projects API Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
- [GitHub Issues Features](https://github.com/features/issues)
- [GitHub Issues Evolution (2025)](https://www.infoq.com/news/2025/02/github-issues/)
- [GitHub Pricing](https://github.com/pricing)
- [gh-pm CLI Extension](https://github.com/yahsan2/gh-pm)
- [Plane Official Site](https://plane.so/)
- [Plane Developer Docs & API](https://developers.plane.so/)
- [Plane Open Source](https://plane.so/open-source)
- [Plane Editions](https://developers.plane.so/self-hosting/editions-and-versions)
- [Plane CLI](https://lobehub.com/skills/aaronshaf-plane-cli)
- [Plane GitHub Repo](https://github.com/makeplane/plane)
- [Shortcut Pricing](https://www.shortcut.com/pricing)
- [Zenhub Official Site](https://www.zenhub.com/)
- [Zenhub Pricing](https://www.zenhub.com/pricing)
- [Huly GitHub Repo](https://github.com/hcengineering/platform)
- [Huly Official Site](https://huly.io/)
- [Backlog.md GitHub Repo](https://github.com/MrLesk/Backlog.md)
- [taskmd Article](https://medium.com/@driangle/taskmd-task-management-for-the-ai-era-92d8b476e24e)
- [MDTM Explained](https://github.com/jezweb/roo-commander/wiki/02_Core_Concepts-03_MDTM_Explained)
- [Ganttify for GitHub](https://gantt-chart.com/github)
