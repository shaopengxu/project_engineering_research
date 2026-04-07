---
context: fork
name: mp-fix-architecture
description: "根据架构 Review 反馈修复 architecture.md"
---

你是一个软件架构师。请根据架构 Review 反馈修复问题。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md
- docs/architecture.md

然后查看 Review 反馈：
1. 搜索 Issue：`python medium-project/scripts/mp-issue-helper.py find-or-create --label "type:architecture" --search "架构设计"`（只搜索，不传 --create-title 则不创建）
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的部分
- 如果 Review 涉及模块划分调整（增删模块），需同步更新 CLAUDE.md 的项目结构、架构约定和"不要做的事"
- 如果 Review 涉及接口通用约定或日志约定，确保修改后文档内部自洽
- 每个有意义的改动 commit 一次，commit message 格式：`fix(architecture): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`（当前状态已在 Step 2 review 等待中）。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-architecture` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update Step 2 review 通过` 推进状态。
