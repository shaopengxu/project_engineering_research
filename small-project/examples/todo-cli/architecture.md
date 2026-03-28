# Todo CLI 架构文档

## 1. 技术选型

| 类别 | 选择 | 理由 |
|------|------|------|
| 语言 | TypeScript 5 | 类型安全，开发效率高 |
| 运行时 | Node.js 20 | LTS 版本，稳定且支持最新 ES 特性 |
| CLI 框架 | Commander.js | 社区成熟，API 简洁，零配置即可生成帮助信息 |
| 测试 | Vitest | 原生 TypeScript 支持，速度快，API 与 Jest 兼容 |
| 构建 | tsup | 零配置打包 TypeScript CLI 工具，输出单文件 |

## 2. 模块划分

### 2.1 技术模块定义

#### cli
- **职责**: 解析命令行参数，调用 task 模块完成业务操作，格式化输出结果
- **边界**: 只处理用户输入和输出格式化，不包含业务逻辑
- **对外接口**: 无（作为入口模块，不被其他模块调用）

#### task
- **职责**: 实现任务的增删改查业务逻辑，维护数据一致性
- **边界**: 不关心数据如何存储，不关心用户如何交互
- **对外接口**: `addTask(title)`, `listTasks(filter?)`, `completeTask(id)`, `deleteTask(id)`

#### storage
- **职责**: 读写 JSON 文件，提供数据持久化能力
- **边界**: 只负责文件的序列化/反序列化，不理解业务含义
- **对外接口**: `load(): TodoList`, `save(data: TodoList): void`

### 2.2 业务模块与技术模块映射

| 业务模块（PRD） | 技术模块 | 说明 |
|----------------|---------|------|
| 任务管理 | cli, task | cli 负责交互，task 负责逻辑 |
| 数据持久化 | storage | 1:1 直接对应 |

### 2.3 模块依赖关系

```
storage（无依赖）
  ↑
task（依赖 storage）
  ↑
cli（依赖 task）
```

### 2.4 共享层准入规则

types.ts 的准入标准：
- 只放被 2 个以上模块使用的类型定义
- 不放业务逻辑（业务逻辑应归属到具体业务模块 task/ 或 storage/）
- 模块内部专用的类型放在模块自己的文件中，不放入 types.ts

## 3. 目录结构

```
todo-cli/
├── CLAUDE.md
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── api-contracts.md
│   └── task-board.md
├── src/
│   ├── cli.ts              # 命令定义和入口
│   ├── task.ts             # 任务管理业务逻辑
│   ├── storage.ts          # JSON 文件读写
│   └── types.ts            # 共享类型定义
├── tests/
│   ├── cli.test.ts         # CLI 命令契约测试
│   ├── task.test.ts        # 任务管理契约测试
│   └── storage.test.ts     # 存储模块契约测试
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

| 目录/文件 | 用途 |
|-----------|------|
| src/ | 源代码，按模块组织为平铺文件（模块少，无需嵌套目录） |
| src/types.ts | 共享类型定义（Todo, TodoList, TaskFilter） |
| tests/ | 测试代码，与 src/ 中的模块一一对应 |
| docs/ | 项目文档 |

## 4. 数据模型

### Todo
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | number | 唯一，自增 | 任务 ID，从 1 开始 |
| title | string | 非空 | 任务标题 |
| status | "todo" \| "done" | 非空 | 任务状态 |
| createdAt | string (ISO 8601) | 非空 | 创建时间 |
| updatedAt | string (ISO 8601) | 非空 | 最后更新时间 |

### TodoList（存储文件结构）
```json
{
  "nextId": 4,
  "todos": [
    {
      "id": 1,
      "title": "买牛奶",
      "status": "done",
      "createdAt": "2026-03-28T10:00:00.000Z",
      "updatedAt": "2026-03-28T11:00:00.000Z"
    }
  ]
}
```

## 5. 关键设计决策

### 决策1: 使用 JSON 文件而非 SQLite
- **问题**: 任务数据需要持久化，选择什么存储方案
- **方案**: 使用 JSON 文件存储
- **理由**: 数据量小（个人 Todo 通常不超过几百条），JSON 文件无额外依赖，方便用户直接查看和备份，满足简单性要求

### 决策2: 平铺文件结构而非嵌套模块目录
- **问题**: 只有 3 个模块，是否需要按目录分隔
- **方案**: src/ 下直接放置模块文件，不再嵌套 modules/ 目录
- **理由**: 模块数量少，平铺更直观，减少目录层级；如果后续模块增多可以重构为目录结构

### 决策3: ID 使用自增整数而非 UUID
- **问题**: 任务 ID 的生成策略
- **方案**: 使用自增整数，在 TodoList 结构中维护 nextId 计数器
- **理由**: CLI 场景下用户需要手动输入 ID，短整数比 UUID 更易用
