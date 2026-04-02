---
context: fork
name: mp-impl
description: "实现业务代码 Task（后端或前端）"
argument-hint: "<module-name> <issue-number> [feature-name]"
---

你是一个开发工程师。请完成指定 Task。

参数：$ARGUMENTS（格式：模块名 Issue编号 [前端feature名]）

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（本模块的设计 + 接口契约）
- 前端 Task 还需读：docs/module-design/{module}-{feature}.md（本 feature 的页面细节）

然后阅读对应的 GitHub Issue 了解任务描述和验收标准：
- 运行 `gh issue view {issue-number}` 查看 Issue 详情

要求：
- 让相关契约测试全部通过
- 编写 L1 集成测试：
  - 后端模块：放在 tests/integration/{module}/ 下，controller → service → repository 真实串联，Mock 其他模块，数据库使用真实连接或测试容器
  - 前端模块：放在 tests/integration/{module}/{feature}/ 下，页面 → hooks → API 层真实串联，仅在网络层使用 MSW mock 后端 API（不 mock hooks）
  > **与契约测试的区别**：`/mp-test-frontend` 编写的契约测试验证"API 请求格式是否正确"和"页面能否渲染给定数据"（mock hooks）；本阶段的 L1 集成测试验证"页面操作 → hook 调用 → API 请求 → 状态更新 → 页面响应"的完整端内数据流（只 mock 网络层）。两者不重复。
- 遵守 CLAUDE.md 中的规范
- 不要修改契约测试代码。如果发现不一致，在 Issue comment 中指出具体矛盾，等待确认
- 不要实现当前 Task 以外的功能
- 不要修改其他模块目录下的文件
- 修改共享代码（infra/、共享类型、共享工具）前，先在 Issue comment 中说明需求，获得技术负责人确认后再修改
- 后端模块实现涉及数据模型时，在 `tests/fixtures/{module}.ts` 中创建或补充工厂函数（用于生成该模块的测试数据），供 L1 集成测试和后续 E2E 种子数据使用
- 对复杂内部逻辑补充单元测试
- 如需调整数据模型：先更新 module-design 文档，再更新 schema.prisma，最后运行 `npx prisma migrate dev --name <描述>`，migration 生成后立即 commit
- 每个有意义的改动 commit 一次，commit message 格式：`<type>(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "实现完成，契约测试和 L1 集成测试全部通过"` 报告

完成后更新 `docs/workflow-state.md`：设置 `substep: 5d-review`。

> **注意**：不要更新模块进度表的"实现"列。该列由 `/mp-workflow-update` 在模块粒度统一管理（契约测试 review 通过时设为 `in_progress`，模块所有 Task 完成时设为 `done`）。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
