# Project: {项目名称}

## 一句话描述
{这个项目是什么，解决什么问题}

## Tech Stack
- Language: {语言和版本}
- Runtime: {运行环境}
- Framework: {框架}
- DB: {数据库 + ORM}
- Test: {测试框架}

## 项目文档
- docs/prd.md — 产品需求
- docs/architecture.md — 架构设计
- docs/api-contracts.md — 接口契约
- docs/task-board.md — 任务看板

## 常用命令
- `{启动命令}` — 启动开发服务器
- `{测试命令}` — 跑全部测试
- `{契约测试命令}` — 只跑契约测试（如: `npx vitest run tests/` 或按目录划分）
- `{单文件测试命令}` — 跑单个文件测试（如: `npx vitest run tests/xxx.test.ts`）
- `{lint命令}` — lint 检查
- `{构建命令}` — 构建

## 项目结构
{填入 architecture.md 确定后的目录结构}

## 代码规范
- {规范1}
- {规范2}
- {规范3}

## 架构约定
- {约定1}
- {约定2}

## 测试环境
- 测试数据库: {如: 内存 SQLite / 独立测试文件 / 测试容器，说明与开发环境的隔离方式}
- 测试数据隔离: {如: 每个测试文件使用独立数据库 / 每个测试前清表 / 使用临时目录}
- 环境变量: {如: TEST_DB_PATH=:memory:, TODO_FILE=/tmp/test-todo.json}

## Git 规则
- 每次完成一个有意义的改动后，主动 commit
- commit message 格式：`<type>: <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 不要把无关改动放在同一个 commit

## 不要做的事
> 注意：CLAUDE.md 会被所有 Agent 加载。如果某条规则只针对特定角色，请标注适用角色（如"仅限 Implementer agent"），避免与其他角色的职责冲突。

- {禁止事项1}
- {禁止事项2}
- 不要修改契约测试代码（仅限 Implementer agent；Tester agent 负责编写和更新契约测试）

## 错误处理规则
- 修改一个问题超过 2 次仍未解决时，停止修改，分析根本原因
- 给出不同方案或建议寻求帮助
- 不要在同一个方向上尝试超过 3 次
