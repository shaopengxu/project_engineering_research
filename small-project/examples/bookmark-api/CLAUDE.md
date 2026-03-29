# Project: Bookmark API

## 一句话描述
一个个人书签收藏管理的 REST API 服务，为浏览器扩展或其他客户端提供书签和标签管理后端。

## Tech Stack
- Language: TypeScript 5
- Runtime: Node.js 20
- Framework: Express
- DB: SQLite (better-sqlite3)
- Test: Vitest + Supertest

## 项目文档
- docs/prd.md — 产品需求
- docs/architecture.md — 架构设计
- docs/api-contracts.md — 接口契约
- docs/task-board.md — 任务看板

## 常用命令
- `npm run dev` — 启动开发服务器（nodemon + ts-node）
- `npm test` — 跑全部测试
- `npx vitest run tests/bookmark/ tests/tag/` — 只跑契约测试
- `npx vitest run tests/bookmark/bookmark-crud.test.ts` — 跑单个文件测试
- `npm run lint` — lint 检查
- `npm run build` — 构建

## 项目结构
```
src/
├── modules/
│   ├── bookmark/
│   │   ├── bookmark.controller.ts   # 路由处理
│   │   ├── bookmark.service.ts      # 业务逻辑
│   │   ├── bookmark.repository.ts   # 数据访问
│   │   ├── bookmark.types.ts        # 模块内类型
│   │   └── index.ts                 # 模块导出
│   └── tag/
│       ├── tag.controller.ts
│       ├── tag.service.ts
│       ├── tag.repository.ts
│       ├── tag.types.ts
│       └── index.ts
├── shared/
│   ├── types.ts                     # 共享类型（分页、响应结构）
│   └── utils/
│       └── validation.ts            # 共享校验函数（URL、正整数）
├── infra/
│   ├── database.ts                  # SQLite 连接和建表
│   ├── error.ts                     # AppError 类和错误处理中间件
│   ├── response.ts                  # 统一响应格式辅助函数
│   └── config.ts                    # 应用配置（端口、数据库路径）
└── app.ts                           # Express 入口
tests/
├── bookmark/
│   ├── bookmark-crud.test.ts        # 书签 CRUD 契约测试
│   └── bookmark-tag.test.ts         # 书签-标签关联契约测试
└── tag/
    └── tag-crud.test.ts             # 标签 CRUD 契约测试
```

## 代码规范
- 使用 ESM 模块格式（import/export）
- 每个模块遵循 controller → service → repository 三层结构
- 所有公开函数必须有 JSDoc 注释
- 错误使用自定义 AppError 类，包含 HTTP 状态码和业务错误码
- 数据库操作全部在 repository 层，service 层不直接操作数据库

## 架构约定
- 模块依赖方向：bookmark 和 tag 各自依赖 shared/infra，禁止 bookmark 和 tag 之间直接互相调用
- 书签-标签关联逻辑归属 bookmark 模块，通过操作 bookmark_tag 表实现
- shared/ 目录只放被 2 个以上模块使用的代码，不放业务逻辑
- infra/ 目录负责基础设施（数据库、错误处理、配置），不包含业务逻辑
- 所有接口统一使用 { data } / { error: { code, message } } 响应格式

## 测试环境
- 测试数据库: 内存 SQLite（`:memory:`），每个测试文件使用独立的数据库实例
- 测试数据隔离: 每个测试文件创建独立的内存数据库，测试结束后自动销毁
- 环境变量: TEST_DB_PATH=:memory:

## Git 规则
- 每次完成一个有意义的改动后，主动 commit
- commit message 格式：`<type>: <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 不要把无关改动放在同一个 commit

## 不要做的事
- 不要添加用户认证和权限管理
- 不要引入 ORM（直接使用 better-sqlite3 的同步 API）
- 不要修改契约测试代码（仅限 Implementer agent；Tester agent 负责编写和更新契约测试）
- 不要在 repository 层以外直接操作数据库
- 不要在 bookmark 模块和 tag 模块之间创建直接的 import 依赖
- 不要使用异步数据库驱动（better-sqlite3 是同步 API，不需要 async/await 操作数据库）

## 错误处理规则
- 修改一个问题超过 2 次仍未解决时，停止修改，分析根本原因
- 给出不同方案或建议寻求帮助
- 不要在同一个方向上尝试超过 3 次
