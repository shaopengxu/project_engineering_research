# 接口契约模板 — 选择指南

根据项目类型选择对应的模板文件，复制为 `docs/api-contracts.md` 后填写。

| 模板文件 | 适用项目类型 | 典型场景 |
|---------|------------|---------|
| [api-contracts-rest.md](api-contracts-rest.md) | Web 后端、全栈应用、BFF 层 | Express / FastAPI / Spring Boot |
| [api-contracts-cli.md](api-contracts-cli.md) | 命令行工具、脚手架、DevOps 工具 | Commander.js / Click / Cobra |
| [api-contracts-sdk.md](api-contracts-sdk.md) | 工具库、SDK、共享 package | npm 包 / PyPI 包 / Go module |
| [api-contracts-mq.md](api-contracts-mq.md) | 消息消费者、事件处理器 | Kafka / RabbitMQ / SQS |
| [api-contracts-frontend.md](api-contracts-frontend.md) | SPA、管理后台 | React / Vue / Next.js（无自建后端） |

如果项目混合了多种类型（如后端 API + CLI 管理工具），可以合并多个模板的内容到同一个 `docs/api-contracts.md` 中。

## 所有模板的共同要求

- 每个接口/命令/函数/事件/页面都必须包含四要素：**输入、输出、业务规则、错误处理**
- 文档末尾必须附带**需求追溯表**，逐条映射 PRD 的业务规则和验收标准到契约章节
