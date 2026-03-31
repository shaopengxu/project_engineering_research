# 模块详细设计: {模块名称}

> 本文档描述 {模块名称} 模块的内部设计和接口契约。系统级架构见 architecture.md。
>
> **前端模块文档拆分**：前端模块（如 web-app）拆为整体文档 + feature 级文档：
> - `web-app.md`（整体）：路由结构、布局、共享状态、共享组件、通用约定
> - `web-app-{feature}.md`（逐 feature）：该 feature 的页面、交互流程、调用的后端接口
>
> 后端模块每个模块一个文件，不拆分。

## 1. 模块概述

- **职责**: {一句话描述}
- **类型**: {后端模块 / 前端模块}
- **业务模块映射**: PRD 中的 {对应业务模块名}

---

## 2. 内部架构

> 根据模块类型选择对应的架构描述。

### 后端模块

#### 分层结构

```
{module}/
├── controller.ts      # 请求处理、参数校验、响应格式化
├── service.ts         # 业务逻辑、规则执行
├── repository.ts      # 数据访问、SQL/查询封装
├── types.ts           # 模块内类型定义
└── index.ts           # 对外导出（公开接口）
```

| 层 | 职责 | 依赖 |
|----|------|------|
| Controller | 接收请求、参数校验、调用 Service、格式化响应 | Service |
| Service | 业务逻辑、业务规则执行、跨层编排 | Repository, 其他模块的 Service（通过接口） |
| Repository | 数据库操作、Prisma 查询封装 | Prisma Client（infra） |

#### 控制流

```
请求 → Controller（校验）→ Service（业务逻辑）→ Repository（数据访问）→ 响应
```

### 前端模块

#### 目录结构

```
{module}/
├── features/          # 按业务域组织
│   ├── {feature-a}/
│   │   ├── pages/             # 页面组件
│   │   ├── components/        # feature 私有组件
│   │   ├── hooks/             # feature 私有 hooks
│   │   └── api/               # feature 私有 API 调用
│   └── {feature-b}/
│       └── ...
├── shared/            # 共享组件、hooks、工具函数、类型
├── stores/            # 全局状态管理（跨 feature 共享）
├── routes.ts          # 统一路由
└── main.tsx
```

| 层 | 职责 | 依赖 |
|----|------|------|
| Pages | 页面组件（React Router 路由对应），组合子组件 | Components, Hooks |
| Components | Ant Design 基础上的业务组件，只接收 props，不直接调用 API | — |
| Hooks | TanStack Query 数据获取 + 业务逻辑封装 | API, Stores |
| API | 封装后端接口调用（axios / fetch），处理请求/响应转换 | 后端模块接口 |
| Stores | Zustand 跨页面共享状态（仅在需要时使用） | — |

#### 控制流

```
用户操作 → Page → Hook（useQuery/useMutation）→ API 层（fetch）→ TanStack Query 缓存更新 → 重新渲染
```

---

## 3. 数据模型

> 后端模块填数据库模型，前端模块填核心状态/类型定义。

### 后端模块

#### {模型A}

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | string (uuid) | PK | 主键 |
| {字段} | {类型} | {约束} | {说明} |
| createdAt | datetime | NOT NULL | 创建时间 |
| updatedAt | datetime | NOT NULL | 更新时间 |

#### 模型关系
```
{模型A} 1 ← N {模型B}（一个{模型A}对应多个{模型B}）
```

#### 与其他模块数据的关系
- {模型A}.{外键字段} → {其他模块.模型}.id（通过接口调用访问，不直接访问其他模块的表）

### 前端模块

#### 核心类型定义

```typescript
// 与后端接口对应的数据类型
interface {TypeA} {
  id: string;
  {field}: {type};  // {说明}
}

// 页面/组件状态类型
interface {PageState} {
  {field}: {type};  // {说明}
}
```

#### 状态管理

| 状态 | 作用域 | 存储方式 | 说明 |
|------|--------|---------|------|
| {状态名} | 页面内 | useState / useReducer | {说明} |
| {状态名} | 跨页面 | Zustand store | {说明} |
| {状态名} | 服务端数据 | TanStack Query | {说明，自动缓存/刷新} |
| {状态名} | 持久化 | localStorage | {说明，如用户偏好} |

---

## 4. 接口契约

> 根据模块类型选择对应的契约描述。

### 后端模块 — 提供的接口

> 每个接口必须包含五要素：**输入、输出、业务规则、错误码、consumers**。
> 接口通用约定（认证方式、响应格式、分页、HTTP 状态码）见 architecture.md。

#### {接口名称}

`{METHOD} {path}`

**描述**: {这个接口做什么}

**认证**: {需要 / 不需要}

**Consumers**: {列出调用此接口的模块，如: module-b, web-app；无外部消费方则标注"仅内部"}

**Request Body**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| field1 | string | 是 | {描述} |
| field2 | number | 否 | {描述，默认值: {默认值}} |

**Response 200**:
```json
{
  "data": {
    "id": "string",
    "field1": "string"
  }
}
```

**业务规则**:
- {规则1}
- {规则2}

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_FIELD1 | field1 格式不合法 |
| 409 | DUPLICATE_FIELD1 | field1 已存在 |

---

#### 内部接口（跨模块 Service 调用）

> 非 HTTP 暴露的接口。用于其他模块的 Service 层直接调用本模块的 Service。

##### {ServiceName}.{methodName}

**描述**: {这个方法做什么}

**Consumers**: {module-b, module-c}

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| param1 | string | 是 | {描述} |

**返回值**:
```typescript
{ id: string, field1: string }
```

**业务规则**:
- {规则1}

**错误码**:
| error.code | 触发条件 |
|-----------|---------|
| NOT_FOUND | 资源不存在 |

### 前端模块 — 页面与路由

| 路由 | 页面组件 | 功能描述 | 调用的后端接口 |
|------|---------|---------|--------------|
| /path-a | PageA | {一句话描述} | GET /api/xxx, POST /api/yyy |
| /path-b | PageB | {一句话描述} | GET /api/zzz |
| /path-a/:id | PageADetail | {一句话描述} | GET /api/xxx/:id, PUT /api/xxx/:id |

#### {PageA} 页面

**功能**: {这个页面做什么}

**页面状态**:
| 状态 | 类型 | 来源 | 说明 |
|------|------|------|------|
| {state} | {type} | API / 用户输入 | {说明} |

**调用的后端接口**:
| 接口 | 触发时机 | 成功处理 | 错误处理 |
|------|---------|---------|---------|
| GET /api/xxx | 页面加载 | 渲染列表 | 显示错误提示 |
| POST /api/yyy | 表单提交 | 跳转/刷新 | 显示表单错误 |

**交互流程**:
```
用户打开页面 → 加载数据（GET /api/xxx）→ 渲染列表
用户点击创建 → 弹出表单 → 填写 → 提交（POST /api/yyy）→ 成功后刷新列表
```

**组件结构**:
```
PageA
├── SearchBar          # 搜索/筛选
├── DataTable          # 数据列表
│   └── TableRow       # 单行
├── CreateModal        # 创建弹窗
└── Pagination         # 分页
```

---

## 5. 消费的外部接口

> 后端模块填其他后端模块的接口，前端模块填调用的后端 API 汇总。

| 接口 | 提供方 | 调用场景 |
|------|--------|---------|
| {接口名} | {module-x} | {什么时候调用、为什么需要} |

## 6. 关键业务逻辑

### {逻辑1: 如状态流转 / 表单校验规则 / 权限控制}
{详细描述复杂业务逻辑}

## 7. 模块特有约定

- {约定1: 如本模块的安全要求}
- {约定2: 如本模块的性能约束}
- {约定3: 如本模块的错误处理策略}

## 8. 已知限制和 TODO

- {限制1: 如当前版本不支持 XXX}
- {TODO: 如后续需要支持 XXX}
