# 测试策略

## 测试分层

### 后端模块测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| 契约测试 | Tester agent | Step 5（模块实现前） | module-design/{module}.md 接口契约 | 必须 |
| 单元测试 | Implementer agent | Step 5（实现中） | 复杂内部逻辑 | 按需 |
| L1 模块内集成 | Implementer agent | Step 5（实现中） | controller → service → repository 串联 | **必须** |
| L2 关键路径集成 | Implementer agent | Step 5（模块完成后独立会话） | 跨模块真实调用 | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |

### 前端模块测试分层

| 测试层级 | 谁写 | 什么时候 | 依据 | 是否必须 |
|---------|------|---------|------|---------|
| API 调用层测试 | Tester agent | Step 5（feature 实现前） | web-app-{feature}.md 中"调用的后端接口" | 必须 |
| 页面渲染测试 | Tester agent | Step 5（feature 实现前） | web-app-{feature}.md 中"页面与路由" | 必须 |
| 页面集成测试 | Implementer agent | Step 5（实现中） | 页面 → hooks → API 层串联（mock 后端） | **必须** |
| E2E 测试 | Tester agent | Step 6 | PRD 验收标准 | 核心路径必须 |

> **前端契约测试说明**：前端的"契约测试"等价物是 API 调用层测试 + 页面渲染测试。API 调用层测试验证请求参数和响应处理与 module-design 中后端接口定义一致；页面渲染测试验证页面组件能正确渲染 mock 数据并响应用户交互。

## Mock 策略

### 后端

| 测试层级 | 模块间依赖 | 外部依赖（数据库、第三方 API） |
|---------|-----------|---------------------------|
| 契约测试 | Mock / Stub | Mock（内存数据库可替代） |
| 单元测试 | Mock / Stub | Mock |
| L1 模块内集成 | Mock 其他模块 | 真实连接或测试容器 |
| L2 跨模块集成 | **真实调用** | 真实连接或测试容器 |
| E2E 测试 | **真实调用** | 真实连接 |

### 前端

| 测试层级 | 后端 API | 浏览器环境 |
|---------|---------|-----------|
| API 调用层测试 | Mock（MSW 或手动 mock） | jsdom |
| 页面渲染测试 | Mock（MSW 或手动 mock） | jsdom |
| 页面集成测试 | Mock（MSW 或手动 mock） | jsdom |
| E2E 测试 | **真实调用** | 真实浏览器（Playwright） |

## L2 集成测试的触发时机

当模块 B 依赖模块 A，且模块 A 已实现完成：

1. 模块 B 完成所有 Task 和模块级 Review 后，开独立会话编写跨模块集成测试
2. 使用真实的模块 A（不 Mock）
3. 串行开发天然保证被依赖模块先完成，无需额外协调

## infra 模块说明

infra 是技术基础设施模块，不属于业务模块，因此不走契约测试流程。

**infra 包含的内容**：
- 数据库连接和 Prisma Client 初始化
- 配置管理（环境变量加载）
- 全局错误处理中间件
- 标准响应格式工具函数
- 通用中间件（认证、日志等）

**infra 的验收标准**：
- 依赖安装成功，lint 通过
- 数据库连接成功（开发环境和测试环境）
- 错误处理中间件能正确捕获和格式化错误
- 标准响应格式工具函数可用
- 所有后续模块可以正常导入和使用 infra 提供的功能

## 测试目录结构

```
tests/
├── contracts/              # 契约测试（按模块组织）
│   ├── module-a/
│   ├── module-b/
│   └── web-app/            # 前端按 feature 组织
│       ├── {feature-a}/
│       └── {feature-b}/
├── unit/                   # 单元测试（按模块组织）
├── integration/            # 集成测试
│   ├── module-a/           # L1: 模块内集成
│   ├── module-b/
│   └── paths/              # L2: 关键路径集成
│       ├── order-payment-flow.test.ts
│       └── user-order-flow.test.ts
├── e2e/                    # E2E 测试（按用户流程）
└── fixtures/               # 共享测试数据（工厂函数，非硬编码）
```

## 契约测试预期状态

测试代码能编译/加载，但执行时全部失败（因为实现不存在）— 这是 TDD 的正常状态（先红后绿）。强类型语言通过 Step 4 的导出桩文件解决编译问题。
