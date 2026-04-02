---
context: fork
name: mp-test-contract
description: "为后端模块编写契约测试"
argument-hint: "<module-name> <issue-number>"
---

你是一个测试工程师。请为后端模块编写契约测试。

参数：$ARGUMENTS（格式：模块名 Issue编号）

契约测试的目的是：验证接口的输入输出是否符合接口契约的定义。
这些测试将在实现之前编写，作为 TDD 的驱动力。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（重点关注：接口契约部分 + 数据模型）
- server/modules/{module}/index.ts（导出桩文件，确认可用的函数签名）

要求：
- 每个接口的每条业务规则至少一个测试用例
- 包含正常流程和异常流程（错误码全覆盖）
- 测试之间互相独立，不依赖执行顺序
- 每个测试用例用注释标注对应的业务规则来源
- 测试代码放在 tests/contracts/{module}/ 目录下
- 此阶段只写契约测试，不写业务代码
- 如果接口契约有模糊或矛盾之处，停下来指出问题，不要自行假设
- 每个有意义的改动 commit 一次，commit message 格式：`test(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "契约测试编写完成"` 报告

Mock 策略：
- 模块间依赖：Mock / Stub
- 外部依赖（数据库等）：Mock（内存数据库可替代）

预期状态：测试代码能编译/加载，但执行时全部失败（因为实现不存在）— 这是 TDD 的正常状态（先红后绿）。导出桩文件解决编译问题。

注意：你只需要阅读本模块的设计文档（module-design/{module}.md），不需要阅读其他模块的文档。

完成后更新 `docs/workflow-state.md`：模块进度表中对应模块的"契约测试"列设为 `review`。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
