---
context: fork
name: mp-fix-acceptance
description: "根据验收预检反馈修复问题"
---

你是一个开发工程师。请根据验收预检反馈修复问题。

请先阅读以下文件：
- docs/prd.md（验收标准）
- docs/architecture.md（模块列表）
- docs/workflow-state.md（当前进度）
- CLAUDE.md

然后查看预检反馈：
1. 搜索 Issue：`python medium-project/scripts/mp-issue-helper.py find-or-create --label "type:acceptance" --search "验收预检"`（只搜索，不传 --create-title 则不创建）
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条预检 comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 可修复的问题类型：
  - **测试未通过**：定位失败测试，修复测试代码或业务代码
  - **验收标准缺少 E2E 测试**：补充 E2E 测试用例（对照 PRD 验收标准）
  - **README 不完整**：补充项目启动说明
  - **.env.example 不完整**：补充缺失的环境变量
- 不可修复的问题（在 Issue comment 中报告，由技术负责人协调处理）：
  - 模块 Review Issue 未关闭（需先完成对应模块 Review 流程）
  - 实现类 Task Issue 未关闭（需先完成对应 Task）
- 修复后运行全量测试验证：`npm test` 和 E2E 测试
- 每个有意义的改动 commit 一次，commit message 格式：`fix(acceptance): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新预检。"` 报告，并列出无法自行修复的问题

不更新 `docs/workflow-state.md`。

> **重新预检**：修复完成后，技术负责人应再次调用 `/mp-review-acceptance` 进行重新预检。

> **状态更新边界**：skill 不修改 workflow-state。验收通过后由技术负责人通过 `/mp-workflow-update 验收通过` 推进状态。
