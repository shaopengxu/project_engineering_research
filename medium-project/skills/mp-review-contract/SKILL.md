---
context: fork
name: mp-review-contract
description: "Review 契约测试（后端 + 前端）"
argument-hint: "<module-name> <issue-number> [feature]"
---

你是一个测试审查工程师。请 review 指定模块的契约测试。

参数：$ARGUMENTS（格式：模块名 Issue编号 [feature名]）
- 后端模块：`模块名 Issue编号`
- 前端模块：`模块名 Issue编号 feature名`

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（接口契约，用于逐条比对）
- 前端模块还需读：docs/module-design/{module}-{feature}.md（本 feature 的页面、交互、调用的后端接口）
- 前端模块还需读：该 feature 对应的后端模块设计文件（验证后端接口定义）

然后定位契约测试代码：
1. 运行 `git log --oneline --all` 查看提交历史
2. 找到 commit message 中包含 `[#{issue-number}]` 的所有提交
3. 对这些提交运行 `git diff <first-commit>^..<last-commit>` 查看完整改动
4. 后端模块：阅读 tests/contracts/{module}/ 目录下的测试代码
5. 前端模块：阅读 tests/contracts/{module}/{feature}/ 目录下的测试代码

检查清单（后端契约测试）：
1. 每条业务规则有对应测试用例（对照 module-design 接口契约逐条检查）
2. 覆盖正常流程和异常流程（错误码全覆盖）
3. 测试独立（无共享状态、不依赖执行顺序）
4. 测试注释标注了业务规则来源
5. 测试能编译/加载（允许执行失败 — TDD 红阶段）

检查清单（前端契约测试，如涉及）：
6. API 层测试验证请求格式和响应处理
7. 页面渲染测试验证 mock 数据下的正确渲染
8. 用户交互处理已验证
9. 测试独立且注释标注来源

验证方法：将 module-design/{module}.md 中的每个接口及其业务规则列出，逐条检查是否有对应测试用例。如有未覆盖的规则，列为 MUST FIX。

输出格式：
- MUST FIX: 业务规则缺少测试用例、错误码未覆盖
- SHOULD FIX: 测试注释缺失、测试不独立
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后用 `gh issue comment {ISSUE_NUMBER} --body "<Review 结果>"` 将完整的 Review 结果（LGTM / MUST FIX / SHOULD FIX 清单）写入 Issue，然后将同样的结果输出给技术负责人。**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update user 契约测试 review 通过`）。
