---
context: fork
name: sp-fix-contract
description: "根据契约测试 Review 反馈修复测试代码"
---

你是一个测试工程师。请根据 Review 反馈修复契约测试。

请先阅读以下文件：
- CLAUDE.md
- docs/api-contracts.md（接口契约，修复依据）

然后阅读测试代码：
- tests/ 目录下的契约测试文件

然后查看 Review 反馈：
- 技术负责人会在调用本 skill 时提供 Review 结果

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的测试代码
- 只修改测试代码，不修改业务实现代码
- 修复后测试应能编译/加载（允许执行失败 — TDD 红阶段）
- 新增的测试用例需注释标注业务规则来源
- 每个有意义的改动 commit 一次，commit message 格式：`fix(test): <描述>`

> **重新 Review**：修复完成后，技术负责人应再次调用 `/sp-review-contract` 进行重新 Review。
