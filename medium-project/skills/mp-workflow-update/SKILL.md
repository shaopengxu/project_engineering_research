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

执行类 skill（mp-impl、mp-test-contract 等）在完成后会自动将 workflow-state 的 step/substep 推进到"等待 review"状态。Review 类 skill（mp-review-task、mp-review-module 等）只输出结论并写入 GitHub Issue comment，不修改状态。

**本 skill（mp-workflow-update）负责所有人工闸门的状态转换**：技术负责人 review 通过/不通过后，调用本 skill 推进或回退状态。同时负责同步 GitHub Issue 状态——关闭已完成的 Task Issue 和阶段 Issue。

## 状态更新

参数：$ARGUMENTS

用户会用自然语言描述状态变更，例如：
- "Step 1 完成，PRD 和 CLAUDE.md 已就绪"
- "Step 2 review 通过了"
- "user 模块设计 review 通过"
- "web-app 整体设计完成"
- "web-app auth feature 设计 review 通过"
- "Step 3 review 通过"
- "脚手架 review 通过"
- "Issues review 通过"
- "infra #1 review 通过"
- "user 契约测试 #5 review 通过"
- "web-app auth 契约测试 #8 review 通过"
- "Issue #12 实现完成"
- "Issue #12 review LGTM"
- "Issue #12 review 有 MUST FIX"
- "Issue #12 修复完成"
- "user 模块所有 Task 完成"
- "web-app auth 所有 Task 完成"
- "web-app auth Feature Review LGTM"
- "user 模块 Review LGTM"
- "web-app 模块 Review LGTM"
- "user L2 集成测试 #15 完成"
- "开始处理 order 模块"
- "开始处理 web-app auth feature"
- "E2E 测试通过"
- "验收通过"

## 更新逻辑

1. 读取当前 `docs/workflow-state.md`
2. 根据用户描述确定要更新的字段和需要关闭的 Issue：

| 用户描述 | workflow-state 更新 | GitHub Issue 操作 |
|---------|-------------------|------------------|
| Step 1 完成 | step → 2, substep → 清空 | **关闭阶段 Issue**: `type:prd-review` 标题含 "PRD Review" |
| Step 2 review 通过 | step → 3, substep → 清空 | **关闭阶段 Issue**: `type:architecture` 标题含 "架构设计" |
| {module} 模块设计 review 通过 | （不更新） | **关闭阶段 Issue**: `type:design` + `module:{module}` 标题含 "模块设计: {module}" |
| {module} {feature} 模块设计 review 通过 | （不更新） | **关闭阶段 Issue**: `type:design` + `module:{module}` 标题含 "模块设计: {module}/{feature}" |
| 前端整体设计完成 | 备注中记录 | **关闭阶段 Issue**（如存在）: `type:design` + `module:{module}` 标题含 "模块设计: {module}" |
| Step 3 review 通过 | step → 4, substep → 清空 | **关闭阶段 Issue**: `type:design` 标题含 "模块设计: 汇总检查" |
| 脚手架 review 通过 | step → 4, substep → 4b | **关闭阶段 Issue**: `type:scaffold` 标题含 "脚手架" |
| Issues review 通过 | step → 5, substep → 5a | **关闭阶段 Issue**: `type:task-split` 标题含 "任务拆分" |
| infra #N review 通过 | substep → 5b | **关闭 Task Issue #N** |
| {module} 契约测试 #N review 通过 | substep → 5c | **关闭 Task Issue #N** |
| Issue #N 实现完成 | substep → 5c-review | （不操作 Issue） |
| Issue #N review LGTM | substep → 5c（下一个 Task） | **关闭 Task Issue #N** |
| Issue #N review 有问题 | substep → 5e | （不操作 Issue） |
| Issue #N 修复完成 | substep → 5e-review | （不操作 Issue） |
| {module} 模块所有 Task 完成 | substep → 5f | （不操作 Issue） |
| {feature} 所有 Task 完成 | substep → 5f | （不操作 Issue） |
| {module} {feature} Feature Review LGTM | substep → 5b（下一个 feature）或不变（等待模块 Review） | **关闭阶段 Issue**: `type:feature-review` + `module:{module}` 标题含 "Feature Review: {module}/{feature}" |
| {module} 模块 Review LGTM | substep → 5g | **关闭阶段 Issue**: `type:module-review` + `module:{module}` 标题含 "模块 Review: {module}" |
| L2 集成测试 #N 完成 | module → 下一个模块 | **关闭 Task Issue #N** |
| 开始处理某模块 | module → 该模块, substep → 5b | （不操作 Issue） |
| 开始处理某 feature | module → 该模块, feature → 该 feature, substep → 5b | （不操作 Issue） |
| E2E 测试通过 | step → 7 | **关闭阶段 Issue**: `type:e2e` 标题含 "E2E 测试" |
| 验收通过 | step → done | **关闭阶段 Issue**: `type:acceptance` 标题含 "验收预检" |

3. 更新 `docs/workflow-state.md`
4. 执行 GitHub Issue 操作（见下方"GitHub Issue 同步"）
5. commit 状态文件，commit message：`docs: 更新 workflow 状态 - {简要描述}`
6. 输出：

```
已更新: {变更摘要}

下一步:
{具体操作描述或 skill 调用命令}
```

## GitHub Issue 同步

本 skill 在状态推进时执行两类 Issue 操作：

### 1. Task Issue 关闭

当表格中标注 **关闭 Task Issue #N** 时，直接关闭：
```bash
gh issue close {N} --comment "Review 通过，Task 完成。"
```

### 2. 阶段 Issue 关闭

当表格中标注 **关闭阶段 Issue** 时，先按标签 + 标题搜索 open 状态的 Issue，找到后关闭：
```bash
# 搜索（以架构设计为例）
ISSUE_NUM=$(gh issue list --label "type:architecture" --search "架构设计 in:title" --state open --json number --jq '.[0].number')

# 如果找到，关闭
if [ -n "$ISSUE_NUM" ]; then
  gh issue close $ISSUE_NUM --comment "Review 通过，阶段完成。"
fi
```

如果未找到匹配的 Issue 则跳过（可能尚未创建或已关闭），不报错。

### 阶段 Issue 搜索模式速查

| 阶段 Issue | 搜索标签 | 标题关键词 |
|-----------|---------|-----------|
| PRD Review | `type:prd-review` | `PRD Review` |
| 架构设计 | `type:architecture` | `架构设计` |
| 模块设计: {module} | `type:design` + `module:{module}` | `模块设计: {module}` |
| 模块设计: {module}/{feature} | `type:design` + `module:{module}` | `模块设计: {module}/{feature}` |
| 模块设计: 汇总检查 | `type:design` | `模块设计: 汇总检查` |
| 脚手架 | `type:scaffold` | `脚手架` |
| 任务拆分 | `type:task-split` | `任务拆分` |
| Feature Review | `type:feature-review` + `module:{module}` | `Feature Review: {module}/{feature}` |
| 模块 Review | `type:module-review` + `module:{module}` | `模块 Review: {module}` |
| E2E 测试 | `type:e2e` | `E2E 测试` |
| 验收预检 | `type:acceptance` | `验收预检` |

> **Project Board 配置**：在 GitHub Project Settings → Workflows 中启用 "Item closed → set Status to Done"，这样关闭 Issue 后 Project Board Status 会自动更新为 Done，无需手动操作。
