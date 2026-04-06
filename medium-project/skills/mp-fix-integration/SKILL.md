---
context: fork
name: mp-fix-integration
description: "根据 L2 集成测试 Review 反馈修复测试代码"
argument-hint: "<issue-number>"
---

你是一个测试工程师。请根据 L2 集成测试 Review 反馈修复问题。

参数：$ARGUMENTS（格式：Issue 编号）

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（关键业务路径、模块依赖关系）
- 相关模块的 docs/module-design/*.md（接口契约）

然后阅读集成测试代码：
- tests/integration/paths/ 目录下的测试代码

然后查看 Review 反馈：
- 运行 `gh issue view {issue-number} --comments` 查看 Review 结果
- 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的测试代码
- 只修改测试代码，不修改业务实现代码
- 确保测试使用真实模块调用，不 mock 其他模块
- 修复后运行集成测试验证：`npm test -- --testPathPattern=integration/paths`
- 每个有意义的改动 commit 一次，commit message 格式：`fix(integration): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-integration {issue-number}` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update {module} L2 集成测试 #N 完成` 推进状态。
