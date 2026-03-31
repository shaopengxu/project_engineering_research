# 项目结构与环境配置

## 目录结构

```
project/
├── CLAUDE.md                        # 全局 CLAUDE.md（< 100 行）
├── README.md
├── docs/
│   ├── prd.md                       # PRD（> 500 行时可拆为 prd/ 目录）
│   ├── architecture.md              # 系统级架构（含接口通用约定、依赖矩阵、需求追溯表）
│   ├── module-design/               # 模块详细设计 + 接口契约
│   │   ├── module-a.md
│   │   ├── module-b.md
│   │   ├── web-app.md               # 前端整体（路由、布局、共享状态）
│   │   ├── web-app-{feature}.md     # 前端 feature 级（页面、交互、API 调用）
│   │   └── admin.md
├── server/                          # 后端
│   ├── modules/
│   │   ├── module-a/
│   │   │   ├── controller.ts
│   │   │   ├── service.ts
│   │   │   ├── repository.ts
│   │   │   ├── types.ts
│   │   │   └── index.ts             # 导出桩（Step 4 创建）
│   │   └── module-b/
│   │       └── ...
│   ├── infra/                       # 基础设施（数据库、配置、错误处理、响应格式）
│   └── app.ts
├── web/                             # 前端 SPA
│   ├── features/                    # 按业务域组织
│   │   ├── {feature-a}/             # 页面 + 私有组件 + hooks + API
│   │   └── {feature-b}/
│   ├── shared/                      # 共享组件、hooks、工具函数
│   ├── stores/                      # 全局状态管理
│   ├── routes.ts                    # 统一路由
│   └── main.tsx
├── admin/                           # 管理后台（结构同 web/）
│   └── ...
└── tests/
    ├── contracts/                   # 契约测试（按模块）
    ├── unit/                        # 单元测试（按模块）
    ├── integration/                 # 集成测试
    │   ├── {module-a}/              # L1 模块内
    │   └── paths/                   # L2 关键路径
    ├── e2e/                         # E2E 测试
    └── fixtures/                    # 共享测试数据
```

## 数据库迁移策略

- 使用 Prisma Migrate 管理数据库 schema 变更
- 统一一个 `prisma/schema.prisma` 文件，所有模块的数据模型集中定义
- Step 4 脚手架阶段：根据 module-design 中的数据模型创建初始 schema，运行 `npx prisma migrate dev --name init`
- Step 5 实现阶段：模块实现中如需调整数据模型，先更新 module-design 文档，再更新 schema.prisma，最后运行 `npx prisma migrate dev --name <描述>`
- 每次 migration 生成后立即 commit，commit message: `docs(infra): migration <描述> [#issue-number]`
- 测试环境使用独立数据库，通过 `DATABASE_URL` 环境变量区分

## 开发环境配置

Step 4 脚手架阶段需完成以下环境配置：

- **环境变量**：创建 `.env.example` 文件，列出所有必需的环境变量（`DATABASE_URL`、`PORT` 等），`.env` 加入 `.gitignore`
- **数据库**：本地 PostgreSQL 实例，在 README.md 或 `.env.example` 中说明连接方式
- **测试数据库**：独立的 PostgreSQL 测试库，测试前自动 migrate，测试后数据隔离（事务回滚或 truncate）
- **启动验证**：脚手架完成后确保 `npm install` + `npm run dev:server` + `npm run dev:web` 均可正常启动
- **TypeScript 配置**：根目录 `tsconfig.json` + 各端独立 tsconfig（server、web、admin）
