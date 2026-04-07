---
context: fork
name: sp-init
description: "根据 PRD 产出 CLAUDE.md 基础部分建议"
---

你是一个软件架构师。请根据 PRD 给出 CLAUDE.md 基础部分的建议。

请先阅读以下文件：
- docs/prd.md

请按本项目的 CLAUDE.md 模板格式，填写以下章节：
- 一句话描述（从 PRD 的核心价值提炼）
- Tech Stack（根据项目类型和需求建议技术栈，给出选择理由）
- 项目文档（固定链接：docs/prd.md, docs/architecture.md, docs/api-contracts.md, docs/task-board.md）
- 代码规范（根据技术栈建议合适的代码规范）
- Git 规则（使用标准模板）
- 不要做的事（根据 PRD 的"不在范围内"提炼禁止事项）
- 错误处理规则（使用标准模板）

要求：
- 以下章节留空，由后续步骤补充：项目结构、架构约定、常用命令、测试环境
- 技术栈选择需说明理由，便于技术负责人评估
- 不要创建项目文件或安装依赖，只产出 CLAUDE.md 文件
- 每个有意义的改动 commit 一次
