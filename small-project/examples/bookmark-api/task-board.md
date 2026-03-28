# Bookmark API 任务看板

> 更新规则：由技术负责人统一更新，避免多人同时编辑冲突。Agent 完成任务后在会话中报告状态，由技术负责人同步到此文件。

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
  - 分支: feature/impl-001
  - 涉及文件: src/infra/database.ts, src/infra/error.ts, src/infra/response.ts, src/infra/config.ts, src/shared/types.ts, src/shared/utils/validation.ts
  - 需通过测试: 无（基础设施层无独立契约测试，由上层模块测试间接覆盖）
  - 依赖: 无
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Impl-002**: 实现 Express 应用入口和中间件注册
  - 分支: feature/impl-002
  - 涉及文件: src/app.ts
  - 需通过测试: 无
  - 依赖: Impl-001
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

### bookmark

- [ ] **Impl-003**: 实现书签 CRUD（repository + service + controller）
  - 分支: feature/impl-003
  - 涉及文件: src/modules/bookmark/bookmark.repository.ts, src/modules/bookmark/bookmark.service.ts, src/modules/bookmark/bookmark.controller.ts, src/modules/bookmark/bookmark.types.ts, src/modules/bookmark/index.ts
  - 需通过测试: Test-001, Test-002, Test-003, Test-004, Test-005
  - 依赖: Impl-002
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

- [ ] **Impl-004**: 实现书签-标签关联管理
  - 分支: feature/impl-004
  - 涉及文件: src/modules/bookmark/bookmark.repository.ts, src/modules/bookmark/bookmark.service.ts, src/modules/bookmark/bookmark.controller.ts
  - 需通过测试: Test-006, Test-007
  - 依赖: Impl-003, Impl-005（需要 tag 模块的基本数据支持）
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

### tag

- [ ] **Impl-005**: 实现标签 CRUD（repository + service + controller）
  - 分支: feature/impl-005
  - 涉及文件: src/modules/tag/tag.repository.ts, src/modules/tag/tag.service.ts, src/modules/tag/tag.controller.ts, src/modules/tag/tag.types.ts, src/modules/tag/index.ts
  - 需通过测试: Test-008, Test-009, Test-010
  - 依赖: Impl-002
  - 开始时间:
  - 状态: 未开始
  - 阻塞原因:

## 完成记录

| Task | 类型 | 完成时间 | 备注 |
|------|------|---------|------|
| | | | |
