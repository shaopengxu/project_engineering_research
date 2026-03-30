# {项目名称} 系统架构文档

> 本文档只描述**系统级**架构：模块划分、依赖关系、跨模块数据流、部署概要。
> 每个模块的内部设计见 module-design/{module}.md。

## 1. 技术选型

| 类别 | 选择 | 理由 |
|------|------|------|
| 语言 | {语言} | {理由} |
| 框架 | {框架} | {理由} |
| 数据库 | {数据库} | {理由} |
| 测试 | {测试框架} | {理由} |
| 其他 | {如消息队列、缓存等} | {理由} |

## 2. 模块划分

### 2.1 模块总览

| 模块 | 类型 | 职责（一句话） |
|------|------|--------------|
| shared | 技术模块 | 跨模块共享的类型定义和工具函数 |
| infra | 技术模块 | 基础设施（数据库、配置、错误处理、响应格式） |
| {module-a} | 业务模块 | {职责} |
| {module-b} | 业务模块 | {职责} |
| {module-c} | 业务模块 | {职责} |
| ... | ... | ... |

### 2.2 业务模块与 PRD 映射

| 业务模块（PRD） | 技术模块 | 说明 |
|----------------|---------|------|
| {PRD模块A} | {module-a} | 1:1 直接对应 |
| {PRD模块B} | {module-b}, {module-c} | 1:N，拆分为两个技术模块，因为 {原因} |

### 2.3 模块定义

#### shared
- **职责**: 跨模块共享的类型和工具
- **准入规则**: 只放被 2 个以上模块使用的代码；不放业务逻辑；每个文件 < 100 行
- **修改权限**: 仅技术负责人审批后修改（业务模块开发期间）

#### infra
- **职责**: 数据库连接、配置管理、全局错误处理、标准响应格式
- **修改权限**: 同 shared

#### {module-a}
- **职责**: {一句话描述}
- **边界**: {什么属于这个模块，什么不属于}
- **对外接口**: {列出暴露的关键接口名称}
- **详细设计**: module-design/{module-a}.md

#### {module-b}
- **职责**: {一句话描述}
- **边界**: {什么属于这个模块，什么不属于}
- **对外接口**: {列出暴露的关键接口名称}
- **详细设计**: module-design/{module-b}.md

{... 每个模块一节}

## 3. 模块依赖关系

### 3.1 依赖关系图

```
shared + infra
  ↑    ↑    ↑    ↑
{module-a}  {module-b}  {module-c}  {module-d}
              ↑            ↑
              └── {module-e}（依赖 module-b + module-c）
```

### 3.2 依赖规则

- 所有业务模块依赖 shared + infra（省略不画）
- 业务模块间依赖方向**单向**，禁止循环
- 当出现双向需求时，使用事件通知 / 回调 / 中间模块解耦（记录到 decision-log.md）

### 3.3 依赖矩阵

| 模块 | 依赖（调用方） | 被依赖（提供方） |
|------|-------------|----------------|
| {module-a} | shared, infra | {module-c}, {module-e} |
| {module-b} | shared, infra | {module-e} |
| {module-c} | shared, infra, {module-a} | {module-e} |
| {module-d} | shared, infra | 无 |
| {module-e} | shared, infra, {module-b}, {module-c} | 无 |

## 4. 跨模块数据流

### 4.1 关键业务路径

**路径 1: {路径名称，如"下单流程"}**

```
用户请求 → {module-a}.Controller
  → {module-a}.Service 校验参数
  → 调用 {module-b}.Service.{method}（扣减库存）
  → 调用 {module-c}.Service.{method}（创建支付单）
  → 返回订单结果
```

**路径 2: {路径名称}**

```
{描述另一条关键路径}
```

### 4.2 事件流（如有异步通信）

| 事件 | 发布方 | 消费方 | 触发条件 | 处理逻辑 |
|------|--------|--------|---------|---------|
| {事件名} | {module-a} | {module-b} | {什么时候触发} | {消费方做什么} |

## 5. 目录结构

> 以下为常见技术栈的目录结构示例，根据实际技术选型选择或调整。

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
│   ├── {module-b}/
│   │   └── ...
│   └── shared/
│       ├── CLAUDE.md
│       ├── types/
│       └── utils/
├── infra/
│   ├── database.ts
│   ├── config.ts
│   ├── error-handler.ts
│   └── response.ts
└── app.ts
```

**示例 B: Python + FastAPI 后端**

```
src/
├── modules/
│   ├── {module_a}/
│   │   ├── CLAUDE.md
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   └── models.py
│   ├── {module_b}/
│   │   └── ...
│   └── shared/
│       ├── CLAUDE.md
│       ├── dependencies.py
│       └── utils.py
├── infra/
│   ├── database.py
│   └── config.py
└── main.py
```

**示例 C: Go + Gin 后端**

```
cmd/
└── server/
    └── main.go
internal/
├── {module_a}/
│   ├── CLAUDE.md
│   ├── handler.go
│   ├── service.go
│   ├── repository.go
│   └── model.go
├── {module_b}/
│   └── ...
└── shared/
    ├── CLAUDE.md
    ├── middleware/
    └── response/
config/
└── config.go
```

## 6. 数据模型概览

> 只列出跨模块关系的数据模型。模块内部的数据模型详见 module-design/{module}.md。

### 模型关系总览

```
{模型A} 1 ← N {模型B}（一个{模型A}对应多个{模型B}）
{模型B} N ← M {模型C}（多对多，通过 {关联表} 关联）
{模型D} 1 ← 1 {模型A}（一对一）
```

### 跨模块数据关系

| 关系 | 模型A（模块） | 模型B（模块） | 关系类型 | 关联管理方 |
|------|-------------|-------------|---------|----------|
| {关系名} | {模型}（{module-a}） | {模型}（{module-b}） | 1:N | {module-b}（通过接口调用获取 module-a 数据） |
| {关系名} | {模型}（{module-b}） | {模型}（{module-c}） | N:M | {module-c}（管理关联表） |

### 关键约束
- {约束1: 如外键行为（ON DELETE CASCADE / SET NULL / RESTRICT）}
- {约束2: 如唯一约束}
- {约束3: 如跨模块数据一致性保证策略（事务 / 最终一致 / 补偿）}

## 7. 关键架构决策

> 简要记录此处。如果决策复杂或后续有变更，在 decision-log.md 中创建完整 ADR 记录。

### 决策1: {标题}
- **问题**: {要解决什么}
- **方案**: {选了什么}
- **理由**: {为什么}

### 决策2: {标题}
- **问题**: {要解决什么}
- **方案**: {选了什么}
- **理由**: {为什么}

## 8. 部署概要（可选）

> 小规模中型项目可省略此节。如果部署架构影响模块设计（如前后端分离、微服务拆分预留），则需要说明。

- **部署方式**: {单体 / 前后端分离 / 其他}
- **运行环境**: {如 Docker / 云平台 / VPS}
- **数据库部署**: {与应用同机 / 独立实例 / 托管服务}
