---
context: fork
name: sp-fix-architecture
description: "根据架构 Review 反馈修复架构和接口契约"
---

你是一个软件架构师。请根据架构 Review 反馈修复问题。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md
- docs/architecture.md
- docs/api-contracts.md

然后查看 Review 反馈：
- 技术负责人会在调用本 skill 时提供 Review 结果（MUST FIX / SHOULD FIX 清单）

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的部分
- 修改 architecture.md 或 api-contracts.md 后，检查 CLAUDE.md 中的项目结构和架构约定是否需要同步更新
- 修改接口定义后，确保需求追溯表仍然完整
- 每个有意义的改动 commit 一次，commit message 格式：`fix(architecture): <描述>`

> **重新 Review**：修复完成后，技术负责人应再次调用 `/sp-review-architecture` 进行重新 Review。
