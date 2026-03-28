# 小项目开发流程规范

## 适用范围

- 3 个以内业务模块
- 1-2 人开发（程序员主导）
- 开发周期 1-4 周
- 单仓库，无需多 agent 并行

## 不适用场景

- 探索性原型（不确定做什么）→ 先做 spike 验证方向，再回来走流程
- 纯 UI 还原（无业务逻辑）→ 不需要架构设计和契约测试
- 修 bug / 小改动 → 直接改，不需要走完整流程
- 超过 3 个模块或需要多人并行 → 使用 medium-project 流程

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

Step 4: 契约测试先行（按模块拆分，每个模块一个会话）
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

- **契约测试**：验证接口的输入输出是否符合 api-contracts.md 的定义，在实现之前编写，是 TDD 的驱动力。本文中的契约测试指基于 api-contracts.md 定义验证接口输入输出的规格测试（Specification Test），非 Pact 风格的消费者驱动契约测试。
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

## 速查：每步的输入输出

| Step | 执行者 | 输入 | 产出 | 质量门禁 |
|------|--------|------|------|---------|
| 1 | 人 | — | PRD, CLAUDE.md | 无 |
| 2 | Architect Agent | PRD | architecture.md, api-contracts.md | 技术负责人 Review |
| 3 | 人 | architecture.md | task-board.md, 项目脚手架 | 无 |
| 4 | Tester Agent | api-contracts.md, architecture.md | 契约测试代码 | 技术负责人 Review |
| 5 | Implementer + Reviewer Agent | 文档 + 测试 | 业务代码（逐 Task） | 测试通过 + LGTM |
| 6 | Tester Agent | PRD 验收标准 | E2E 测试 | 测试通过 |
| 7 | 产品经理 | PRD | 验收确认 | 全部通过 |
