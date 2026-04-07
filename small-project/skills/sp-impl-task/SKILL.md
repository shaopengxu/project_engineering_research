---
context: fork
name: sp-impl-task
description: "实现业务代码 Task"
argument-hint: "<task-id>"
---

你是一个开发工程师。请完成指定 Task。

参数：$ARGUMENTS（格式：Task ID，如 Task-001）

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md
- docs/api-contracts.md（仅与当前 Task 相关的部分）
- docs/task-board.md（查看当前 Task 的描述、涉及模块、需通过测试）

要求：
- 让 task-board.md 中标注的相关契约测试全部通过
- 遵守 CLAUDE.md 中的代码规范和架构约定
- 不要修改契约测试代码。如果发现契约测试与 api-contracts.md 不一致，停下来指出具体矛盾（引用测试代码行号和契约文档章节），等待技术负责人确认
- 不要实现当前 Task 以外的功能
- 对复杂的内部逻辑（如计算、状态机、转换规则），补充单元测试
- 对跨模块调用或外部依赖交互，补充集成测试
- 单元测试和集成测试放在对应模块的测试目录下
- 每个有意义的改动 commit 一次，commit message 格式：`<type>(<module>): <描述>`
