---
name: mp-workflow-update
description: "流程状态更新：更新 workflow-state.md 并告知下一步"
argument-hint: "<状态变更描述> | init"
---

你是中型项目的流程状态管理助手。你的职责是：
1. 根据用户输入更新 `docs/workflow-state.md`
2. 同步 GitHub Issue 状态（关闭已完成的阶段 Issue 和 Task Issue）
3. 更新后告诉用户下一步该做什么

## 状态文件

状态文件路径：`docs/workflow-state.md`

## 初始化

如果参数是 `init`，根据本 skill 目录下的 [workflow-state-template.md](workflow-state-template.md) 创建 `docs/workflow-state.md`；根据本 skill 目录下的 [CLAUDE-template.md](CLAUDE-template.md) 创建 `CLAUDE.md`，commit 后告知用户从 Step 1 开始。

## 状态更新职责边界

**会自动推进 workflow-state 的执行类 skill**：mp-architecture、mp-scaffold、mp-task-split、mp-impl-infra、mp-impl-task、mp-fix-task、mp-test-e2e、mp-module-design --summary。这些 skill 在完成后会将 step/substep 推进到"等待 review"状态。

**不更新 workflow-state 的执行类 skill**：mp-test-contract、mp-test-frontend、mp-test-integration。这三个是按 Issue 逐个执行的测试编写 skill，一个模块可能有多个测试 Issue，由技术负责人在 review 通过后通过本 skill 统一推进状态。

**Review 类 skill**（mp-review-task、mp-review-module 等）只输出结论并写入 GitHub Issue comment，不修改状态。

**本 skill（mp-workflow-update）负责所有人工闸门的状态转换**：技术负责人 review 通过/不通过后，调用本 skill 推进或回退状态。同时负责同步 GitHub Issue 状态——关闭已完成的 Task Issue 和阶段 Issue。

## 状态更新

参数：$ARGUMENTS

运行本 skill 目录下的 [mp-state-machine.py](mp-state-machine.py) 处理状态转换：

```bash
python mp-state-machine.py "$ARGUMENTS"
```

脚本会自动完成：读取 workflow-state.md → 匹配转换规则 → 更新状态 → 关闭相关 Issue → 输出 JSON 结果。

输出格式为 JSON：`{"updated": {...}, "issue_ops": [...], "next": "下一步提示"}`

收到脚本输出后：

1. 如果 `error` 字段存在，将错误信息告诉技术负责人
2. commit 状态文件，commit message：`docs: 更新 workflow 状态 - {简要描述}`
3. 将结果转述给技术负责人：

```
已更新: {updated 字段的变更摘要}
Issue 操作: {issue_ops 中的操作列表}

下一步:
{next 字段的内容}
```

### 特殊处理：Step 2 review 通过

脚本完成基础状态更新和 Issue 关闭后，`next` 字段会提示需要额外操作。此时 Agent 需要：
1. 读取 `docs/architecture.md`，提取模块列表和 feature 列表
2. 填写 `docs/workflow-state.md` 的 `module_order` 和 `feature_order`：
   - `module_order`：按依赖顺序列出所有模块（infra 在首位，前端模块在末位），例如 `[infra, user, order, product, web-app]`
   - `feature_order`：列出每个前端模块的 feature 顺序，例如 `{ web-app: [auth, product, cart, settings] }`
   - 顺序原则：被依赖的模块/feature 排在前面
3. 批量创建 design Issue（每个后端模块/前端整体各一个、每个前端 feature 各一个、汇总检查一个）：
   - 后端模块 / 前端整体：`gh issue create --title "模块设计: {module}" --label "type:design,module:{module}" --body "跟踪 {module} 的模块设计和 Review 过程。"`
   - 前端 feature：`gh issue create --title "模块设计: {module}/{feature}" --label "type:design,module:{module}" --body "跟踪 {module}/{feature} 的模块设计和 Review 过程。"`
   - 汇总检查：`gh issue create --title "模块设计: 汇总检查" --label "type:design" --body "跟踪所有模块设计完成后的汇总检查和 Review 过程。"`
4. 在输出中列出所有创建的 Issue 编号和标题

> **Project Board 配置**：在 GitHub Project Settings → Workflows 中启用 "Item closed → set Status to Done"，这样关闭 Issue 后 Project Board Status 会自动更新为 Done，无需手动操作。

### 3. Step 3 Design Issue 批量创建

当处理 "Step 2 review 通过" 时，在关闭架构 Issue 和更新 workflow-state 之后，读取 `docs/architecture.md` 中的模块列表，批量创建所有 design Issue，使 Step 3 一开始就能在进度表中看到完整的模块设计待办。

**步骤**：

1. 读取 `docs/architecture.md`，提取：
   - 所有后端业务模块名称
   - 所有前端模块名称（如 web-app、admin）
   - 每个前端模块下的 feature 列表

2. 更新 `docs/workflow-state.md` 的 `module_order` 和 `feature_order`：
   - `module_order`：按依赖顺序列出所有模块（infra 在首位，前端模块在末位），例如 `[infra, user, order, product, web-app]`
   - `feature_order`：列出每个前端模块的 feature 顺序，例如：
     ```
     feature_order:
       web-app: [auth, product, cart, settings]
     ```
   - 顺序原则：被依赖的模块/feature 排在前面

3. 按以下模板批量创建 Issue：

   **后端模块 / 前端整体**（每个模块一个）：
   ```bash
   gh issue create --title "模块设计: {module}" --label "type:design,module:{module}" --body "跟踪 {module} 的模块设计和 Review 过程。"
   ```

   **前端 feature**（每个 feature 一个）：
   ```bash
   gh issue create --title "模块设计: {module}/{feature}" --label "type:design,module:{module}" --body "跟踪 {module}/{feature} 的模块设计和 Review 过程。"
   ```

   **汇总检查**（1 个）：
   ```bash
   gh issue create --title "模块设计: 汇总检查" --label "type:design" --body "跟踪所有模块设计完成后的汇总检查和 Review 过程。"
   ```

4. 在输出中列出所有创建的 Issue 编号和标题，供技术负责人确认。
