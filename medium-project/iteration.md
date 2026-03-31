# 迭代管理

## 何时需要多迭代

- 4-5 个模块：通常 1 个迭代
- 6-8 个模块：建议 2-3 个迭代
- 判断标准：模块间有明确的优先级差异，或产品经理希望尽早验证核心流程

## 迭代划分

使用 **GitHub Milestones** 管理迭代：

```
Milestone 1: 核心模块
  后端: infra + user + product
  前端: web-app（auth feature + product feature）
  → Step 2-7 完整走一遍
  → 实现顺序: infra → user → product → web-app（相关页面）
  → 产品经理验收核心流程

Milestone 2: 交易模块
  后端: order + payment + inventory
  前端: web-app（order feature）+ admin（订单管理页面）
  → Step 2（增量：只设计新模块，review 对已有模块的影响）→ Step 4-7
  → 实现顺序: inventory → order → payment → web-app（新页面）→ admin
  → 产品经理验收交易流程

Milestone 3: 辅助模块
  后端: notification + coupon + analytics
  前端: admin（剩余管理页面）
  → 同上（增量模式）
  → 最终全量验收
```

> **前端模块时序**：每个迭代内，前端模块在其依赖的后端模块全部完成后再实现。前端按 feature 拆分设计文档和测试，每个迭代只设计和实现与本迭代后端模块对应的 feature，不必等所有后端模块完成。

## 迭代间的关系

- 后续迭代的 Step 2 只设计本迭代新增模块，但必须 review 对已有模块的影响
- 已有模块的接口如需变更，按变更传播规则处理
- 每个迭代结束时保持 main 可部署

## 增量开发（已有项目加新功能）

| 场景 | 起始步骤 | 说明 |
|------|---------|------|
| 新增业务模块 | Step 2（评估对现有架构影响） | 更新 architecture.md 依赖图，然后 3 → 4 → ... |
| 已有模块增加接口 | Step 3（更新 module-design/{module}.md） | 同时更新 architecture.md 依赖矩阵 |
| 跨多模块的新功能 | Step 2（影响评估） | 查接口依赖矩阵确定影响范围 → 3 → 5 |
| 模块内重构不改接口 | Step 5（实现阶段） | 契约测试不需要改（接口没变） |
| 修 bug | 不走流程 | 直接改 + 补测试 + 提交 |

关键原则：**变了什么文档，就从那个文档对应的步骤开始往后走。** 改了接口 → 从契约测试开始更新；只改实现 → 直接进入实现阶段。
