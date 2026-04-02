---
context: fork
name: mp-scaffold
description: "根据架构文档初始化项目脚手架 + 回填 CLAUDE.md"
---

你是一个软件架构师。请根据架构文档初始化项目脚手架。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：技术选型、目录结构）
- docs/module-design/（所有模块设计文件，了解数据模型和接口签名）

请完成以下工作：

1. **项目目录结构**：
   - 根据 architecture.md 的目录结构创建项目框架
   - 创建所有模块目录
   - 创建测试目录结构（按 architecture.md 的目录结构）

2. **依赖安装与构建配置**：
   - 安装依赖（根据 architecture.md 技术选型，包括测试工具链：Vitest、React Testing Library、MSW、Playwright 等）
   - 配置构建工具、测试框架、lint
   - 初始化 Playwright（`npx playwright install --with-deps`）
   - 配置 TypeScript（根目录 tsconfig.json + 各端独立 tsconfig）

3. **环境配置**：
   - 创建 `docker-compose.yml`（至少包含 PostgreSQL 服务，配置开发和测试两个数据库）
   - 创建 `.env.example`（DATABASE_URL、PORT、LOG_LEVEL 等必需环境变量）
   - `.env` 加入 `.gitignore`

4. **导出桩文件**：
   - 后端：为每个后端模块创建 `index.ts` 导出桩文件，根据 module-design 中的接口契约声明函数签名，函数体 `throw new Error('Not implemented')`
   - 前端：为每个 feature 创建 `api/` 层桩文件（导出 API 调用函数，函数体 `throw new Error('Not implemented')`）和页面组件桩文件（导出空壳组件），确保前端契约测试能编译

5. **启动验证**：
   - 确保 `docker compose up -d` 能启动本地依赖
   - 确保 `npm install` 成功
   - 确保 `npm run lint` 通过
   - 确保测试框架能启动
   - 确保 `npm run dev:server` 能启动（即使没有业务路由）
   - 确保 `npm run dev:web` 能启动（即使没有业务页面）
   - 如有管理后台：确保 `npm run dev:admin` 能启动

6. **回填 CLAUDE.md**：
   - 常用命令（与实际脚手架配置一致）
   - 测试环境（隔离方式、环境变量）

要求：
- 不要写业务代码和测试代码
- 每个有意义的改动 commit 一次

完成后更新 `docs/workflow-state.md`：设置 `step: 4`，`substep: 4a-review`。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
