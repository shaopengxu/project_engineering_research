---
context: fork
name: mp-fix-module-design
description: "根据模块设计 Review 反馈修复设计文档"
argument-hint: "<module-name> <issue-number> [feature-name] | --summary <issue-number>"
---

你是一个软件架构师。请根据模块设计 Review 反馈修复问题。

参数：$ARGUMENTS（格式：模块名 Issue编号 [feature名]，或 `--summary Issue编号`）
- 两个参数（模块名 + Issue 编号）：后端模块或前端整体设计修复
- 三个参数（模块名 + Issue 编号 + feature 名）：前端 feature 级设计修复
- `--summary` + Issue 编号：汇总检查修复

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md

根据参数模式读取对应文件：
- 单模块：`docs/module-design/{module}.md` + 已有的其他 module-design/*.md（检查错误码、接口风格）
- 前端 feature：`docs/module-design/{module}.md`（整体设计）+ `docs/module-design/{module}-{feature}.md` + 对应后端模块设计
- `--summary`：所有 `docs/module-design/*.md` + `docs/prd.md`

然后查看 Review 反馈：
- 运行 `gh issue view {issue-number} --comments` 查看 Review 结果
- 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的部分
- 不要修改其他模块的设计文件。如果修复过程中发现跨模块不一致，在 Issue comment 中指出
- 修复接口契约时，确保五要素（输入、输出、业务规则、错误码、consumers）完整
- 修复错误码冲突时，只改本模块的错误码，不改其他模块
- `--summary` 模式修复的是 `docs/architecture.md` 中的接口依赖矩阵和需求追溯表
- 每个有意义的改动 commit 一次，commit message 格式：`fix(module-design): {module} - <描述>`
- 完成后用 `gh issue comment {issue-number} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`（模块级进度通过 GitHub Issues 追踪）。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-module-design {module} {issue-number} [feature] | --summary {issue-number}` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update` 推进状态（如 `/mp-workflow-update user 模块设计 review 通过`）。
