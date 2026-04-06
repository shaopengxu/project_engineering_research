---
context: fork
name: mp-fix-scaffold
description: "根据脚手架 Review 反馈修复项目脚手架"
---

你是一个开发工程师。请根据脚手架 Review 反馈修复问题。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（验证技术选型和目录结构）
- docs/module-design/*.md（验证桩文件签名）

然后查看 Review 反馈：
1. 搜索 Issue：
   `gh issue list --label "type:scaffold" --search "脚手架 in:title" --state open --json number --jq '.[0].number'`
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机添加业务代码或测试代码
- 修复桩文件签名时，以 module-design 中的接口契约为准
- 修复配置问题后，实际运行验证：
  - 依赖安装：`npm install`
  - lint：`npm run lint`
  - 测试框架：`npm test -- --passWithNoTests`
  - Docker：`docker compose up -d`（如涉及）
  - Dev server：`npm run dev:server` / `npm run dev:web`（如涉及）
- 如果修复涉及 CLAUDE.md 中的常用命令或测试环境配置，同步更新 CLAUDE.md
- 每个有意义的改动 commit 一次，commit message 格式：`fix(scaffold): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`（当前状态已在 Step 4a review 等待中）。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-scaffold` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update 脚手架 review 通过` 推进状态。
