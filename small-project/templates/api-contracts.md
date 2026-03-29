# 接口契约模板 — 选择指南

根据项目类型选择对应的模板文件，复制为 `docs/api-contracts.md` 后填写。

| 模板文件 | 适用项目类型 | 典型场景 |
|---------|------------|---------|
| [api-contracts-rest.md](api-contracts-rest.md) | Web 后端、全栈应用、BFF 层 | Express / FastAPI / Spring Boot |
| [api-contracts-cli.md](api-contracts-cli.md) | 命令行工具、脚手架、DevOps 工具 | Commander.js / Click / Cobra |
| [api-contracts-sdk.md](api-contracts-sdk.md) | 工具库、SDK、共享 package | npm 包 / PyPI 包 / Go module |
| [api-contracts-mq.md](api-contracts-mq.md) | 消息消费者、事件处理器 | Kafka / RabbitMQ / SQS |
| [api-contracts-frontend.md](api-contracts-frontend.md) | SPA、管理后台 | React / Vue / Next.js（无自建后端） |

## 混合类型项目（如后端 + 前端）

如果项目包含多种类型（如后端 REST API + 前端 SPA），将多个模板的内容合并到同一个 `docs/api-contracts.md` 中，用一级标题分隔：

```markdown
# 后端 API 接口
（从 api-contracts-rest.md 模板填写）

# 前端 Store/页面
（从 api-contracts-frontend.md 模板填写）

# 需求追溯表
（一张表覆盖所有 PRD 规则，"对应契约章节"指向上方对应的标题）
```

保持单个 `docs/api-contracts.md` 文件，不拆成多个——整个流程中所有 agent 和文档都引用这一个路径。

## 模块间内部接口（可选）

如果模块间存在被依赖的内部接口（如 storage 模块的 load/save 被 task 模块依赖），且其行为变更会导致依赖方出错，建议也纳入契约文档。在对外接口章节之后、需求追溯表之前，增加一个"模块间内部接口"章节，说明：

- 为什么这些内部接口需要契约测试（被其他模块依赖，行为变更会破坏依赖方）
- 每个接口的输入、输出、业务规则

**判断标准**：纯模块内部的 helper 函数不需要；只有被其他模块依赖且行为变更会导致依赖方出错的接口才纳入。

## 所有模板的共同要求

- 每个接口/命令/函数/事件/页面都必须包含四要素：**输入、输出、业务规则、错误处理**
- 文档末尾必须附带**需求追溯表**，逐条映射 PRD 的业务规则和验收标准到契约章节
