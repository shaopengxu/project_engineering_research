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
└── 技术负责人: 填写 CLAUDE.md 的项目名称和一句话描述

Step 2: 系统架构设计
├── [Architect agent]: /mp-architecture → 产出 architecture.md + 补充 CLAUDE.md
└── 技术负责人: review
    ├── 通过 → 进入 Step 3
    └── 不通过 → 修订

Step 3: 模块详细设计 + 接口契约（每个模块使用 /mp-module-design）
├── 后端模块（按依赖顺序串行）：逐模块 /mp-module-design {module}
├── 前端模块（后端模块全部完成后）：
│   ├── /mp-module-design web-app → 整体设计
│   ├── 逐 feature /mp-module-design web-app {feature} → feature 级设计
│   └── admin 同上（页面少时可不拆 feature）
├── 所有模块完成后：/mp-module-design --summary → 补充 architecture.md 汇总部分
└── 技术负责人: review 所有模块设计
    ├── 通过 → 进入 Step 4
    └── 不通过 → 对应模块修订

Step 4: 环境初始化 + 任务拆分
├── [Architect agent]: /mp-scaffold → 初始化脚手架 + 回填 CLAUDE.md
├── 技术负责人: review 脚手架
├── [Architect agent]: /mp-task-split → 拆分任务 + 创建 GitHub Issues
└── 技术负责人: review Issues
    ├── 通过 → 进入 Step 5
    └── 不通过 → 修订

Step 5: 契约测试 + 实现 + Review（按模块串行推进）
├── 5a. /mp-impl-infra → infra 实现（一次性），技术负责人 review 后继续
│
└── 循环 [按依赖顺序逐模块执行]：被依赖的后端模块 → 依赖方后端模块 → 前端模块
    │
    ├── 5b. 测试先行（按模块类型二选一）：
    │   ├── 后端模块 → /mp-test-contract
    │   └── 前端模块 → 按 feature 逐个 /mp-test-frontend
    │   技术负责人: review 测试代码
    │
    ├── 循环 [按 Task 依赖顺序逐 Task 执行]:
    │   ├── 5c. /mp-impl → 实现当前 Task
    │   ├── 5d. /mp-review-task → Task Review
    │   │   ├── LGTM → 进入下一个 Task
    │   │   ├── MUST FIX / SHOULD FIX → 5e. /mp-review-fix → 修复后重新 Review
    │   │   └── 涉及接口变更 → 停止，按变更传播规则处理
    │   └── 技术负责人: 更新 Issue 状态
    │
    ├── 5f. /mp-review-module → 模块级 Review
    ├── 5g. /mp-test-integration → L2 关键路径集成测试（当被依赖模块已完成时）
    └── 技术负责人: 确认当前模块完成，推进下一个模块

Step 6: E2E 测试
├── /mp-test-e2e → 根据 PRD 验收标准编写 E2E 测试
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

## 相关文档

| 文档 | 内容 |
|------|------|
| [tech-lead-guide.md](tech-lead-guide.md) | 技术负责人操作指南（Skill 速查、GitHub Project 初始化、文档管理、Review、流转、迭代、速查参考） |
| [templates/](templates/) | CLAUDE.md 模板 |
