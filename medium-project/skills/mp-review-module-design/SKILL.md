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

检查清单 — 模块设计：
1. 内部分层符合 architecture.md 约定
2. 数据模型完整（字段、类型、约束）
3. 公开接口清单与 architecture.md 一致
4. 消费的外部接口在依赖关系中有体现
5. 关键业务逻辑有详细说明（状态机、计算规则等）
6. 没有设计其他模块的内容

检查清单 — 接口契约：
7. 每个接口都有完整的五要素（输入、输出、业务规则、错误码、consumers）
8. 接口签名与 module-design 中"公开接口清单"一致
9. 错误码全局不重复（与已有模块不冲突）
10. 接口风格与已有模块一致（遵循通用约定）

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

完成后：将 Review 结果输出给技术负责人，**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人通过 `/mp-workflow-update` 触发（如 `/mp-workflow-update user 模块设计 review 通过`）。
