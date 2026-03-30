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
- docs/architecture.md — 系统架构
- docs/module-design/ — 模块详细设计 + 接口契约
- 任务管理 — GitHub Projects（`gh issue list` 查看）

## 常用命令
- `{启动命令}` — 启动开发服务器
- `{测试命令}` — 跑全部测试
- `{契约测试命令}` — 只跑契约测试
- `{集成测试命令}` — 只跑集成测试
- `{单文件测试命令}` — 跑单个文件测试
- `{lint命令}` — lint 检查
- `{构建命令}` — 构建

## 项目结构
{只列顶层目录和模块名，不展开模块内部结构}
```
src/
├── modules/
│   ├── {module-a}/    # {一句话职责}
│   └── {module-b}/    # {一句话职责}
└── ...
tests/
├── contracts/         # 契约测试
├── integration/       # 集成测试（含 paths/ 关键路径）
├── e2e/               # E2E 测试
└── fixtures/          # 共享测试数据
```

## 代码规范
- {规范1}
- {规范2}

## 架构约定
- {约定1: 如模块间依赖方向}
- {约定2: 如分层规则}

## 测试环境
- 测试数据库: {如: 内存 SQLite / 测试容器}
- 测试数据隔离: {如: 每个测试文件使用独立数据库}
- 环境变量: {如: TEST_DB_PATH=:memory:}

## Git 规则
- 每次完成一个有意义的改动后，主动 commit
- commit message 格式：`<type>(<module>): <描述为什么改>`
- type: feat / fix / docs / refactor / test
- 不要把无关改动放在同一个 commit

## infra 修改规则
- 修改 infra/ 前，先在 Issue comment 中说明需求，获得技术负责人确认

## 不要做的事
> 注意：CLAUDE.md 会被所有 Agent 加载。如果某条规则只针对特定角色，请标注适用角色。

- {禁止事项1}
- {禁止事项2}
- 不要修改契约测试代码（仅限 Implementer agent）
- 不要修改其他模块目录下的文件（仅限 Implementer agent）
- 修改 infra/ 前需确认（仅限 Implementer agent）

## 错误处理规则
- 修改一个问题超过 2 次仍未解决时，停止修改，分析根本原因
- 给出不同方案或建议寻求帮助
- 不要在同一个方向上尝试超过 3 次

