---
context: fork
name: mp-review-integration
description: "Review L2 跨模块集成测试"
argument-hint: "<issue-number>"
---

你是一个集成测试审查工程师。请 review L2 跨模块集成测试。

参数：$ARGUMENTS（格式：Issue 编号）

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（关键业务路径、模块依赖关系）
- 相关模块的 docs/module-design/*.md（接口契约）

然后定位集成测试代码：
1. 运行 `git log --oneline --all` 查看提交历史
2. 找到 commit message 中包含 `[#{issue-number}]` 的所有提交
3. 对这些提交运行 `git diff <first-commit>^..<last-commit>` 查看完整改动
4. 阅读 tests/integration/paths/ 目录下的测试代码

检查清单：
1. 测试覆盖了关键业务路径的完整链路（如 下单 → 扣库存 → 创建支付单）
2. 使用真实模块调用，不 mock 其他模块
3. 外部依赖使用测试环境（如测试数据库）
4. 覆盖正常流程和关键异常流程
5. 测试数据通过 fixtures 工厂函数创建，不依赖硬编码数据
6. 测试间无共享状态，可独立运行
7. 测试能编译并运行通过（运行 `npm test -- --testPathPattern=integration/paths` 验证）

输出格式：
- MUST FIX: 关键路径未覆盖、mock 了本应真实调用的模块、测试运行失败
- SHOULD FIX: 异常流程未覆盖、测试数据硬编码
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后用 `gh issue comment {ISSUE_NUMBER} --body "<Review 结果>"` 将完整的 Review 结果（LGTM / MUST FIX / SHOULD FIX 清单）写入 Issue，然后将同样的结果输出给技术负责人。**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update user L2 集成测试完成`）。
