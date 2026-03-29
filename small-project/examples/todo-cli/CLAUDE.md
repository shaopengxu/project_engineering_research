# Project: Todo CLI

## 一句话描述
一个本地命令行 Todo 管理工具，让开发者在终端内快速管理待办事项。

## Tech Stack
- Language: TypeScript 5
- Runtime: Node.js 20
- Framework: Commander.js
- DB: JSON 文件（无 ORM）
- Test: Vitest

## 项目文档
- docs/prd.md — 产品需求
- docs/architecture.md — 架构设计
- docs/api-contracts.md — 接口契约
- docs/task-board.md — 任务看板

## 常用命令
- `npm run dev -- add "test"` — 开发模式运行
- `npm test` — 跑全部测试
- `npx vitest run tests/` — 只跑契约测试
- `npx vitest run tests/task.test.ts` — 跑单个文件测试
- `npm run lint` — lint 检查
- `npm run build` — 构建

## 项目结构
```
src/
├── cli.ts              # 命令定义和入口
├── task.ts             # 任务管理业务逻辑
├── storage.ts          # JSON 文件读写
└── types.ts            # 共享类型定义
tests/
├── cli.test.ts         # CLI 命令契约测试
├── task.test.ts        # 任务管理契约测试
├── storage.test.ts     # 存储模块契约测试
└── e2e/                # Step 6 时创建，存放 E2E 测试
```

## 代码规范
- 使用 ESM 模块格式（import/export）
- 函数优先，避免不必要的 class
- 所有公开函数必须有 JSDoc 注释
- 错误使用自定义 Error 类（TodoError），包含退出码

## 架构约定
- 模块依赖方向：cli → task → storage，禁止反向依赖
- storage 模块不理解业务含义，只做序列化/反序列化
- task 模块不直接操作文件系统，通过 storage 模块间接访问
- cli 模块不包含业务逻辑，只做参数解析和输出格式化

## 测试环境
- 测试数据隔离: 每个测试使用独立的临时目录，测试结束后自动清理
- 环境变量: TODO_FILE=/tmp/test-{random}.json（每个测试文件使用不同的临时文件路径）

## Git 规则
- 每次完成一个有意义的改动后，主动 commit
- commit message 格式：`<type>: <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 不要把无关改动放在同一个 commit

## 不要做的事
- 不要引入数据库（SQLite 等），使用 JSON 文件即可
- 不要添加网络功能（云同步、HTTP 接口等）
- 不要修改契约测试代码（仅限 Implementer agent；Tester agent 负责编写和更新契约测试）
- 不要在 storage 模块中引入业务逻辑
- 不要使用 console.log 替代 process.stdout/stderr

## 错误处理规则
- 修改一个问题超过 2 次仍未解决时，停止修改，分析根本原因
- 给出不同方案或建议寻求帮助
- 不要在同一个方向上尝试超过 3 次
