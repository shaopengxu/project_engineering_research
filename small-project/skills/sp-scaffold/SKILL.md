---
context: fork
name: sp-scaffold
description: "初始化项目脚手架 + 拆分任务写入 task-board.md"
---

你是一个软件架构师。请根据架构文档初始化项目脚手架并拆分开发任务。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md
- docs/api-contracts.md

请完成两项工作：

### 1. 项目脚手架初始化

- 根据 architecture.md 的技术选型和目录结构创建项目框架
- 安装依赖、配置构建工具、测试框架、lint 等开发工具
- 确保以下命令能成功执行：
  - 依赖安装命令（如 `npm install`）
  - lint 命令（即使无源码）
  - 测试框架启动命令（即使无测试文件）
- 只创建目录结构和配置文件，不写业务代码，不写测试代码
- 对于强类型语言（如 TypeScript），为每个模块创建**导出桩文件**（只声明函数签名，函数体 `throw new Error('Not implemented')`），确保 Step 4 的契约测试能编译/加载
- 如 architecture.md 中有外部依赖清单，在 `.env.example` 中包含对应 API key 占位变量并注释说明
- 回填 CLAUDE.md：根据实际脚手架配置填写"常用命令"和"测试环境"章节

### 2. 拆分开发任务

产出 `docs/task-board.md`：
- 按 task-board.md 模板格式填写
- 契约测试任务：api-contracts.md 中每个接口对应一个测试任务，标注对应契约章节和测试文件路径
- 实现任务：按模块拆分，每个任务标注"需通过测试"（关联正确的 Test ID）
- 被依赖模块（shared/infra）的任务排在前面
- 依赖关系完整，不能有隐式依赖
- 每个任务粒度：< 15 文件、< 500 行、一句话可描述、单会话可完成
- 如果拆不到这个粒度，停下来说明问题，可能需要回退到 Step 2 调整模块划分

要求：
- 脚手架和 task-board.md 完成后各 commit 一次
- 不要写业务代码和测试代码
