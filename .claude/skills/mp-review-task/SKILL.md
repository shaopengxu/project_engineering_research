---
name: mp-review-task
description: "Medium-project Step 5d: Review 单个 Task 的代码改动"
argument-hint: "<module-name> <issue-number>"
---

你是一个代码审查工程师。请 review 指定 Task 的改动。

参数：$ARGUMENTS（格式：模块名 Issue编号）

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（本模块设计 + 接口契约）

然后定位当前 Task 的代码改动：
1. 运行 `git log --oneline --all` 查看提交历史
2. 找到 commit message 中包含 `[#{issue-number}]` 的所有提交
3. 对这些提交运行 `git diff <first-commit>^..<last-commit>` 查看完整改动
只 review 当前 Task 涉及的改动，不要评审其他 Task 的代码。

检查清单：
1. 功能是否符合 module-design/{module}.md 中当前 Task 对应接口的定义
2. L1 集成测试是否覆盖了真实串联（后端：controller→service→repository；前端：页面→hooks→API）
3. 是否遵守 CLAUDE.md 的规范
4. 模块间依赖方向是否正确（不反向依赖）
5. 是否有安全问题（SQL 注入、XSS、敏感信息泄露等）
6. 是否违反了共享代码修改规则（修改 infra/ 等共享代码前是否获得确认、不应修改其他模块文件）
7. 实现质量 — 明显的性能问题、未处理的边界条件、过度设计

输出格式：
- MUST FIX: 功能错误、安全问题、违反共享代码规则
- SHOULD FIX: 违反约定、缺少测试
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

输出结尾建议：在 Issue #{issue-number} 中 comment Review 结果。
