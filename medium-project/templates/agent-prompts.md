# Agent Prompt 模板（中型项目）

以下是各角色 agent 在每个阶段的提示词模板。
架构设计分为两步（Step 2 系统架构 + Step 3 模块设计），模块级上下文加载、GitHub Issues 交互。串行推进，无需 Worktree 或分支管理。

---

## Step 1 — Architect Agent（CLAUDE.md 基础部分）

在新会话中使用：

```
你是一个软件架构师。请根据 PRD 给出 CLAUDE.md 基础部分的建议。

请先阅读以下文件：
- docs/prd.md

请按 CLAUDE.md 模板格式（参考 medium-project/templates/CLAUDE.md），填写以下章节：
- 一句话描述（从 PRD 的核心价值提炼）
- Tech Stack（使用固定技术栈：TypeScript 全栈，后端 Express + Prisma + PostgreSQL，前端 React + Vite + React Router + Ant Design + TanStack Query + Zustand，测试 Vitest + React Testing Library）
- 项目文档（固定链接：docs/prd.md, docs/architecture.md, docs/module-design/, GitHub Projects）
- 代码规范（ESLint + Prettier，文件 kebab-case，组件 PascalCase）
- Git 规则（使用标准模板，commit 格式为 `<type>(<module>): <描述>`）
- 共享代码修改规则（使用标准模板）
- 不要做的事（根据 PRD 的"不在范围内"提炼禁止事项）
- 错误处理规则（使用标准模板）

要求：
- 以下章节留空，由后续步骤补充：项目结构、架构约定、常用命令、测试环境
- 技术栈已固定，直接使用，不需要选择理由
- 不要创建项目文件或安装依赖，只产出 CLAUDE.md 文件
```

---

## Step 2 — Architect Agent（系统架构设计）

在新会话中使用：

```
你是一个软件架构师。请根据 PRD 设计系统级架构。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md

请产出 architecture.md（参考 medium-project/templates/architecture.md），包含：

1. 技术选型（使用固定技术栈，确认写入 architecture.md）
2. 模块划分：
   - 列出所有模块（业务模块 + 技术模块），每个模块一句话职责
   - 业务模块与 PRD 的映射关系
   - 每个模块的边界和对外接口（接口名称级别，不需要完整定义）
   - infra 的职责边界
3. 模块依赖关系：
   - 依赖关系图（ASCII 图）
   - 依赖矩阵（每个模块依赖谁、被谁依赖）
   - 依赖规则（单向无环，循环依赖的解耦策略）
4. 跨模块数据流：
   - 关键业务路径的调用链
   - 事件流（如有异步通信）
5. 目录结构
6. 数据模型概览（只列跨模块关系的模型）
7. 关键架构决策
8. 接口通用约定：
   - 认证方式
   - 响应格式（成功/失败统一结构）
   - 分页约定
   - HTTP 状态码约定
9. 部署概要（可选，如部署架构影响模块设计则必须说明）

同时补充 CLAUDE.md：
- 项目结构（只列顶层目录和模块名）
- 架构约定（从模块依赖关系和设计决策中提炼）
- 不要做的事（补充架构相关禁止事项）

要求：
- 只做系统级设计，不设计模块内部结构（内部设计在后续会话中由独立的 Architect 完成）
- 模块间依赖方向单向，不能有循环
- 业务模块数量应在 4-8 个之间，如果超出建议调整粒度
- 每个模块的职责能用一句话说清
- 不要过度设计
```

---

## Step 3 — Architect Agent（模块详细设计 + 接口契约）

**每个模块一个独立会话**，按依赖顺序串行推进。在新会话中使用：

### 后端模块会话

```
你是一个软件架构师。请为 {模块名} 设计内部架构，并同时定义该模块的接口契约。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：{模块名} 的职责定义、依赖关系、跨模块数据流中涉及本模块的部分、接口通用约定）
- docs/prd.md（重点关注：与 {模块名} 对应的业务需求部分）
- docs/module-design/（如已有其他模块的设计文件，阅读以了解已定义的接口）

请产出 module-design/{module-name}.md（参考 medium-project/templates/module-design.md），包含：

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
```

### 前端模块会话

> 前端模块（web-app、admin）应在所有后端模块设计完成后再设计，因为前端依赖后端接口。

```
你是一个软件架构师。请为前端模块 {模块名} 设计内部架构。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：前端模块职责、调用的后端模块）
- docs/prd.md（重点关注：页面功能、用户交互流程、UI 相关的验收标准）
- docs/module-design/（所有后端模块的设计文件，了解可调用的后端接口）

请产出 module-design/{module-name}.md（参考 medium-project/templates/module-design.md 的前端模块部分），包含：

1. 模块概述（职责、PRD 映射、类型标注为"前端模块"）
2. 内部架构（目录结构：pages / components / hooks / api / stores / routes）
3. 核心类型定义和状态管理（页面状态、全局状态、持久化状态）
4. **页面与路由** — 每个页面包含：
   - 路由路径
   - 功能描述
   - 页面状态
   - 调用的后端接口（接口名、触发时机、成功/错误处理）
   - 交互流程
   - 组件结构树
5. 消费的后端接口汇总（哪些后端接口、什么页面调用）
6. 关键业务逻辑（前端校验规则、权限控制、复杂交互逻辑）
7. 模块特有约定（响应式要求、浏览器兼容、性能约束等）

要求：
- 每个页面调用的后端接口必须在对应后端模块的 module-design 中有定义
- 如果发现需要的后端接口不存在，停下来指出缺失
- 页面组件结构树不需要细到每个 HTML 元素，描述到业务组件粒度即可
- 不要设计其他模块的内容
```

### 最后一个模块完成后（同一会话或新会话）

```
所有模块设计已完成。请补充 architecture.md 的跨模块汇总部分：

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
```

---

## Step 4 — Architect Agent（脚手架 + 任务拆分 + GitHub Issues）

在新会话中使用：

```
你是一个软件架构师。请根据架构文档初始化项目脚手架、拆分任务、创建 GitHub Issues。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md
- docs/module-design/（所有模块设计文件）

请完成以下工作：

1. 项目脚手架初始化：
   - 根据 architecture.md 的目录结构创建项目框架
   - 安装依赖、配置构建工具、测试框架、lint
   - 配置 TypeScript（根目录 tsconfig.json + 各端独立 tsconfig）
   - 创建 `.env.example`（DATABASE_URL、PORT 等必需环境变量），`.env` 加入 `.gitignore`
   - 为每个后端模块创建**导出桩文件**（只声明函数签名，函数体 `throw new Error('Not implemented')`）
   - 确保安装、lint、测试框架启动命令都能成功

2. 创建 GitHub Issues：
   - 契约测试任务：每个模块的接口契约对应契约测试 Issue
   - 实现任务：按模块拆分，每个 Issue 标注依赖（Depends on #N）和需通过的测试
   - 集成测试任务：为 architecture.md 中的每条关键路径创建 L2 集成测试 Issue
   - 使用标签：type:contract-test / type:impl / type:integration-test / type:e2e / type:infra + module:{name}
   - 使用 Milestone 标注迭代（如需多迭代）

3. 回填 CLAUDE.md：
   - 常用命令（与实际脚手架配置一致）
   - 测试环境（隔离方式、环境变量）

任务拆分原则：
- infra 独立为最高优先级 Task
- 每个业务模块可拆为 2-6 个 Task（按层或按功能拆分）
- 单个 Task: < 15 个文件、< 500 行改动、一句话可描述、单会话可完成
- Task 间依赖标注为 DAG（在 Issue body 中声明 Depends on）
- 如果拆不到粒度，停下来说明问题

要求：
- 不要写业务代码和测试代码
- 脚手架完成后 commit，GitHub Issues 创建后在 commit message 中记录
```

---

## Step 5 — 按模块串行：契约测试 → 实现 → Review

执行顺序：infra（使用 5a prompt）→ 后端模块（使用 5b + 5d-5h）→ 前端模块（使用 5c + 5d-5h）。
每个模块按以下顺序完成后，再推进下一个模块。

### 5a. Implementer Agent（infra 实现）

infra 模块不走契约测试流程，直接实现。在新会话中使用：

```
你是一个开发工程师。请实现 infra 基础设施模块。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：技术选型、目录结构、接口通用约定）

请完成以下基础设施：

1. 数据库连接：
   - Prisma Client 初始化和导出
   - 根据 module-design 中的数据模型创建 prisma/schema.prisma
   - 运行 `npx prisma migrate dev --name init` 创建初始 migration

2. 配置管理：
   - 环境变量加载（dotenv）
   - 创建 .env.example（DATABASE_URL、PORT 等）
   - .env 加入 .gitignore

3. 全局错误处理中间件：
   - 统一错误捕获和格式化
   - 错误响应遵循 architecture.md 的响应格式约定

4. 标准响应格式工具函数：
   - 成功响应和错误响应的格式化函数
   - 遵循 architecture.md 的响应格式约定

5. 通用中间件：
   - 认证中间件（如 architecture.md 中有定义）
   - 请求日志中间件

6. Express 应用初始化（server/app.ts）

验收标准：
- `npm install` 成功
- `npm run lint` 通过
- `npm run dev:server` 能启动（即使没有业务路由）
- 数据库连接成功
- 错误处理中间件可用

要求：
- 每个有意义的改动 commit 一次，commit message 包含 `[#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "infra 实现完成"` 报告
```

---

### 5b. Tester Agent（后端模块契约测试）

**每个模块一个独立会话**，按依赖顺序串行推进。在新会话中使用：

```
你是一个测试工程师。请为后端模块 {模块名} 编写契约测试。

契约测试的目的是：验证接口的输入输出是否符合接口契约的定义。
这些测试将在实现之前编写，作为 TDD 的驱动力。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（重点关注：接口契约部分 + 数据模型）
- server/modules/{module}/index.ts（导出桩文件，确认可用的函数签名）

要求：
- 每个接口的每条业务规则至少一个测试用例
- 包含正常流程和异常流程（错误码全覆盖）
- 测试之间互相独立，不依赖执行顺序
- 每个测试用例用注释标注对应的业务规则来源
- 测试代码放在 tests/contracts/{module}/ 目录下
- 此阶段只写契约测试，不写业务代码
- 如果接口契约有模糊或矛盾之处，停下来指出问题，不要自行假设
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "契约测试编写完成"` 报告

注意：你只需要阅读本模块的设计文档（module-design/{module}.md），不需要阅读其他模块的文档。
```

### 5b. Tester Agent（前端模块测试）

**每个前端模块一个独立会话**，在所有依赖的后端模块完成后执行。在新会话中使用：

```
你是一个测试工程师。请为前端模块 {模块名} 编写测试。

前端测试包含两部分：
1. **API 调用层测试**：验证 api/ 层的请求参数和响应处理与 module-design 中后端接口定义一致
2. **页面渲染测试**：验证页面组件能正确渲染 mock 数据并响应用户交互

这些测试将在实现之前编写，作为 TDD 的驱动力。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（重点关注：页面与路由、调用的后端接口、交互流程）
- docs/module-design/（已完成的后端模块设计文件，了解后端接口定义）

要求：

API 调用层测试：
- 每个后端接口调用验证请求 URL、HTTP 方法、请求参数格式
- 验证响应数据的解析和转换逻辑
- 验证错误响应的处理（对照后端接口的错误码）
- 使用 MSW（Mock Service Worker）或手动 mock 拦截 HTTP 请求
- 测试代码放在 tests/contracts/{module}/ 目录下

页面渲染测试：
- 每个页面至少一个渲染测试（使用 React Testing Library）
- 验证关键用户交互（按钮点击、表单提交、列表渲染）
- Mock 所有 API 调用（通过 mock hooks 或 MSW）
- 测试代码放在 tests/contracts/{module}/ 目录下

通用要求：
- 测试之间互相独立，不依赖执行顺序
- 每个测试用例用注释标注对应的 module-design 来源
- 此阶段只写测试，不写业务代码
- 如果 module-design 有模糊或矛盾之处，停下来指出问题
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "前端测试编写完成"` 报告
```

---

### 5c. Implementer Agent（实现）

在新会话中使用：

```
你是一个开发工程师。请完成以下 Task。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（本模块的设计 + 接口契约）

当前 Task：
- Issue: #{issue-number}
- 描述: {任务描述}
- 涉及模块: {模块名}
- 契约测试: tests/contracts/{module}/{test-file}

要求：
- 让相关契约测试全部通过
- 编写 L1 集成测试，放在 tests/integration/{module}/ 下：
  - 后端模块：controller → service → repository 真实串联
  - 前端模块：页面 → hooks → API 层串联（mock 后端 API）
- 遵守 CLAUDE.md 中的规范
- 不要修改契约测试代码。如果发现不一致，在 Issue comment 中指出具体矛盾，等待确认
- 不要实现当前 Task 以外的功能
- 不要修改其他模块目录下的文件
- 修改共享代码（infra/、共享类型、共享工具）前，先在 Issue comment 中说明需求，获得技术负责人确认后再修改
- 对复杂内部逻辑补充单元测试
- 每个有意义的改动 commit 一次，commit message 格式：`<type>(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "实现完成，契约测试和 L1 集成测试全部通过"` 报告
```

---

### 5d. Reviewer Agent（Task Review）

每个 Task 完成后触发。在新会话中使用：

```
你是一个代码审查工程师。请 review 当前 Task 的改动。

当前 Task：
- Issue: #{issue-number}
- 描述: {任务描述}
- 涉及模块: {模块名}

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md（本模块设计 + 接口契约）

然后定位当前 Task 的代码改动：
1. 运行 `git log --oneline --all` 查看提交历史
2. 找到 commit message 中包含 `[#{issue-number}]` 的所有提交
3. 对这些提交运行 `git diff <first-commit>^..<last-commit>` 查看完整改动
只 review 当前 Task 涉及的改动，不要评审其他 Task 的代码。

检查清单：
1. 功能是否符合 module-design/{module}.md 中当前 Task 对应接口的定义
2. L1 集成测试是否覆盖了真实串联（后端：controller→service→repository；前端：页面→hooks→API）
3. 是否遵守 CLAUDE.md 的规范
4. 模块间依赖方向是否正确（不反向依赖）
5. 是否有安全问题（SQL 注入、XSS、敏感信息泄露等）
6. 是否违反了共享代码修改规则（修改 infra/ 等共享代码前是否获得确认、不应修改其他模块文件）
7. 实现质量 — 明显的性能问题、未处理的边界条件、过度设计

输出格式：
- MUST FIX: 功能错误、安全问题、违反共享代码规则
- SHOULD FIX: 违反约定、缺少测试
- OPTIONAL: 建议优化
- 如果没有 MUST FIX 和 SHOULD FIX，输出 "LGTM"

输出结尾建议：在 Issue #{issue-number} 中 comment Review 结果。
```

---

### 5e. Implementer Agent（Review 修复）

当 Reviewer 输出 MUST FIX 或 SHOULD FIX 后。在新会话中使用：

```
你是一个开发工程师。请根据 Review 反馈修复问题。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md

当前 Task：
- Issue: #{issue-number}
- 涉及模块: {模块名}
- 契约测试: tests/contracts/{module}/{test-file}

Review 反馈：
{粘贴 Reviewer Agent 输出的完整 Review 结果}

要求：
- 逐条修复 MUST FIX 和 SHOULD FIX
- 修复后确保所有契约测试和 L1 集成测试仍然通过
- 不要修改契约测试代码。如果认为 Review 反馈与契约矛盾，在 Issue comment 中指出
- 不要修复 OPTIONAL 条目，除非修复成本极低
- 不要趁修复之机重构 Review 未提及的代码
- 每个有意义的改动 commit 一次，commit message 格式：`fix(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "Review 问题已修复"` 报告
```

---

### 5f. Reviewer Agent（模块 Review）

模块所有 Task 完成后触发。在新会话中使用：

```
你是一个代码审查工程师。请对 {模块名} 模块进行整体 Review。

该模块的所有 Task 已逐个 Review 通过。本次 Review 关注模块级的一致性和完整性。

请先阅读以下文件：
- CLAUDE.md
- docs/module-design/{module}.md

然后阅读该模块的全部源代码：server/modules/{module}/（后端模块）或 {web|admin}/（前端模块）

检查清单：
1. 模块内命名风格是否一致（变量、函数、文件命名）
2. 错误处理方式是否统一（错误码格式、异常抛出方式）
3. module-design/{module}.md 中的所有接口是否都已实现
4. 模块内各层职责是否清晰（controller 不含业务逻辑、repository 不含校验逻辑等）
5. 是否有跨层泄漏（如 controller 直接调用 repository）
6. 是否有不必要的代码重复
7. CLAUDE.md 中的约定是否都被遵守

输出格式（同 Task Review）：
- MUST FIX / SHOULD FIX / OPTIONAL / LGTM
```

---

### 5g. Implementer Agent（L2 关键路径集成测试）

当前模块完成模块级 Review 且被依赖模块已实现完成后，开独立会话。在新会话中使用：

```
你是一个开发工程师。请编写跨模块集成测试。

请先阅读以下文件：
- CLAUDE.md
- docs/architecture.md（重点关注：跨模块数据流 > {关键路径名称}）
- docs/module-design/（涉及模块的接口定义）

当前 Task：
- Issue: #{issue-number}
- 关键路径: {描述，如: 用户下单 → 扣减库存 → 创建支付单}
- 涉及模块: {module-a}, {module-b}, {module-c}

要求：
- 在 tests/integration/paths/ 目录下创建集成测试文件
- 使用真实的模块间调用（不 Mock 其他模块）
- 外部依赖（数据库等）使用测试环境（内存数据库或测试容器）
- 覆盖关键路径的正常流程和关键异常流程
- 每个测试用例标注对应的业务路径
- 每个有意义的改动 commit 一次，commit message 格式：`test(<module>): <描述> [#issue-number]`
- 完成后用 `gh issue comment {ISSUE_NUMBER} --body "L2 集成测试完成"` 报告
```

---

## Step 6 — Tester Agent（E2E 测试）

在新会话中使用：

```
你是一个测试工程师。请根据 PRD 验收标准编写 E2E 测试。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md（重点关注：每个模块的验收标准）
- docs/architecture.md（了解系统入口和整体流程）

要求：
- 每条 PRD 验收标准至少一个 E2E 测试用例
- 覆盖核心用户流程（从用户操作到最终结果的完整链路）
- 测试用例用注释标注对应的 PRD 验收标准
- E2E 测试放在 tests/e2e/ 目录下
- 不要重复契约测试和集成测试已覆盖的内容，聚焦于端到端完整流程
- 使用真实依赖（不 Mock）
```

---

## 通用：Agent 遇到阻塞时的处理

所有 agent 在遇到以下情况时，应停止当前工作并通过 `gh issue comment` 报告：

1. **文档矛盾或模糊** — 指出具体哪两处矛盾，不要自行假设
2. **依赖未就绪** — 说明依赖什么、当前状态是什么
3. **需要修改 infra/** — 说明需要什么、用途是什么，等技术负责人处理
4. **发现接口需要变更** — 描述变更内容和原因，等技术负责人评估影响范围
5. **同一问题修改超过 2 次未解决** — 停止，分析根本原因，给出不同方案
6. **超出当前 Task 范围** — 说明哪些工作超出范围，等待确认

---

## 技术负责人操作指南

### Review 深度分级

| Task 类型 | Review 深度 | 重点关注 |
|-----------|-----------|---------|
| 基础设施（infra） | 快速扫描 | 配置正确、依赖合理、能跑通 |
| 核心业务模块 | 逐条对照契约 | 业务规则覆盖、错误处理、边界条件 |
| 跨模块交互 | 重点检查 | 依赖方向、接口一致性、数据流转 |
| 模块级 Review | 一致性检查 | 命名风格、错误处理方式、职责分层 |

**可"信任 Agent + 测试"的场景**：简单 CRUD、测试全部通过且 Agent 未报告异常。
**必须人工逐行过的场景**：安全相关、复杂业务规则、跨模块数据一致性。

### Step 2 架构 Review Checklist

```
- [ ] 模块划分符合单一职责，每个模块职责一句话说清
- [ ] 模块间依赖方向单向，无循环依赖
- [ ] 业务模块数量在 4-8 个（过多需拆迭代、过少则本流程过重）
- [ ] 关键业务路径的数据流完整
- [ ] infra 职责边界明确
- [ ] 跨模块数据关系清晰（关联管理方、外键策略）
- [ ] 架构决策有理由说明
- [ ] 接口通用约定已定义（认证、响应格式、分页、状态码）
- [ ] 部署概要已说明（如影响模块设计）
```

### Step 3 模块设计 + 接口契约 Review Checklist

```
模块设计：
- [ ] 内部分层符合 architecture.md 约定
- [ ] 数据模型完整（字段、类型、约束）
- [ ] 公开接口清单与 architecture.md 一致
- [ ] 消费的外部接口在依赖关系中有体现
- [ ] 关键业务逻辑有详细说明（状态机、计算规则等）
- [ ] 没有设计其他模块的内容

接口契约（每个模块完成后检查）：
- [ ] 每个接口都有完整的五要素（输入、输出、业务规则、错误码、consumers）
- [ ] 接口签名与 module-design 中"公开接口清单"一致
- [ ] 错误码全局不重复（与已有模块不冲突）
- [ ] 接口风格与已有模块一致（遵循通用约定）

所有模块完成后检查：
- [ ] 需求追溯表中列出了 PRD 的每条业务规则和验收标准（无遗漏）
- [ ] 每一行的"对应契约章节"都已填写（不允许为空）
- [ ] 抽查 3-5 条：翻到对应契约章节，确认规则完整描述
- [ ] 接口依赖矩阵完整，覆盖所有跨模块调用
```

### Step 4 脚手架 + Issues Review Checklist

```
脚手架：
- [ ] 依赖安装成功
- [ ] lint 命令能跑通
- [ ] 测试框架能启动
- [ ] 后端模块导出桩文件存在且函数签名与 module-design 中的接口契约一致
- [ ] .env.example 已创建，.env 已加入 .gitignore
- [ ] TypeScript 配置正确（根目录 + 各端独立 tsconfig）

GitHub Issues：
- [ ] 每个接口都有对应的契约测试 Issue
- [ ] 每个实现 Issue 标注了依赖（Depends on #N）
- [ ] 每个实现 Issue 标注了需通过的测试
- [ ] 共享层任务优先级最高
- [ ] 关键路径有 L2 集成测试 Issue
- [ ] Issues 按依赖顺序可串行推进
- [ ] 标签（type + module）正确
```

### Step 5 测试 Review Checklist

```
- [ ] 每条业务规则有对应测试用例（对照 module-design 接口契约逐条检查）
- [ ] 覆盖正常流程和异常流程（错误码全覆盖）
- [ ] 测试独立（无共享状态、不依赖执行顺序）
- [ ] 测试注释标注了业务规则来源
- [ ] Mock/Stub 使用符合 workflow.md Mock 策略
- [ ] 测试能编译/加载（允许执行失败）
```

### Step 5 Task 流转管理

```
每个 Task Review 通过后：
- [ ] 更新 GitHub Issue 状态（关闭 Issue 或移动到 Done）
- [ ] 检查是否解锁了下游依赖任务
- [ ] 如果涉及文档变更，按变更传播规则处理
- [ ] 如果模块所有 Task 完成，触发模块级 Review

模块完成时：
- [ ] 确认该模块所有 Task 已完成
- [ ] 触发模块级 Review
- [ ] 如有跨模块依赖且被依赖模块已完成，触发 L2 集成测试（独立会话）
- [ ] 跑全量测试确认无回归
```

### infra 变更处理

```
收到 Agent 的 infra 变更请求时：
1. 评估需求，确认后允许修改
2. 修改后确认：
   - [ ] 不影响已有模块
   - [ ] 后续 Task 自动使用最新代码
```

### 接口变更处理

```
收到 Agent 的接口变更请求时：
1. 查看 architecture.md 的接口依赖矩阵，确定消费方
2. 评估变更影响：
   - [ ] 变更是否向后兼容？
   - [ ] 影响了哪些模块的契约测试？
   - [ ] 影响了哪些模块的已完成实现？
3. 更新文档：
   - [ ] 更新提供方的 module-design/{module}.md 接口契约
   - [ ] 更新消费方的 module-design 中的"消费的外部接口"
   - [ ] 同步更新 architecture.md 的接口依赖矩阵（如影响范围变化）
4. 通知受影响模块：
   - [ ] 在受影响模块的 Issue 中 comment 变更通知
   - [ ] 后续 Task 使用最新文档
5. 按变更传播规则执行：文档 → 测试 → 实现
```
