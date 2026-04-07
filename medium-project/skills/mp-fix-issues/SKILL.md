---
context: fork
name: mp-fix-issues
description: "根据 Issues Review 反馈修复任务拆分"
---

你是一个项目管理工程师。请根据 Issues Review 反馈修复任务拆分。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（模块列表、依赖关系）
- docs/module-design/*.md（接口清单，用于验证 Issue 覆盖度）

然后获取项目信息：
- `gh issue list --state open --limit 100 --json number,title,labels,body` 查看所有 Issue

然后查看 Review 反馈：
1. 搜索 Issue：`python medium-project/scripts/mp-issue-helper.py find-or-create --label "type:task-split" --search "任务拆分"`（只搜索，不传 --create-title 则不创建）
2. 查看 comments：`gh issue view {ISSUE_NUMBER} --comments`
3. 取最后一条 Review comment 作为修复依据

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 修复类型：
  - **接口缺少对应 Issue**：创建缺失的契约测试 Issue 或实现 Issue（使用 `/mp-task-split` 中的 Issue 模板格式）
  - **依赖关系有环**：编辑 Issue body 中的 `Depends on` 声明，调整依赖方向
  - **依赖标注缺失**：补充 Issue body 中的 `Depends on #N`
  - **标签不正确**：使用 `gh issue edit {N} --add-label / --remove-label` 修正
  - **关键路径缺少集成测试 Issue**：创建 L2 集成测试 Issue
  - **优先级不合理**：调整 milestone 分配
- 创建新 Issue 时：
  - 获取 project-name：`gh project list --owner "@me"`
  - 获取可用 milestone：`gh api repos/{owner}/{repo}/milestones --jq '.[].title'`（{owner}/{repo} 从 `gh repo view --json owner,name` 获取）
  - 使用与 `/mp-task-split` 一致的 Issue 模板格式
  - 将新 Issue 加入 Project
- 不要删除已有 Issue（如认为某个 Issue 多余，在 Review Issue comment 中说明）
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复，请重新 Review。"` 报告

不更新 `docs/workflow-state.md`（当前状态已在 Step 4b review 等待中）。

> **重新 Review**：修复完成后，技术负责人应再次调用 `/mp-review-issues` 进行重新 Review。

> **状态更新边界**：skill 不修改 workflow-state。Review 通过后由技术负责人通过 `/mp-workflow-update Issues review 通过` 推进状态。
