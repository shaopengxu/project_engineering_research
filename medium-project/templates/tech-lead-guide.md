# 技术负责人操作指南（中型项目）

## Skill 速查

| Step | Skill | 参数 |
|------|-------|------|
| 2. 系统架构 | `/mp-architecture` | — |
| 3. 模块设计 | `/mp-module-design` | `<module> [feature]` / `--summary` |
| 4a. 脚手架 | `/mp-scaffold` | — |
| 4b. 任务拆分 | `/mp-task-split` | — |
| 5a. infra 实现 | `/mp-impl-infra` | `<issue-number>` |
| 5b. 后端契约测试 | `/mp-test-contract` | `<module> <issue-number>` |
| 5b. 前端测试 | `/mp-test-frontend` | `<module> <feature> <issue-number>` |
| 5c. 实现 Task | `/mp-impl` | `<module> <issue-number> [feature]` |
| 5d. Task Review | `/mp-review-task` | `<module> <issue-number>` |
| 5e. Review 修复 | `/mp-review-fix` | `<module> <issue-number>` |
| 5f. 模块 Review | `/mp-review-module` | `<module>` |
| 5g. L2 集成测试 | `/mp-test-integration` | `<issue-number>` |
| 6. E2E 测试 | `/mp-test-e2e` | — |

所有 skill 均以 `context: fork` 运行，无需手动开新会话。

---

## Review 指南

### Review 深度分级

| Task 类型 | Review 深度 | 重点关注 |
|-----------|-----------|---------|
| 基础设施（infra） | 快速扫描 | 配置正确、依赖合理、能跑通 |
| 核心业务模块 | 逐条对照契约 | 业务规则覆盖、错误处理、边界条件 |
| 跨模块交互 | 重点检查 | 依赖方向、接口一致性、数据流转 |
| 模块级 Review | 一致性检查 | 命名风格、错误处理方式、职责分层 |

**可"信任 Agent + 测试"的场景**：简单 CRUD、测试全部通过且 Agent 未报告异常。
**必须人工逐行过的场景**：安全相关、复杂业务规则、跨模块数据一致性。

### Step 2 架构 Review Checklist

```
- [ ] 模块划分符合单一职责，每个模块职责一句话说清
- [ ] 模块间依赖方向单向，无循环依赖
- [ ] 业务模块数量在 4-8 个（过多需拆迭代、过少则本流程过重）
- [ ] 关键业务路径的数据流完整
- [ ] infra 职责边界明确
- [ ] 跨模块数据关系清晰（关联管理方、外键策略）
- [ ] 架构决策有理由说明
- [ ] 接口通用约定已定义（认证、响应格式、分页、状态码）
- [ ] 部署概要已说明（如影响模块设计）
```

### Step 3 模块设计 + 接口契约 Review Checklist

```
模块设计：
- [ ] 内部分层符合 architecture.md 约定
- [ ] 数据模型完整（字段、类型、约束）
- [ ] 公开接口清单与 architecture.md 一致
- [ ] 消费的外部接口在依赖关系中有体现
- [ ] 关键业务逻辑有详细说明（状态机、计算规则等）
- [ ] 没有设计其他模块的内容

接口契约（每个模块完成后检查）：
- [ ] 每个接口都有完整的五要素（输入、输出、业务规则、错误码、consumers）
- [ ] 接口签名与 module-design 中"公开接口清单"一致
- [ ] 错误码全局不重复（与已有模块不冲突）
- [ ] 接口风格与已有模块一致（遵循通用约定）

所有模块完成后检查：
- [ ] 需求追溯表中列出了 PRD 的每条业务规则和验收标准（无遗漏）
- [ ] 每一行的"对应契约章节"都已填写（不允许为空）
- [ ] 抽查 3-5 条：翻到对应契约章节，确认规则完整描述
- [ ] 接口依赖矩阵完整，覆盖所有跨模块调用
```

### Step 4 脚手架 + Issues Review Checklist

```
脚手架：
- [ ] 依赖安装成功
- [ ] lint 命令能跑通
- [ ] 测试框架能启动
- [ ] 后端模块导出桩文件存在且函数签名与 module-design 中的接口契约一致
- [ ] .env.example 已创建，.env 已加入 .gitignore
- [ ] TypeScript 配置正确（根目录 + 各端独立 tsconfig）

GitHub Issues：
- [ ] 每个接口都有对应的契约测试 Issue
- [ ] 每个实现 Issue 标注了依赖（Depends on #N）
- [ ] 每个实现 Issue 标注了需通过的测试
- [ ] 共享层任务优先级最高
- [ ] 关键路径有 L2 集成测试 Issue
- [ ] Issues 按依赖顺序可串行推进
- [ ] 标签（type + module）正确
```

### Step 5 测试 Review Checklist

```
- [ ] 每条业务规则有对应测试用例（对照 module-design 接口契约逐条检查）
- [ ] 覆盖正常流程和异常流程（错误码全覆盖）
- [ ] 测试独立（无共享状态、不依赖执行顺序）
- [ ] 测试注释标注了业务规则来源
- [ ] Mock/Stub 使用符合 workflow.md Mock 策略
- [ ] 测试能编译/加载（允许执行失败）
```

### Step 5 Task 流转管理

```
每个 Task Review 通过后：
- [ ] 更新 GitHub Issue 状态（关闭 Issue 或移动到 Done）
- [ ] 检查是否解锁了下游依赖任务
- [ ] 如果涉及文档变更，按变更传播规则处理
- [ ] 如果模块所有 Task 完成，触发模块级 Review

模块完成时：
- [ ] 确认该模块所有 Task 已完成
- [ ] 触发模块级 Review
- [ ] 如有跨模块依赖且被依赖模块已完成，触发 L2 集成测试（独立会话）
- [ ] 跑全量测试确认无回归
```

### infra 变更处理

```
收到 Agent 的 infra 变更请求时：
1. 评估需求，确认后允许修改
2. 修改后确认：
   - [ ] 不影响已有模块
   - [ ] 后续 Task 自动使用最新代码
```

### 接口变更处理

```
收到 Agent 的接口变更请求时：
1. 查看 architecture.md 的接口依赖矩阵，确定消费方
2. 评估变更影响：
   - [ ] 变更是否向后兼容？
   - [ ] 影响了哪些模块的契约测试？
   - [ ] 影响了哪些模块的已完成实现？
3. 更新文档：
   - [ ] 更新提供方的 module-design/{module}.md 接口契约
   - [ ] 更新消费方的 module-design 中的"消费的外部接口"
   - [ ] 同步更新 architecture.md 的接口依赖矩阵（如影响范围变化）
4. 通知受影响模块：
   - [ ] 在受影响模块的 Issue 中 comment 变更通知
   - [ ] 后续 Task 使用最新文档
5. 按变更传播规则执行：文档 → 测试 → 实现
```
