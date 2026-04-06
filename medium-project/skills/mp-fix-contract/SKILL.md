---
context: fork
name: mp-fix-contract
description: "根据契约测试 Review 反馈修复测试代码"
argument-hint: "<module-name> <issue-number> [feature]"
---

你是一个测试工程师。请根据契约测试 Review 反馈修复问题。

参数：$ARGUMENTS（格式：模块名 Issue编号 [feature名]）
- 后端模块：`模块名 Issue编号`
- 前端模块：`模块名 Issue编号 feature名`

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（接口契约，修复依据）
- 前端模块还需读：docs/module-design/{module}-{feature}.md

然后阅读测试代码：
- 后端：tests/contracts/{module}/ 目录
- 前端：tests/contracts/{module}/{feature}/ 目录

然后查看 Review 反馈：
- 运行 `gh issue view {issue-number} --comments` 查看 Review 结果
- 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的测试代码
- 只修改测试代码，不修改业务实现代码
- 修复后测试应能编译/加载（允许执行失败 — TDD 红阶段）
- 新增的测试用例需注释标注业务规则来源（对应 module-design 中的章节）
- 每个有意义的改动 commit 一次，commit message 格式：`fix(contract): {module} - <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`（模块级进度通过 GitHub Issues 追踪）。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-contract {module} {issue-number} [feature]` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update` 推进状态。
