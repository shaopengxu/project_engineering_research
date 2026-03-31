# 模块详细设计: {模块名称}

> 本文档描述 {模块名称} 前端模块的整体架构。各 feature 的页面细节见 `{模块名称}-{feature}.md`。
> 系统级架构见 architecture.md。

## 1. 模块概述

- **职责**: {一句话描述}
- **类型**: 前端模块
- **业务模块映射**: PRD 中的 {对应业务模块名}

---

## 2. Feature 划分

| Feature | 包含页面 | 对应后端模块 | 说明 |
|---------|---------|------------|------|
| {feature-a} | {页面列表} | {module-x} | {划分依据} |
| {feature-b} | {页面列表} | {module-y} | {划分依据} |

**划分原则**: {说明 feature 划分与后端模块的对应关系，以及划分依据}

---

## 3. 内部架构

### 目录结构

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

### 控制流

```
用户操作 → Page → Hook（useQuery/useMutation）→ API 层（fetch）→ TanStack Query 缓存更新 → 重新渲染
```

---

## 4. 路由结构

| 路由 | 页面组件 | 所属 Feature | 功能描述 | 认证要求 |
|------|---------|-------------|---------|---------|
| /path-a | PageA | {feature-a} | {一句话描述} | {需要 / 不需要} |
| /path-b | PageB | {feature-b} | {一句话描述} | {需要 / 不需要} |
| /path-a/:id | PageADetail | {feature-a} | {一句话描述} | {需要 / 不需要} |

---

## 5. 布局设计

### 全局布局

```
{描述全局布局结构，如:}
AppLayout
├── Header             # 顶部导航栏（logo、用户信息、退出）
├── Sidebar            # 侧边菜单（如有）
└── Content            # 页面内容区域
```

### 导航结构

| 菜单项 | 路由 | 图标 | 权限要求 |
|--------|------|------|---------|
| {菜单项} | /path-a | {图标} | {权限} |

---

## 6. 共享层设计

### 共享组件

| 组件 | 用途 | 使用方 |
|------|------|--------|
| {ComponentName} | {一句话描述} | {哪些 feature 使用} |

### 共享 Hooks

| Hook | 用途 | 使用方 |
|------|------|--------|
| {useHookName} | {一句话描述，如: 获取当前登录用户信息} | {哪些 feature 使用} |

### 全局状态管理（Zustand）

| Store | 状态 | 用途 | 使用方 |
|-------|------|------|--------|
| {storeName} | {状态字段} | {一句话描述} | {哪些 feature 使用} |

### API Client 配置

- **基础 URL**: {如 /api}
- **请求拦截器**: {如 自动附加 Authorization header}
- **响应拦截器**: {如 统一错误处理、401 跳转登录}
- **错误处理**: {如 toast 提示、表单错误回填}

---

## 7. 核心类型定义

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

---

## 8. 模块特有约定

- {约定1: 如响应式要求}
- {约定2: 如浏览器兼容要求}
- {约定3: 如性能约束}
