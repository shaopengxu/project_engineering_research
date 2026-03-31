# Project: {项目名称}

## 一句话描述
{这个项目是什么，解决什么问题}

## Tech Stack
- Language: TypeScript（全栈）
- Runtime: Node.js
- Backend: Express + Prisma + PostgreSQL
- Frontend: React + Vite + React Router + Ant Design + TanStack Query + Zustand
- Test: Vitest + React Testing Library

## 项目文档
- docs/prd.md — 产品需求
- docs/architecture.md — 系统架构
- docs/module-design/ — 模块详细设计 + 接口契约
- 任务管理 — GitHub Projects（`gh issue list` 查看）

## 常用命令
- `npm run dev:server` — 启动后端开发服务器
- `npm run dev:web` — 启动前端 SPA
- `npm run dev:admin` — 启动管理后台
- `npx vitest` — 跑全部测试
- `npx vitest tests/contracts` — 只跑契约测试
- `npx vitest tests/integration` — 只跑集成测试
- `npx vitest {file}` — 跑单个文件测试
- `npm run lint` — ESLint + Prettier 检查
- `npm run build` — 构建全部

## 项目结构
```
server/                # 后端 (Express + Prisma)
├── modules/
│   ├── {module-a}/    # {一句话职责}
│   └── {module-b}/    # {一句话职责}
├── infra/             # 数据库、配置、错误处理、响应格式
└── app.ts
web/                   # 前端 SPA (React + Vite)
├── pages/
├── components/
├── hooks/
├── api/
└── stores/
admin/                 # 管理后台 (React + Vite + Ant Design)
└── ...                # 结构同 web/
tests/
├── contracts/         # 契约测试
├── unit/              # 单元测试
├── integration/       # 集成测试（含 paths/ 关键路径）
├── e2e/               # E2E 测试
└── fixtures/          # 共享测试数据
```

## 代码规范
- ESLint + Prettier，提交前必须通过 lint
- 文件命名：kebab-case（如 user-service.ts）
- 组件命名：PascalCase（如 UserList.tsx）
- {项目特有规范}

## 架构约定
- 后端模块间依赖单向，禁止循环
- 后端分层：controller → service → repository，不跳层
- 前端通过 api/ 层调用后端，组件不直接发请求
- 前端状态：页面内用 useState，跨页面用 Zustand，服务端数据用 TanStack Query
- {项目特有约定}

## 测试环境
- 测试数据库: PostgreSQL 测试库（通过 DATABASE_URL 环境变量区分）
- 测试数据隔离: 每个测试文件使用事务回滚
- 前端测试: Vitest + React Testing Library + jsdom

## Git 规则
- 每次完成一个有意义的改动后，主动 commit
- commit message 格式：`<type>(<module>): <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 不要把无关改动放在同一个 commit

## 共享代码修改规则
- 修改 infra/、共享类型、共享工具前，先在 Issue comment 中说明需求，获得技术负责人确认

## 不要做的事
> 注意：CLAUDE.md 会被所有 Agent 加载。如果某条规则只针对特定角色，请标注适用角色。

- 不要修改契约测试代码（仅限 Implementer agent）
- 不要修改其他模块目录下的文件（仅限 Implementer agent）

## 错误处理规则
- 修改一个问题超过 2 次仍未解决时，停止修改，分析根本原因
- 给出不同方案或建议寻求帮助
- 不要在同一个方向上尝试超过 3 次

