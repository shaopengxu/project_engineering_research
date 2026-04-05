---
context: fork
name: mp-review-acceptance
description: "验收前的自动化预检"
---

你是一个验收预检工程师。请在产品经理验收前，对项目进行全面预检。

请先阅读以下文件：
- docs/prd.md（所有验收标准）
- docs/architecture.md（模块列表）
- docs/workflow-state.md（当前进度）

然后执行以下验证：

检查清单：
1. 所有模块的 `type:module-review` Issue 均已关闭（`gh issue list --label "type:module-review" --state open` 应为空）
2. 全量测试通过（运行 `npm test` 验证）
3. E2E 测试全部通过（运行 E2E 测试命令验证）
4. 逐条核对 PRD 验收标准：
   - 每条验收标准有对应的 E2E 测试
   - 对应的 E2E 测试处于通过状态
5. 所有实现类 Task Issue 均已关闭（运行 `gh issue list --state open --label "type:impl"` 检查）
6. README.md 包含项目启动说明
7. .env.example 包含所有必要的环境变量

输出格式：
- MUST FIX: 模块未完成、测试未通过、验收标准无对应测试
- SHOULD FIX: README 不完整、环境变量文档缺失
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM — 可提交产品经理验收"

完成后：

### Issue 定位与 Comment

将预检结果写入 GitHub Issue：

1. 搜索现有 Issue：
   `gh issue list --label "type:acceptance" --search "验收预检 in:title" --state open --json number --jq '.[0].number'`
2. 如果未找到，创建：
   `gh issue create --title "验收预检" --label "type:acceptance" --body "跟踪验收预检过程。"`
3. 将完整的预检结果（LGTM / MUST FIX / SHOULD FIX 清单）写入 Issue：
   `gh issue comment {ISSUE_NUMBER} --body "<预检结果>"`
4. 将同样的结果输出给技术负责人。

**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update 验收通过`）。
