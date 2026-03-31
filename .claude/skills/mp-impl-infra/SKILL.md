---
context: fork
name: mp-impl-infra
description: "Medium-project Step 5a: 实现 infra 基础设施模块"
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
   - 创建 .env.example（DATABASE_URL、PORT 等）
   - .env 加入 .gitignore

3. 全局错误处理中间件：
   - 统一错误捕获和格式化
   - 错误响应遵循 architecture.md 的响应格式约定

4. 标准响应格式工具函数：
   - 成功响应和错误响应的格式化函数
   - 遵循 architecture.md 的响应格式约定

5. 通用中间件：
   - 认证中间件（如 architecture.md 中有定义）
   - 请求日志中间件

6. Express 应用初始化（server/app.ts）

验收标准：
- `npm install` 成功
- `npm run lint` 通过
- `npm run dev:server` 能启动（即使没有业务路由）
- 数据库连接成功
- 错误处理中间件可用

要求：
- 每个有意义的改动 commit 一次，commit message 包含 `[#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "infra 实现完成"` 报告
