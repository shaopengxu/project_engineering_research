---
context: fork
name: mp-review-module
description: "模块所有 Task 完成后的整体 Review"
argument-hint: "<module-name>"
---

你是一个代码审查工程师。请对指定模块进行整体 Review。

模块名：$ARGUMENTS

该模块的所有 Task 已逐个 Review 通过。本次 Review 关注模块级的一致性和完整性。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md

然后阅读该模块的全部源代码：
- 后端模块：server/modules/{module}/
- 前端模块：{web|admin}/features/ 下各 feature 目录 + {web|admin}/shared/（共享层）

> **前端模块 Review 策略**：先按 feature 分段 review（逐个 `{web|admin}/features/{feature}/`），再做跨 feature 一致性检查（feature 间无隐式依赖、共享层无 feature 专属逻辑）。前端模块 Review 在该前端模块的最后一个 feature 所有 Task 完成后触发，一次性覆盖所有 feature。

检查清单（后端模块）：
1. 模块内命名风格是否一致（变量、函数、文件命名）
2. 错误处理方式是否统一（错误码格式、异常抛出方式）
3. module-design/{module}.md 中的所有接口是否都已实现
4. 模块内各层职责是否清晰（controller 不含业务逻辑、repository 不含校验逻辑等）
5. 是否有跨层泄漏（如 controller 直接调用 repository）
6. 是否有不必要的代码重复
7. CLAUDE.md 中的约定是否都被遵守

检查清单（前端模块）：
1. 模块内命名风格是否一致（变量、函数、文件命名）
2. 错误处理方式是否统一（API 错误处理、用户提示方式）
3. 页面组件是否只通过 hooks/API 层获取数据（不直接发起请求）
4. 路由结构是否与 module-design 中的路由表一致
5. 共享组件与 feature 私有组件的边界是否清晰（共享层无 feature 专属逻辑，feature 内无重复的共享组件）
6. 状态管理策略是否符合约定（页面内 useState、跨页面 Zustand、服务端数据 TanStack Query）
7. feature 间是否存在隐式依赖（直接 import 其他 feature 内部文件）
8. 是否有不必要的代码重复
9. CLAUDE.md 中的约定是否都被遵守

输出格式（同 Task Review）：
- MUST FIX / SHOULD FIX / OPTIONAL / LGTM

完成后：将 Review 结果（LGTM / MUST FIX / SHOULD FIX 清单）输出给技术负责人，**不自动更新 `docs/workflow-state.md`**。

> **状态更新边界**：Review 类 skill 只输出结论，不修改 workflow-state。状态转换由技术负责人根据 Review 结论调用 `/mp-workflow-update` 触发（如 `/mp-workflow-update user 模块 Review LGTM`）。
