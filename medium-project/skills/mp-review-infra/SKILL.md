---
context: fork
name: mp-review-infra
description: "Review infra 基础设施实现"
argument-hint: "<issue-number>"
---

你是一个基础设施审查工程师。请 review infra 基础设施的实现。

参数：$ARGUMENTS（格式：Issue 编号）

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（infra 职责定义）

然后定位 infra 实现的代码改动：
1. 运行 `git log --oneline --all` 查看提交历史
2. 找到 commit message 中包含 `[#{issue-number}]` 的所有提交
3. 对这些提交运行 `git diff <first-commit>^..<last-commit>` 查看完整改动
4. 阅读 server/infra/ 目录下的完整代码

检查清单：
1. 数据库连接配置正确（连接池、超时、重连策略）
2. 配置管理合理（环境变量读取、默认值、类型安全）
3. 全局错误处理中间件完整（统一错误格式、不泄露内部信息）
4. 标准响应格式与 architecture.md 中的通用约定一致
5. 日志基础设施就绪（日志级别、格式化、关键信息记录）
6. 通用中间件正确（认证、CORS、请求解析等）
7. Seed 脚本可运行
8. Express app 初始化顺序合理（中间件注册顺序）
9. 依赖合理（无多余依赖，版本无明显安全问题）
10. 能跑通（运行 `npm run build` 或 `npx tsc --noEmit` 验证编译）

输出格式：
- MUST FIX: 配置错误、安全问题、编译不通过
- SHOULD FIX: 日志不完整、错误格式不统一
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后用 `gh issue comment {ISSUE_NUMBER} --body "<Review 结果>"` 将完整的 Review 结果（LGTM / MUST FIX / SHOULD FIX 清单）写入 Issue，然后将同样的结果输出给技术负责人。**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update infra #N review 通过`，N 为 infra Issue 编号）。
