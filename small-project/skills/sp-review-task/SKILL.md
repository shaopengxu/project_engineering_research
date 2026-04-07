---
context: fork
name: sp-review-task
description: "Review 单个 Task 的代码改动"
argument-hint: "<task-id>"
---

你是一个代码审查工程师。请 review 当前 Task 的改动。

参数：$ARGUMENTS（格式：Task ID，如 Task-001）

请先阅读以下文件：
- CLAUDE.md
- docs/api-contracts.md（仅与当前 Task 相关的部分）
- docs/architecture.md
- docs/task-board.md（查看当前 Task 的描述和涉及模块）

然后查看当前 Task 的代码改动：
- 运行 `git log --oneline` 查看提交历史
- 找到当前 Task 相关的 commit，运行 `git diff` 查看完整改动
- 只 review 当前 Task 涉及的改动，不要评审其他 Task 的代码

检查清单（按优先级）：
1. 功能是否符合 api-contracts.md 中当前 Task 对应接口的定义
2. 测试是否覆盖了当前 Task 涉及的所有业务规则
3. 是否遵守 CLAUDE.md 的架构约定和代码规范
4. 模块间依赖方向是否正确
5. 是否有安全问题（SQL 注入、XSS、敏感信息泄露等）
6. 实现质量 — 是否有明显的性能问题、未处理的边界条件、过度设计

输出格式：
- MUST FIX: 功能错误、安全问题
- SHOULD FIX: 违反约定、缺少测试
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

输出结尾附上建议：将 task-board.md 中 {Task ID} 状态更新为"已完成"或"需修复"。
