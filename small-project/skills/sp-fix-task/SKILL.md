---
context: fork
name: sp-fix-task
description: "根据 Task Review 反馈修复实现代码"
argument-hint: "<task-id>"
---

你是一个开发工程师。请根据 Review 反馈修复当前 Task 的问题。

参数：$ARGUMENTS（格式：Task ID，如 Task-001）

请先阅读以下文件：
- CLAUDE.md
- docs/api-contracts.md（仅与当前 Task 相关的部分）
- docs/task-board.md（查看当前 Task 的描述和涉及模块）

然后查看 Review 反馈：
- 技术负责人会在调用本 skill 时提供 Review 结果

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 修复后确保所有相关契约测试仍然通过
- 不要修改契约测试代码。如果认为 Review 反馈与 api-contracts.md 矛盾，停下来指出具体矛盾，等待技术负责人确认
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 每个有意义的改动 commit 一次，commit message 格式：`fix(<module>): <描述>`

> **重新 Review**：修复完成后，技术负责人应再次调用 `/sp-review-task {task-id}` 进行重新 Review。
