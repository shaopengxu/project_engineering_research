---
context: fork
name: mp-review-scaffold
description: "Review 项目脚手架"
---

你是一个工程审查工程师。请 review 项目脚手架的完整性和正确性。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（验证目录结构与架构一致）
- docs/module-design/*.md（验证桩文件签名）

然后执行以下验证：

检查清单：
1. 依赖安装成功（运行 `npm install` 验证）
2. lint 命令能跑通（运行 `npm run lint` 验证）
3. 测试框架能启动（运行 `npm test -- --passWithNoTests` 或类似命令验证）
4. docker-compose.yml 已创建，`docker compose up -d` 能成功启动（运行验证）
5. 后端模块导出桩文件存在且函数签名与 module-design 中的接口契约一致（逐个检查 server/modules/{module}/）
6. .env.example 已创建，.env 已加入 .gitignore
7. TypeScript 配置正确（根目录 + 各端独立 tsconfig）
8. CLAUDE.md 已回填常用命令和测试环境配置（对比脚手架实际配置，确认一致）

对于检查项 1-4，请实际运行命令并报告结果。
对于检查项 5-8，请阅读文件内容进行验证。

输出格式：
- MUST FIX: 依赖安装失败、lint 不通过、测试框架无法启动、docker-compose 无法启动、桩文件签名与契约不一致
- SHOULD FIX: .env.example 缺失、TypeScript 配置问题、CLAUDE.md 未回填或与实际配置不一致
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后：将 Review 结果输出给技术负责人，**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update 脚手架 review 通过`）。
