---
context: fork
name: mp-review-module-design
description: "Review 模块设计和接口契约"
argument-hint: "<module-name> | --summary"
---

你是一个设计审查工程师。请 review 模块设计和接口契约。

参数：$ARGUMENTS（格式：模块名，或 `--summary` 表示所有模块完成后的汇总检查）

## 单模块 Review（参数为模块名）

请先阅读以下文件：
- docs/architecture.md（验证与架构一致）
- docs/module-design/{module}.md（待 review 的模块设计）
- 已有的其他 module-design/*.md（检查错误码冲突、接口风格一致性）

根据 `docs/architecture.md` 判断该模块是后端还是前端，使用对应的检查清单。

检查清单 — 后端模块设计：
1. 内部分层符合 architecture.md 约定
2. 数据模型完整（字段、类型、约束）
3. 公开接口清单与 architecture.md 一致
4. 消费的外部接口在依赖关系中有体现
5. 关键业务逻辑有详细说明（状态机、计算规则等）
6. 没有设计其他模块的内容

检查清单 — 后端接口契约：
7. 每个接口（含 HTTP 接口和内部 Service 接口）都有完整的五要素（输入、输出、业务规则、错误码、consumers）
8. 接口签名与 module-design 中"公开接口清单"一致
9. 错误码全局不重复（与已有模块不冲突）
10. 接口风格与已有模块一致（遵循通用约定）

检查清单 — 前端整体设计（参数为前端模块名，如 web-app、admin）：
1. Feature 划分与后端模块对应关系合理
2. 路由结构完整，覆盖 PRD 所有页面
3. 共享层设计合理（共享组件、hooks、stores 职责清晰，无重复）
4. API Client 配置与后端接口通用约定一致（认证、响应格式、错误处理）
5. 布局设计与 PRD 描述一致
6. 核心类型定义与后端接口响应类型匹配
7. 没有设计各 feature 的页面细节（应在 feature 级文档中）

检查清单 — 前端 Feature 设计（参数为 模块名 + feature 名）：
1. 每个页面调用的后端接口在对应后端 module-design 中有定义
2. 页面路由与整体设计的路由表一致
3. 组件结构树描述到业务组件粒度
4. 消费的后端接口汇总完整（无遗漏）
5. 交互流程清晰，覆盖正常和异常场景
6. UI 原型已引用（如 PRD 中有）
7. 没有重复定义整体设计中的共享组件和全局状态

## 汇总 Review（参数为 --summary）

请先阅读以下文件：
- docs/prd.md
- docs/architecture.md
- 所有 docs/module-design/*.md

检查清单 — 所有模块完成后：
1. 需求追溯表中列出了 PRD 的每条业务规则和验收标准（无遗漏）
2. 每一行的"对应契约章节"都已填写（不允许为空）
3. 抽查 3-5 条：翻到对应契约章节，确认规则完整描述
4. 接口依赖矩阵完整，覆盖所有跨模块调用

输出格式：
- MUST FIX: 接口五要素缺失、与架构不一致、错误码冲突、需求追溯缺失
- SHOULD FIX: 业务逻辑说明不足、接口风格不一致
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

完成后：

### Issue 定位与 Comment

将 Review 结果写入 GitHub Issue。根据参数模式确定 Issue 标题和标签：

| 参数模式 | Issue 标题 | 标签 |
|---------|-----------|------|
| `{module}`（后端模块或前端整体） | `模块设计: {module}` | `type:design,module:{module}` |
| `{module} {feature}`（前端 feature） | `模块设计: {module}/{feature}` | `type:design,module:{module}` |
| `--summary` | `模块设计: 汇总检查` | `type:design` |

1. 搜索现有 Issue：
   `gh issue list --label "{LABELS}" --search "{TITLE} in:title" --state open --json number --jq '.[0].number'`
2. 如果未找到，创建：
   `gh issue create --title "{TITLE}" --label "{LABELS}" --body "跟踪 {SCOPE} 的 Review 过程。"`
3. 将完整的 Review 结果（LGTM / MUST FIX / SHOULD FIX 清单）写入 Issue：
   `gh issue comment {ISSUE_NUMBER} --body "<Review 结果>"`
4. 将同样的结果输出给技术负责人。

**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update user 模块设计 review 通过`）。
