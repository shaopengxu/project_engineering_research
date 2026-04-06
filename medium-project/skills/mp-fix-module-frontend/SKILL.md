---
context: fork
name: mp-fix-module-frontend
description: "根据前端模块 Review 反馈修复代码"
argument-hint: "<module-name>"
---

你是一个开发工程师。请根据前端模块 Review 反馈修复问题。

模块名：$ARGUMENTS

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（整体设计：共享层、路由结构、API Client 配置）

然后确定该模块的 feature 列表：
- 在 `docs/module-design/` 中查找所有 `{module}-*.md` 文件，逐个阅读

然后阅读该模块的全部源代码：
- `{web|admin}/features/` 下各 feature 目录
- `{web|admin}/shared/`（共享层）

然后查看 Review 反馈：
1. 搜索 Issue：
   `gh issue list --label "type:module-review" --label "module:{module}" --search "模块 Review: {module} in:title" --state open --json number --jq '.[0].number'`
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 修复后确保所有 feature 的契约测试和 L1 集成测试仍然通过
- 修复跨 feature 一致性问题时（如命名风格、错误处理方式），统一到设计文档约定的方式
- 修复共享层问题时（如 feature 专属逻辑混入 shared/），将代码移至对应 feature 内
- 每个有意义的改动 commit 一次，commit message 格式：`fix({module}): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-module-frontend {module}` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update {module} 模块 Review LGTM` 推进状态。
