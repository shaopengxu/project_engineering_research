---
context: fork
name: mp-impl
description: "Medium-project Step 5c: 实现业务 Task（后端或前端）"
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
- 编写 L1 集成测试，放在 tests/integration/{module}/ 下：
  - 后端模块：controller → service → repository 真实串联，Mock 其他模块，数据库使用真实连接或测试容器
  - 前端模块：页面 → hooks → API 层串联，Mock 后端 API（MSW 或手动 mock）
- 遵守 CLAUDE.md 中的规范
- 不要修改契约测试代码。如果发现不一致，在 Issue comment 中指出具体矛盾，等待确认
- 不要实现当前 Task 以外的功能
- 不要修改其他模块目录下的文件
- 修改共享代码（infra/、共享类型、共享工具）前，先在 Issue comment 中说明需求，获得技术负责人确认后再修改
- 对复杂内部逻辑补充单元测试
- 如需调整数据模型：先更新 module-design 文档，再更新 schema.prisma，最后运行 `npx prisma migrate dev --name <描述>`，migration 生成后立即 commit
- 每个有意义的改动 commit 一次，commit message 格式：`<type>(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "实现完成，契约测试和 L1 集成测试全部通过"` 报告

完成后更新 `docs/workflow-state.md`：设置 `substep: 5d`（等待 Task Review）；模块进度表中对应模块的"实现"列设为 `in_progress`。
