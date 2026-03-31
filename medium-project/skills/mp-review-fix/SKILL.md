---
context: fork
name: mp-review-fix
description: "根据 Review 反馈修复问题"
argument-hint: "<module-name> <issue-number>"
---

你是一个开发工程师。请根据 Review 反馈修复问题。

参数：$ARGUMENTS（格式：模块名 Issue编号）

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md

然后查看 Issue 中的 Review 反馈：
- 运行 `gh issue view {issue-number} --comments` 查看 Review 结果

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 修复后确保所有契约测试和 L1 集成测试仍然通过
- 不要修改契约测试代码。如果认为 Review 反馈与契约矛盾，在 Issue comment 中指出
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 每个有意义的改动 commit 一次，commit message 格式：`fix(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复"` 报告

完成后更新 `docs/workflow-state.md`：设置 `substep: 5d-review`（等待重新 Review）。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
