# Todo CLI 任务看板

> 更新规则：由技术负责人统一更新，避免多人同时编辑冲突。Agent 完成任务后在会话中报告状态，由技术负责人同步到此文件。

## 项目阶段

| Step | 状态 | 备注 |
|------|------|------|
| 1 初始化 | 已完成 | |
| 2 架构设计 | 已完成 | |
| 3 任务拆分 | 已完成 | |
| 4 契约测试 | 未开始 | |
| 5 实现 + Review | 未开始 | |
| 6 E2E 测试 | 未开始 | |
| 7 验收 | 未开始 | |

## 进度总览

| 模块 | 测试 | 实现 | Review |
|------|------|------|--------|
| storage | 未开始 | 未开始 | 未开始 |
| task | 未开始 | 未开始 | 未开始 |
| cli | 未开始 | 未开始 | 未开始 |

## 契约测试任务（按模块划分）

> 契约测试由 Tester agent 在实现之前编写，验证接口的输入输出是否符合 api-contracts.md 的定义。
> 单元测试和集成测试由 Implementer agent 在实现过程中按需补充，不在此处规划。

### storage

- [ ] **Test-001**: storage 模块 load/save 测试
  - 对应契约: api-contracts.md#storage 模块内部接口
  - 测试文件: tests/storage.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

### task

- [ ] **Test-002**: addTask 业务逻辑测试
  - 对应契约: api-contracts.md#todo add
  - 测试文件: tests/task.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-003**: listTasks 业务逻辑测试
  - 对应契约: api-contracts.md#todo list
  - 测试文件: tests/task.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-004**: completeTask 业务逻辑测试
  - 对应契约: api-contracts.md#todo done
  - 测试文件: tests/task.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-005**: deleteTask 业务逻辑测试
  - 对应契约: api-contracts.md#todo delete
  - 测试文件: tests/task.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

### cli

- [ ] **Test-006**: CLI 命令解析和输出格式测试
  - 对应契约: api-contracts.md#任务管理命令
  - 测试文件: tests/cli.test.ts
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

> 测试 review：技术负责人在所有测试任务完成后统一 review，确认后进入实现阶段。

## 实现任务（按技术模块划分）

### storage

- [ ] **Impl-001**: 实现 JSON 文件读写
  - 涉及文件: src/storage.ts, src/types.ts
  - 需通过测试: Test-001
  - 依赖: 无
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

### task

- [ ] **Impl-002**: 实现任务增删改查业务逻辑
  - 涉及文件: src/task.ts
  - 需通过测试: Test-002, Test-003, Test-004, Test-005
  - 依赖: Impl-001
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

### cli

- [ ] **Impl-003**: 实现 CLI 命令定义和输出格式化
  - 涉及文件: src/cli.ts
  - 需通过测试: Test-006
  - 依赖: Impl-002
  - 开始时间:
  - 完成时间:
  - 状态: 未开始
  - 阻塞原因:

## E2E 测试任务（Step 6 时填写）

> Step 5 所有实现任务 Review 通过后填写。根据 PRD 验收标准拆分 E2E 测试用例。

（待 Step 5 完成后补充）

## 项目事件记录

> 记录 Task 完成、Review 迭代、架构修订、回退等关键事件。

| 时间 | 事件 | 备注 |
|------|------|------|
| | | |
