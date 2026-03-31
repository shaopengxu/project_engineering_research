---
context: fork
name: mp-scaffold
description: "Medium-project Step 4a: 根据架构文档初始化项目脚手架 + 回填 CLAUDE.md"
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
   - 创建测试目录结构：
     ```
     tests/
     ├── contracts/          # 契约测试（按模块组织，前端按 feature 子目录）
     ├── unit/               # 单元测试（按模块组织）
     ├── integration/        # 集成测试
     │   └── paths/          # L2: 关键路径集成
     ├── e2e/                # E2E 测试（按用户流程）
     └── fixtures/           # 共享测试数据（工厂函数，非硬编码）
     ```

2. **依赖安装与构建配置**：
   - 安装依赖（根据 architecture.md 技术选型）
   - 配置构建工具、测试框架、lint
   - 配置 TypeScript（根目录 tsconfig.json + 各端独立 tsconfig）

3. **环境配置**：
   - 创建 `.env.example`（DATABASE_URL、PORT 等必需环境变量）
   - `.env` 加入 `.gitignore`

4. **导出桩文件**：
   - 为每个后端模块创建 `index.ts` 导出桩文件
   - 根据 module-design 中的接口契约声明函数签名
   - 函数体 `throw new Error('Not implemented')`

5. **启动验证**：
   - 确保 `npm install` 成功
   - 确保 `npm run lint` 通过
   - 确保测试框架能启动
   - 确保 `npm run dev:server` 能启动（即使没有业务路由）

6. **回填 CLAUDE.md**：
   - 常用命令（与实际脚手架配置一致）
   - 测试环境（隔离方式、环境变量）

要求：
- 不要写业务代码和测试代码
- 每个有意义的改动 commit 一次
