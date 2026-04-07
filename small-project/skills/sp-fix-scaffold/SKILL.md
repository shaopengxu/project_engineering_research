---
context: fork
name: sp-fix-scaffold
description: "根据脚手架 Review 反馈修复脚手架和任务拆分"
---

你是一个软件架构师。请根据 Review 反馈修复脚手架和任务拆分。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md
- docs/api-contracts.md
- docs/task-board.md

然后查看 Review 反馈：
- 技术负责人会在调用本 skill 时提供 Review 结果

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 修复脚手架后，实际运行验证（依赖安装、lint、测试框架启动）
- 修复桩文件签名时，以 api-contracts.md 中的接口定义为准
- 如果修复涉及 CLAUDE.md 中的常用命令或测试环境，同步更新
- 每个有意义的改动 commit 一次，commit message 格式：`fix(scaffold): <描述>`

> **重新 Review**：修复完成后，技术负责人应再次调用 `/sp-review-scaffold` 进行重新 Review。
