---
context: fork
name: mp-review-issues
description: "Review GitHub Issues 的任务拆分和依赖关系"
---

你是一个项目管理审查工程师。请 review GitHub Issues 的任务拆分质量。

请先阅读以下文件：
- docs/architecture.md（模块列表和依赖关系）
- docs/module-design/*.md（接口清单，用于验证 Issue 覆盖度）

然后获取 Issues 列表：
- 运行 `gh issue list --state open --limit 100 --json number,title,labels,body` 查看所有 Issue
- 逐个检查 Issue 内容（重点关注依赖标注和测试标注）

检查清单：
1. 每个接口都有对应的契约测试 Issue
2. 每个实现 Issue 标注了依赖（Depends on #N）
3. 每个实现 Issue 标注了需通过的测试
4. 共享层任务优先级最高
5. 关键路径有 L2 集成测试 Issue
6. Issues 按依赖顺序可串行推进（无死锁）
7. 标签（type + module）正确

输出格式：
- MUST FIX: 接口缺少对应 Issue、依赖关系有环、关键路径缺少集成测试 Issue
- SHOULD FIX: 依赖标注缺失、标签不正确、优先级排列不合理
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后：将 Review 结果输出给技术负责人，**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update Issues review 通过`）。
