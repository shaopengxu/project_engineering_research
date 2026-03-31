---
context: fork
name: mp-test-integration
description: "Medium-project Step 5g: 编写 L2 跨模块关键路径集成测试"
argument-hint: "<issue-number>"
---

你是一个开发工程师。请编写跨模块集成测试。

当前 Task Issue: #$ARGUMENTS

请先阅读 Issue 了解关键路径和涉及模块：
- 运行 `gh issue view $ARGUMENTS` 查看 Issue 详情

然后阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：跨模块数据流中与本关键路径相关的部分）
- docs/module-design/（涉及模块的接口定义）

触发条件：当前模块完成模块级 Review，且被依赖的模块已实现完成。串行开发天然保证被依赖模块先完成，无需额外协调。

要求：
- 在 tests/integration/paths/ 目录下创建集成测试文件
- 使用真实的模块间调用（不 Mock 其他模块）
- 外部依赖（数据库等）使用测试环境（内存数据库或测试容器）
- 覆盖关键路径的正常流程和关键异常流程
- 每个测试用例标注对应的业务路径
- 每个有意义的改动 commit 一次，commit message 格式：`test(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "L2 集成测试完成"` 报告
