---
context: fork
name: mp-impl-infra
description: "实现 infra 基础设施模块"
argument-hint: "<issue-number>"
---

你是一个开发工程师。请实现 infra 基础设施模块。

当前 Task Issue: #$ARGUMENTS

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：技术选型、目录结构、接口通用约定）

请完成以下基础设施：

1. 数据库连接：
   - Prisma Client 初始化和导出
   - 根据 module-design 中的数据模型创建 prisma/schema.prisma
   - 运行 `npx prisma migrate dev --name init` 创建初始 migration

2. 配置管理：
   - 环境变量加载（dotenv）
   - 补充 .env.example（在脚手架已创建的基础上，确保包含 DATABASE_URL、PORT、LOG_LEVEL 等必需变量）

3. 全局错误处理中间件：
   - 统一错误捕获和格式化
   - 错误响应遵循 architecture.md 的响应格式约定

4. 标准响应格式工具函数：
   - 成功响应和错误响应的格式化函数
   - 遵循 architecture.md 的响应格式约定

5. 日志基础设施（根据 architecture.md 日志约定）：
   - Logger 工具函数（JSON 结构化输出到 stdout，支持 error/warn/info/debug 级别）
   - 日志级别通过环境变量 `LOG_LEVEL` 控制
   - requestId 中间件（每个请求注入唯一 requestId，贯穿调用链）
   - 请求日志中间件（记录请求方法、路径、状态码、耗时）

6. 通用中间件：
   - 认证中间件（如 architecture.md 中有定义）

7. 数据库种子脚本：
   - 创建 `prisma/seed.ts` 入口文件（从 `tests/fixtures/` 导入工厂函数填充基础数据）
   - 在 `package.json` 中配置 `prisma.seed`（`"prisma": { "seed": "npx tsx prisma/seed.ts" }`）
   - 初始内容可为空壳，后续随 fixtures 积累自然填充

8. Express 应用初始化（server/app.ts）

验收标准：
- `npm install` 成功
- `npm run lint` 通过
- `npm run dev:server` 能启动（即使没有业务路由）
- 数据库连接成功
- 错误处理中间件可用

要求：
- 每个有意义的改动 commit 一次，commit message 包含 `[#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "infra 实现完成"` 报告

完成后更新 `docs/workflow-state.md`：设置 `step: 5`，`substep: 5a-review`；模块进度表中 infra 的"实现"列设为 `review`。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
