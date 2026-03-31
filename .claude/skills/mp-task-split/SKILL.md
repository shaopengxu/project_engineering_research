---
context: fork
name: mp-task-split
description: "Medium-project Step 4b: 拆分任务并创建 GitHub Issues"
---

你是一个软件架构师。请根据架构文档和模块设计拆分任务，并创建 GitHub Issues。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：模块划分、依赖关系、关键业务路径）
- docs/module-design/（所有模块设计文件，了解接口数量和复杂度）

请完成以下工作：

1. **创建 GitHub Issues**：
   - 契约测试任务：每个模块的接口契约对应契约测试 Issue
   - 实现任务：按模块拆分，每个 Issue 标注依赖（Depends on #N）和需通过的测试
   - 集成测试任务：为 architecture.md 中的每条关键路径创建 L2 集成测试 Issue
   - 使用标签：type:contract-test / type:impl / type:integration-test / type:e2e / type:infra + module:{name}
   - 使用 Milestone 标注迭代（如需多迭代）
   - Issue body 格式参考 [task-management.md](../../../medium-project/task-management.md) 中的 Issue 模板

2. **组织 Sub-issues 层级**：
   - 每个模块创建一个父 Issue（模块粒度）
   - Task 作为子 Issue 挂在父 Issue 下

任务拆分原则：
- infra 独立为最高优先级 Task
- 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
- 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
- Task 间依赖关系标注为 DAG（在 Issue body 中声明 Depends on）
- 每个 Task 标注需通过的测试
- 如果拆不到粒度，停下来说明问题

模块内 Task 拆分策略：
- 按层拆分（CRUD 密集型）: repository → service → controller
- 按功能拆分（功能丰富型）: 注册登录 → 个人资料 → 权限管理
- 拆不到粒度 → 说明模块划分需要回退到 Step 2 调整

要求：
- 不要写业务代码和测试代码
- Issues 创建完成后在 commit message 中记录
