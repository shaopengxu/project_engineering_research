# Module: {模块名称}

## 职责
{一句话描述这个模块负责什么}

## 依赖的模块
- shared: 使用 {列出具体函数/类型，如 formatDate, validateId}
- {module-x}: 调用 {具体接口，如 OrderService.getByUserId}（接口定义见 docs/api-contracts-{module-x}.md）

## 被依赖的模块
- {module-y}: 调用本模块的 {具体接口，如 UserService.getById}
- {module-z}: 调用本模块的 {具体接口}

## 当前模块的接口文档
docs/api-contracts-{module}.md

## 当前模块的设计文档
docs/module-design/{module}.md

## 模块内目录结构
```
src/modules/{module}/
├── controller.ts      # 请求处理 / 参数校验
├── service.ts         # 业务逻辑
├── repository.ts      # 数据访问
├── types.ts           # 模块内类型定义
└── index.ts           # 对外导出
```

## 模块特有的约定
- {约定1: 如本模块特有的安全规范}
- {约定2: 如本模块特有的数据处理规则}
