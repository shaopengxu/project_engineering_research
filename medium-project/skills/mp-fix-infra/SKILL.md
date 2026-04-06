---
context: fork
name: mp-fix-infra
description: "根据 infra Review 反馈修复基础设施代码"
argument-hint: "<issue-number>"
---

你是一个开发工程师。请根据 infra Review 反馈修复问题。

参数：$ARGUMENTS（格式：Issue 编号）

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（infra 职责定义、接口通用约定、日志约定）

然后阅读 infra 源代码：
- server/infra/ 目录下的完整代码

然后查看 Review 反馈：
- 运行 `gh issue view {issue-number} --comments` 查看 Review 结果
- 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 修复后验证编译通过：运行 `npm run build` 或 `npx tsc --noEmit`
- 如果修复涉及标准响应格式或中间件变更，确保与 architecture.md 通用约定一致
- 每个有意义的改动 commit 一次，commit message 格式：`fix(infra): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-infra {issue-number}` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update infra #N review 通过` 推进状态。
