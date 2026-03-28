# {项目名称} 架构文档

## 1. 技术选型

| 类别 | 选择 | 理由 |
|------|------|------|
| 语言 | {语言} | {理由} |
| 框架 | {框架} | {理由} |
| 数据库 | {数据库} | {理由} |
| 测试 | {测试框架} | {理由} |

## 2. 模块划分

### 2.1 技术模块定义

#### {模块A名称}
- **职责**: {这个模块负责什么}
- **边界**: {什么属于这个模块，什么不属于}
- **对外接口**: {暴露哪些 service 方法供其他模块调用}

#### {模块B名称}
- **职责**: {这个模块负责什么}
- **边界**: {什么属于这个模块，什么不属于}
- **对外接口**: {暴露哪些 service 方法供其他模块调用}

#### {模块C名称}
- **职责**: {这个模块负责什么}
- **边界**: {什么属于这个模块，什么不属于}
- **对外接口**: {暴露哪些 service 方法供其他模块调用}

### 2.2 业务模块与技术模块映射

| 业务模块（PRD） | 技术模块 | 说明 |
|----------------|---------|------|
| {业务模块A} | {技术模块名} | 1:1 直接对应 |
| {业务模块B} | {技术模块名1}, {技术模块名2} | 1:N，业务拆成了多个技术模块 |

### 2.3 模块依赖关系

```
{模块A}（无依赖）
  ↑
{模块B}（依赖 模块A）
  ↑
{模块C}（依赖 模块B）
```

### 2.4 共享层准入规则

shared/ 目录的准入标准：
- 只放被 **2 个以上模块** 使用的工具函数和类型定义
- 不放业务逻辑（业务逻辑应归属到具体业务模块）
- 每个文件 < 100 行，超过时应考虑拆分或归属到具体模块
- 新增 shared 内容时在 commit message 中说明被哪些模块使用

## 3. 目录结构

> 以下为常见技术栈的目录结构示例，请根据实际技术选型选择或调整。

**示例 A: Node.js + Express 后端**

```
src/
├── modules/
│   ├── {module-a}/
│   │   ├── {module-a}.controller.ts
│   │   ├── {module-a}.service.ts
│   │   ├── {module-a}.repository.ts
│   │   ├── {module-a}.types.ts
│   │   └── index.ts
│   └── {module-b}/
│       └── ...
├── shared/
│   ├── types/
│   └── utils/
├── infra/
│   ├── database.ts
│   └── config.ts
└── app.ts
```

| 目录 | 用途 |
|------|------|
| modules/ | 业务模块，每个模块独立目录 |
| shared/ | 跨模块共享的类型和工具 |
| infra/ | 基础设施（数据库、缓存、日志等） |

**示例 B: Next.js 全栈**

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── {module-a}/
│   │   └── page.tsx
│   ├── api/
│   │   ├── {module-a}/route.ts
│   │   └── {module-b}/route.ts
│   └── layout.tsx
├── components/
│   ├── ui/
│   └── {module-a}/
├── lib/
│   ├── {module-a}.service.ts
│   └── {module-b}.service.ts
├── db/
│   ├── schema.ts
│   └── index.ts
└── types/
```

| 目录 | 用途 |
|------|------|
| app/ | 页面路由和 API 路由 |
| components/ | UI 组件，按通用/模块分目录 |
| lib/ | 业务逻辑和服务层 |
| db/ | 数据库 schema 和连接 |

**示例 C: Python + FastAPI 后端**

```
src/
├── modules/
│   ├── {module_a}/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   └── models.py
│   └── {module_b}/
│       └── ...
├── shared/
│   ├── dependencies.py
│   └── utils.py
├── infra/
│   ├── database.py
│   └── config.py
└── main.py
```

| 目录 | 用途 |
|------|------|
| modules/ | 业务模块，每个模块含路由、服务、数据层 |
| shared/ | 共享依赖注入和工具函数 |
| infra/ | 数据库连接、配置管理 |

**示例 D: Go + Gin 后端**

```
cmd/
└── server/
    └── main.go
internal/
├── {module_a}/
│   ├── handler.go
│   ├── service.go
│   ├── repository.go
│   └── model.go
├── {module_b}/
│   └── ...
└── shared/
    ├── middleware/
    └── response/
pkg/
└── {可复用的公共库}/
config/
└── config.go
```

| 目录 | 用途 |
|------|------|
| cmd/ | 程序入口 |
| internal/ | 业务模块，不对外暴露 |
| pkg/ | 可复用的公共库 |
| config/ | 配置管理 |

**示例 E: Spring Boot 后端**

```
src/main/java/com/example/{project}/
├── modules/
│   ├── {modulea}/
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── dto/
│   │   └── entity/
│   └── {moduleb}/
│       └── ...
├── shared/
│   ├── config/
│   ├── exception/
│   └── util/
└── Application.java
```

| 目录 | 用途 |
|------|------|
| modules/ | 业务模块，每个模块含 controller/service/repository |
| shared/ | 全局配置、异常处理、工具类 |

## 4. 数据模型

### {模型A}
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | string (uuid) | PK | 主键 |
| {字段} | {类型} | {约束} | {说明} |
| createdAt | datetime | NOT NULL | 创建时间 |
| updatedAt | datetime | NOT NULL | 更新时间 |

### {模型B}
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | string (uuid) | PK | 主键 |
| {模型A}Id | string (uuid) | FK → {模型A}.id | 关联{模型A} |
| {字段} | {类型} | {约束} | {说明} |
| createdAt | datetime | NOT NULL | 创建时间 |
| updatedAt | datetime | NOT NULL | 更新时间 |

### 模型关系
```
{模型A} 1 ← N {模型B}（一个{模型A}对应多个{模型B}）
```

## 5. 关键设计决策

### 决策1: {标题}
- **问题**: {要解决什么}
- **方案**: {选了什么}
- **理由**: {为什么}
