---
context: fork
name: mp-test-frontend
description: "为前端模块的 feature 编写 API 调用层测试 + 页面渲染测试"
argument-hint: "<module-name> <feature-name> <issue-number>"
---

你是一个测试工程师。请为前端模块的指定 feature 编写测试。

参数：$ARGUMENTS（格式：模块名 feature名 Issue编号）

前端测试包含两部分：
1. **API 调用层测试**：验证 api/ 层的请求参数和响应处理与后端接口定义一致
2. **页面渲染测试**：验证页面组件在给定 mock 数据下能正确渲染关键元素并响应用户交互（shallow 级别：直接 mock hooks 返回值，不关心数据获取链路）

这些测试将在实现之前编写，作为 TDD 的驱动力。

> **与 L1 集成测试的区别**：本 skill 编写的测试属于"契约级"，聚焦于 API 层请求/响应规格和页面渲染正确性，mock 粒度较粗（mock hooks 或 MSW）。后续 `/mp-impl` 中编写的前端 L1 集成测试属于"集成级"，聚焦于页面 → hooks → API 层的真实数据流转串联，仅在网络层使用 MSW mock，不 mock hooks。两者测试目标不同，不应重复：
> - **本 skill（契约级）**：API 函数的请求格式对不对？页面拿到数据能不能正确渲染？→ 验证"接口契约"
> - **mp-impl（集成级）**：页面触发操作后，hook 是否正确调用 API 函数、状态是否正确更新、页面是否正确响应？→ 验证"端内串联"

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（整体设计：共享层、路由结构）
- docs/module-design/{module}-{feature}.md（本 feature 的页面、交互、调用的后端接口）
- docs/module-design/（该 feature 对应的后端模块设计文件，了解后端接口定义）

要求：

API 调用层测试：
- 每个后端接口调用验证请求 URL、HTTP 方法、请求参数格式
- 验证响应数据的解析和转换逻辑
- 验证错误响应的处理（对照后端接口的错误码）
- 使用 MSW（Mock Service Worker）拦截 HTTP 请求（已在项目依赖中安装）
- 测试代码放在 tests/contracts/{module}/{feature}/ 目录下

页面渲染测试：
- 每个页面至少一个渲染测试（使用 React Testing Library）
- 验证关键用户交互（按钮点击、表单提交、列表渲染）
- Mock 所有 API 调用（通过 mock hooks 或 MSW）
- 测试代码放在 tests/contracts/{module}/{feature}/ 目录下

通用要求：
- 测试之间互相独立，不依赖执行顺序
- 每个测试用例用注释标注对应的 module-design 来源
- 此阶段只写测试，不写业务代码
- 如果 module-design 有模糊或矛盾之处，停下来指出问题
- 每个有意义的改动 commit 一次，commit message 格式：`test(<module>/<feature>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "{feature} 前端测试编写完成"` 报告

预期状态：测试代码能编译/加载，但执行时全部失败（因为实现不存在）— 这是 TDD 的正常状态（先红后绿）。脚手架阶段创建的 api/ 层桩文件和页面组件桩文件解决编译问题。

注意：你只需要阅读本 feature 的设计文档和整体设计文档，不需要阅读其他 feature 的文档。

完成后：不更新 `docs/workflow-state.md`（模块级进度通过 GitHub Issues 追踪）。状态转换由技术负责人通过 `/mp-workflow-update` 触发。
