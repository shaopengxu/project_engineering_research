---
context: fork
name: mp-fix-e2e
description: "根据 E2E 测试 Review 反馈修复测试代码"
---

你是一个测试工程师。请根据 E2E 测试 Review 反馈修复问题。

请先阅读以下文件：
- docs/prd.md（验收标准，修复依据）
- CLAUDE.md
- docs/architecture.md（核心用户流程）

然后阅读 E2E 测试代码：
- tests/e2e/ 目录下的所有测试文件

然后查看 Review 反馈：
1. 搜索 Issue：`python medium-project/scripts/mp-issue-helper.py find-or-create --label "type:e2e" --search "E2E 测试"`（只搜索，不传 --create-title 则不创建）
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的测试代码
- 只修改测试代码和种子数据，不修改业务实现代码
- 补充缺失的 E2E 测试时，对照 PRD 验收标准，确保覆盖完整用户流程
- 修复后运行 E2E 测试验证通过
- 每个有意义的改动 commit 一次，commit message 格式：`fix(e2e): <描述>`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

**不可自行修复的问题**：以下类型的问题超出本 skill 的修复范围，应在 Issue comment 中报告并停止，由技术负责人协调修复：
- **疑似业务 bug**：标注涉及的模块和接口 → 技术负责人安排 `/mp-impl-task {module} {issue-number}` 修复
- **跨模块集成问题**：标注涉及的模块组合 → 技术负责人安排 `/mp-test-integration {issue-number}` 补充覆盖以定位问题
- **种子数据不足**（需要新建 fixture 或修改 seed.ts）→ 可自行补充 `tests/fixtures/` 和 `prisma/seed.ts`

不更新 `docs/workflow-state.md`。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-e2e` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update E2E 测试通过` 推进状态。
