---
context: fork
name: mp-fix-feature
description: "根据前端 Feature Review 反馈修复代码"
argument-hint: "<module-name> <feature-name>"
---

你是一个开发工程师。请根据前端 Feature Review 反馈修复问题。

参数：$ARGUMENTS（格式：模块名 feature名）

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（整体设计：共享层、路由结构）
- docs/module-design/{module}-{feature}.md（本 feature 的页面、交互、组件树）

然后阅读该 feature 的全部源代码：
- `{web|admin}/features/{feature}/`

然后查看 Review 反馈：
1. 搜索 Issue：`gh issue list --label "type:feature-review" --label "module:{module}" --search "Feature Review: {module}/{feature} in:title" --state open --json number --jq '.[0].number'`
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 修复后确保该 feature 的契约测试和 L1 集成测试仍然通过
- 不修改其他 feature 的代码。如果发现跨 feature 问题，在 Issue comment 中指出
- 不修改共享层代码（shared/）。如果修复需要变更共享层，在 Issue comment 中指出
- 每个有意义的改动 commit 一次，commit message 格式：`fix({module}/{feature}): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-feature {module} {feature}` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update {module} {feature} Feature Review LGTM` 推进状态。
