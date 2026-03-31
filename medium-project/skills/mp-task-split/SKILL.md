---
context: fork
name: mp-task-split
description: "拆分任务并创建 GitHub Issues"
---

你是一个软件架构师。请根据架构文档和模块设计拆分任务，并创建 GitHub Issues。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：模块划分、依赖关系、关键业务路径）
- docs/module-design/（所有模块设计文件，了解接口数量和复杂度）

请完成以下工作：

1. **创建 GitHub Issues**（使用以下模板）：

   **契约测试 Issue**：
   ```bash
   gh issue create \
     --title "[{module}] 契约测试: {接口名称}" \
     --label "type:contract-test,module:{module}" \
     --milestone "{milestone}" \
     --project "{project-name}" \
     --body "## 任务描述\n为 {接口名称} 编写契约测试。\n\n## 所属模块\n{module}\n\n## 依赖\n无\n\n## 对应契约章节\nmodule-design/{module}.md 中的 \"{接口名称}\" 章节\n\n## 需通过测试\n- [ ] 正常流程测试\n- [ ] 异常流程测试（错误码覆盖）"
   ```

   **实现 Issue**：
   ```bash
   gh issue create \
     --title "[{module}] 实现: {任务描述}" \
     --label "type:impl,module:{module}" \
     --milestone "{milestone}" \
     --project "{project-name}" \
     --body "## 任务描述\n{一句话描述}\n\n## 所属模块\n{module}\n\n## 依赖\n- Depends on #{issue-number}\n\n## 需通过测试\n- [ ] 契约测试: tests/contracts/{module}/{test-file}\n- [ ] L1 集成测试: tests/integration/{module}/{test-file}\n\n## 验收标准\n- [ ] {criterion 1}\n- [ ] {criterion 2}"
   ```

   **集成测试 Issue**：
   ```bash
   gh issue create \
     --title "[integration] L2: {关键路径描述}" \
     --label "type:integration-test" \
     --milestone "{milestone}" \
     --project "{project-name}" \
     --body "## 任务描述\n验证 {module-a} → {module-b} 的关键路径集成。\n\n## 涉及模块\n{module-a}, {module-b}\n\n## 依赖\n- Depends on #{module-a-issue}\n- Depends on #{module-b-issue}\n\n## 测试路径\ntests/integration/paths/{path-name}.test.ts\n\n## 验收标准\n- [ ] 真实模块间调用（不 Mock）\n- [ ] 覆盖正常流程和关键异常流程"
   ```

2. **组织 Sub-issues 层级**：
   - 每个模块创建一个父 Issue（模块粒度）
   - Task 作为子 Issue 挂在父 Issue 下
   - 依赖声明：Issue body 中用 `Depends on #N` 标注前置依赖

任务拆分原则：
- infra 独立为最高优先级 Task
- 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
- 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
- Task 间依赖关系标注为 DAG（在 Issue body 中声明 Depends on）
- 每个 Task 标注需通过的测试
- 如果拆不到粒度，停下来说明问题

模块内 Task 拆分策略：
- 按层拆分（CRUD 密集型）: repository → service → controller
- 按功能拆分（功能丰富型）: 注册登录 → 个人资料 → 权限管理
- 拆不到粒度 → 说明模块划分需要回退到 Step 2 调整

要求：
- 不要写业务代码和测试代码
- Issues 创建完成后在 commit message 中记录

完成后更新 `docs/workflow-state.md`：设置 `step: 4`，`substep: 4b-review`。根据创建的 Issues 填充模块进度表：
- infra 一行（类型"基础设施"，设计/契约测试/Task Review/模块 Review/L2 集成测试 标 `N/A`）
- 每个后端模块一行（类型"后端"）
- 前端模块按 feature 拆行（如 `web-app/auth`、`web-app/product`，类型"前端"），feature 列表从 architecture.md 的 Feature 划分获取
- 所有可填列初始为空

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
