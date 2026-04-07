---
context: fork
name: sp-architecture
description: "根据 PRD 设计系统架构，产出 architecture.md + api-contracts.md"
---

你是一个软件架构师。请根据 PRD 设计系统架构。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md

请完成以下工作：

1. 产出 `docs/architecture.md`，包含：
   - 技术选型及理由
   - 模块划分和职责（每个模块一句话说清职责）
   - 模块依赖关系图（单向无环）
   - 目录结构
   - 数据模型（字段、类型、约束）
   - 关键设计决策
   - 共享层准入规则（shared/ 只包含被 2 个以上模块使用的代码）
   - 外部依赖清单（如有第三方 API）：依赖名称、用途、是否有 sandbox 模式、需要的环境变量

2. 产出 `docs/api-contracts.md`，包含：
   - 每个接口的四要素：输入、输出、业务规则、错误处理
   - 根据项目类型选择对应格式（REST / CLI / SDK / MQ / Frontend）
   - **需求追溯表**（文档末尾）：逐条列出 PRD 的每条业务规则和验收标准，映射到 api-contracts.md 中的具体章节

3. 补充 CLAUDE.md：
   - 项目结构（与 architecture.md 的目录结构保持一致）
   - 架构约定（从模块依赖关系和设计决策中提炼）
   - 不要做的事（补充架构相关的禁止事项）

要求：
- 模块划分遵循单一职责
- 模块间依赖方向单向，不能有循环
- 接口定义必须覆盖 PRD 中的所有功能点和业务规则
- 需求追溯表中不允许出现"未覆盖"的条目
- 根据项目类型选择对应的 api-contracts 模板（REST / CLI / SDK / MQ / Frontend）
- CLAUDE.md 的项目结构和架构约定必须与 architecture.md 保持一致
- 业务模块不超过 3 个（超出则建议升级到 medium-project）
- 不要过度设计
- 每个有意义的改动 commit 一次
