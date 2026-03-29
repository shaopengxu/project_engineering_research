# Bookmark API 任务看板

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
| shared + infra | — | 未开始 | 未开始 |
| bookmark | 未开始 | 未开始 | 未开始 |
| tag | 未开始 | 未开始 | 未开始 |

## 契约测试任务（按接口划分）

> 契约测试由 Tester agent 在实现之前编写，验证接口的输入输出是否符合 api-contracts.md 的定义。
> 单元测试和集成测试由 Implementer agent 在实现过程中按需补充，不在此处规划。

### bookmark

- [ ] **Test-001**: POST /bookmarks 添加书签测试
  - 对应契约: api-contracts.md#添加书签
  - 测试文件: tests/bookmark/bookmark-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-002**: GET /bookmarks 查询书签列表测试
  - 对应契约: api-contracts.md#查询书签列表
  - 测试文件: tests/bookmark/bookmark-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-003**: GET /bookmarks/:id 查看书签详情测试
  - 对应契约: api-contracts.md#查看书签详情
  - 测试文件: tests/bookmark/bookmark-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-004**: PUT /bookmarks/:id 更新书签测试
  - 对应契约: api-contracts.md#更新书签
  - 测试文件: tests/bookmark/bookmark-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-005**: DELETE /bookmarks/:id 删除书签测试
  - 对应契约: api-contracts.md#删除书签
  - 测试文件: tests/bookmark/bookmark-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-006**: POST /bookmarks/:id/tags 给书签添加标签测试
  - 对应契约: api-contracts.md#给书签添加标签
  - 测试文件: tests/bookmark/bookmark-tag.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-007**: DELETE /bookmarks/:id/tags/:tagId 移除书签的标签测试
  - 对应契约: api-contracts.md#移除书签的标签
  - 测试文件: tests/bookmark/bookmark-tag.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

### tag

- [ ] **Test-008**: POST /tags 创建标签测试
  - 对应契约: api-contracts.md#创建标签
  - 测试文件: tests/tag/tag-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-009**: GET /tags 查询所有标签测试
  - 对应契约: api-contracts.md#查询所有标签
  - 测试文件: tests/tag/tag-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Test-010**: DELETE /tags/:id 删除标签测试
  - 对应契约: api-contracts.md#删除标签
  - 测试文件: tests/tag/tag-crud.test.ts
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

> 测试 review：技术负责人在所有测试任务完成后统一 review，确认后进入实现阶段。

## 实现任务（按技术模块划分）

### shared + infra

- [ ] **Impl-001**: 实现基础设施层（数据库连接、错误处理、响应格式、配置）
  - 涉及文件: src/infra/database.ts, src/infra/error.ts, src/infra/response.ts, src/infra/config.ts, src/shared/types.ts, src/shared/utils/validation.ts
  - 需通过测试: 无（基础设施层无独立契约测试，由上层模块测试间接覆盖）
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Impl-002**: 实现 Express 应用入口和中间件注册
  - 涉及文件: src/app.ts
  - 需通过测试: 无
  - 依赖: Impl-001
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

### bookmark

- [ ] **Impl-003**: 实现书签 CRUD（repository + service + controller）
  - 涉及文件: src/modules/bookmark/bookmark.repository.ts, src/modules/bookmark/bookmark.service.ts, src/modules/bookmark/bookmark.controller.ts, src/modules/bookmark/bookmark.types.ts, src/modules/bookmark/index.ts
  - 需通过测试: Test-001, Test-002, Test-003, Test-004, Test-005
  - 依赖: Impl-002
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Impl-004**: 实现书签-标签关联管理
  - 涉及文件: src/modules/bookmark/bookmark.repository.ts, src/modules/bookmark/bookmark.service.ts, src/modules/bookmark/bookmark.controller.ts
  - 需通过测试: Test-006, Test-007
  - 依赖: Impl-003, Impl-005（需要 tag 模块的基本数据支持）
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

### tag

- [ ] **Impl-005**: 实现标签 CRUD（repository + service + controller）
  - 涉及文件: src/modules/tag/tag.repository.ts, src/modules/tag/tag.service.ts, src/modules/tag/tag.controller.ts, src/modules/tag/tag.types.ts, src/modules/tag/index.ts
  - 需通过测试: Test-008, Test-009, Test-010
  - 依赖: Impl-002
  - 开始时间:
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

---

## 附：变更场景示例（展示变更传播规则的实际运作）

> 以下是一个假设的变更场景，用于说明当实现过程中发现接口设计需要调整时，如何按变更传播规则处理。

### 场景：实现 Impl-003 时发现分页设计不合理

**背景**：Implementer agent 在实现 `GET /bookmarks` 时发现，当前契约定义的分页参数是 `page` + `pageSize`，但 SQLite 的 `LIMIT/OFFSET` 语义与 `page` 不直接对应，容易在并发删除时导致跳过或重复记录。技术负责人评估后决定改为 cursor-based 分页。

**处理步骤**：

1. **暂停 Impl-003**，在 task-board 标记为"阻塞：接口变更待确认"

2. **更新 api-contracts.md**（文档优先）：
   - `GET /bookmarks` 的 Request 参数从 `page + pageSize` 改为 `cursor + limit`
   - Response 增加 `nextCursor` 字段
   - commit: `docs: GET /bookmarks 改为 cursor 分页，影响范围: Test-002, Impl-003`

3. **更新契约测试**（测试跟进）：
   - 新会话中 Tester agent 更新 Test-002 的测试用例
   - 修改分页相关的请求参数和响应断言
   - commit: `test: 更新 Test-002 适配 cursor 分页`

4. **继续实现**（实现最后）：
   - 新会话中 Implementer agent 基于更新后的契约和测试继续 Impl-003
   - 实现 cursor-based 分页逻辑

5. **更新 task-board 记录**：
   - 在项目事件记录中注明：`Impl-003 因分页方案变更暂停，变更 api-contracts.md 和 Test-002 后恢复`
