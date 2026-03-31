---
context: fork
name: mp-module-design
description: "Medium-project Step 3: 模块详细设计 + 接口契约，支持后端模块、前端整体、前端 feature、汇总"
argument-hint: "<module-name> [feature-name] | --summary"
---

根据参数决定执行哪种设计任务：

- **一个参数**：查看 `docs/architecture.md` 判断该模块是后端还是前端
  - 后端模块 → 执行「后端模块设计」
  - 前端模块 → 执行「前端整体设计」
- **两个参数**（模块名 + feature 名）→ 执行「前端 feature 级设计」
- **`--summary`** → 执行「汇总补充」

参数值：$ARGUMENTS

---

## 后端模块设计

你是一个软件架构师。请为该后端模块设计内部架构，并同时定义该模块的接口契约。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：该模块的职责定义、依赖关系、跨模块数据流中涉及本模块的部分、接口通用约定）
- docs/prd.md（重点关注：与该模块对应的业务需求部分）
- docs/module-design/（如已有其他模块的设计文件，阅读以了解已定义的接口）

请按照本 skill 目录下的 [backend-module-template.md](backend-module-template.md)，产出 `docs/module-design/{module-name}.md`，包含：

1. 模块概述（职责、PRD 映射）
2. 内部架构（分层结构、控制流）
3. 数据模型（本模块拥有的表/模型，字段、类型、约束）
4. **接口契约** — 本模块的所有接口定义，每个接口包含五要素：
   - 输入（参数/请求体）
   - 输出（响应格式，遵循 architecture.md 的通用约定）
   - 业务规则
   - 错误码
   - **Consumers 字段**（从 architecture.md 的依赖关系中确定消费方）
   另外，如有非 HTTP 暴露的内部接口（用于 Service 层跨模块调用），同样按五要素定义
5. 消费的外部接口（调用哪些其他模块的接口、什么场景下调用）
6. 关键业务逻辑（状态机、计算规则、复杂分支等）
7. 模块特有约定（安全要求、性能约束等）

要求：
- 内部分层遵循 architecture.md 中的目录结构约定
- 数据模型的外键关系如果跨模块，通过接口调用访问，不直接访问其他模块的表
- 接口定义必须与 architecture.md 中"对外接口"一致
- 消费的外部接口必须在 architecture.md 的依赖关系中有体现
- 每个接口的 Consumers 字段不能为空（如果没有外部消费方则标注"仅内部"）
- 错误码在本模块内不重复、含义明确
- 接口格式使用 HTTP REST API
- 不要设计其他模块的内容
- 如果 docs/module-design/ 下已有其他模块的设计文件：
  - 接口风格与已有模块保持一致
  - 消费已有模块的接口时，确认调用方式与已有定义一致
  - 错误码全局不重复（检查已有模块的错误码）
  - 不要修改已有模块的设计文件。如发现不一致，停下来指出问题

---

## 前端整体设计

> 前端模块（web-app、admin）应在所有后端模块设计完成后再设计，因为前端依赖后端接口。
> 前端模块拆为整体文档 + feature 级文档。本任务产出整体文档。

你是一个软件架构师。请为该前端模块设计整体架构。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：前端模块职责、调用的后端模块、Feature 划分）
- docs/prd.md（重点关注：页面功能、用户交互流程、UI 原型图或原型链接）
- docs/module-design/（所有后端模块的设计文件，了解可调用的后端接口）

请按照本 skill 目录下的 [frontend-overall-template.md](frontend-overall-template.md)，产出 `docs/module-design/{module-name}.md`（整体设计文档），包含：

1. 模块概述（职责、PRD 映射、类型标注为"前端模块"）
2. Feature 划分（列出所有 feature 及其包含的页面，说明划分依据）
3. 内部架构（目录结构：features/ + shared/ + stores/ + routes.ts）
4. 路由结构（所有页面的路由表，标注所属 feature）
5. 布局设计（全局布局、导航结构；如 PRD 中有整体布局的 UI 原型，引用原型图路径或链接）
6. 共享层设计：
   - 共享组件（全局复用的 UI 组件）
   - 共享 hooks（认证状态、通用数据获取等）
   - 全局状态管理（Zustand store 设计）
   - API client 配置（基础 URL、拦截器、错误处理）
7. 核心类型定义（跨 feature 共享的类型）
8. 模块特有约定（响应式要求、浏览器兼容、性能约束等）

要求：
- 本文档只设计整体结构和共享层，不设计各 feature 的页面细节
- 各 feature 的详细设计将在独立会话中通过 `/mp-module-design {module-name} {feature}` 产出
- Feature 划分应与后端模块对应（如 auth feature 对应 user 后端模块）
- 如果 admin 页面较少（< 5 个），可以不拆 feature，一个文件写完整体 + 页面细节

---

## 前端 feature 级设计

> 每个 feature 一个独立会话，按迭代需要逐个推进。

你是一个软件架构师。请为该前端模块的指定 feature 设计页面细节。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module-name}.md（整体设计：路由结构、共享层、类型定义）
- docs/module-design/（该 feature 对应的后端模块设计文件，了解可调用的后端接口）
- docs/prd.md（重点关注：与该 feature 相关的页面功能、验收标准、UI 原型图或原型链接）

请按照本 skill 目录下的 [frontend-feature-template.md](frontend-feature-template.md)，产出 `docs/module-design/{module-name}-{feature}.md`，包含：

1. Feature 概述（职责、包含的页面、对应的后端模块）
2. **页面与路由** — 每个页面包含：
   - UI 原型（如 PRD 中有该页面的原型图或原型链接，引用到此处，供实现时参考）
   - 路由路径（与整体设计的路由表一致）
   - 功能描述
   - 页面状态
   - 调用的后端接口（接口名、触发时机、成功/错误处理）
   - 交互流程
   - 组件结构树
3. Feature 私有组件（不在 shared/ 中的组件）
4. Feature 私有 hooks（数据获取、业务逻辑封装）
5. 消费的后端接口汇总（哪些后端接口、什么页面调用）
6. 关键业务逻辑（前端校验规则、权限控制、复杂交互逻辑）

要求：
- 每个页面调用的后端接口必须在对应后端模块的 module-design 中有定义
- 如果发现需要的后端接口不存在，停下来指出缺失
- 如果 PRD 中有该页面的 UI 原型图（图片路径）或原型链接（如 Figma URL），必须在对应页面的「UI 原型」字段中引用，供 Implementer agent 实现时参考
- 页面组件结构树不需要细到每个 HTML 元素，描述到业务组件粒度即可
- 不要设计其他 feature 的内容
- 使用整体设计中定义的共享组件和全局状态，不要重复定义

---

## 汇总补充（--summary）

所有模块设计已完成。请补充 architecture.md 的跨模块汇总部分。

请先阅读以下文件：
- docs/architecture.md
- docs/module-design/（所有模块设计文件）
- docs/prd.md

请在 architecture.md 中补充/完善：

1. **接口通用约定**（如尚未完整定义）— 确认认证方式、响应格式、分页约定、HTTP 状态码
2. **接口依赖矩阵**（接口 × 提供方 × 消费方 × 变更影响级别）— 汇总所有模块的 consumers 字段
3. **需求追溯表**（PRD 每条业务规则/验收标准 → 对应 module-design 中的接口定义）— 确保 PRD 全覆盖
4. **部署概要**（如部署架构影响模块设计）

要求：
- 接口通用约定必须与各模块接口契约的响应格式一致
- 接口依赖矩阵必须完整，覆盖所有跨模块调用
- 需求追溯表中不允许出现"未覆盖"的条目
- 如果发现 PRD 中的功能点/业务规则在已有接口中未覆盖，停下来指出遗漏

完成后更新 `docs/workflow-state.md`：更新模块进度表中对应模块的"设计"列为 `review`；如果是 `--summary` 则设置 `step: 3`，`substep: review`。

> **状态更新边界**：skill 只将状态推进到"等待 review"。Review 通过/不通过的状态转换由技术负责人通过 `/mp-workflow-update` 触发。
