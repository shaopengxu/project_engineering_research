---
context: fork
name: sp-fix-e2e
description: "根据 E2E 测试 Review 反馈修复测试代码"
---

你是一个测试工程师。请根据 E2E 测试 Review 反馈修复问题。

请先阅读以下文件：
- docs/prd.md（验收标准，修复依据）
- CLAUDE.md
- docs/architecture.md

然后阅读 E2E 测试代码：
- tests/e2e/ 目录下的所有测试文件

然后查看 Review 反馈：
- 技术负责人会在调用本 skill 时提供 Review 结果

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的测试代码
- 只修改测试代码，不修改业务实现代码
- 补充缺失的 E2E 测试时，对照 PRD 验收标准确保覆盖完整用户流程
- 修复后运行 E2E 测试验证通过
- 每个有意义的改动 commit 一次，commit message 格式：`fix(e2e): <描述>`

> **重新 Review**：修复完成后，技术负责人应再次调用 `/sp-review-e2e` 进行重新 Review。
