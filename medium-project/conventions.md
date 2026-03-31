# 开发约定

## Git 策略

### 提交规范

- 直接在 main 分支开发，不使用 feature 分支
- commit 粒度：每个有意义的改动一个 commit
- commit message 格式：`<type>(<module>): <描述为什么改> [#issue-number]`
- type: feat / fix / docs / refactor / test
- 示例：`feat(order): 实现订单创建接口 [#12]`、`fix(infra): 修正错误处理中间件 [#3]`
- 不要把无关改动放在同一个 commit
- Task 标识 `[#issue-number]` 用于 Reviewer agent 定位相关提交

### Task 完成流程

Reviewer 输出 LGTM 后，Task 即视为完成（代码已在 main 上），更新 GitHub Issue 状态即可。

## Review 机制

### 分层 Review

| Review 类型 | 触发时机 | 执行者 | 关注点 |
|------------|---------|--------|--------|
| Task Review | 每个 Task 完成 | Reviewer Agent | 功能正确性、代码规范、测试覆盖 |
| 模块 Review | 模块所有 Task 完成 | Reviewer Agent（模块级 prompt） | 模块内一致性、命名/风格统一、接口覆盖完整性 |
| 跨模块 Review | 涉及跨模块变更时 | 技术负责人 | 接口一致性、依赖方向、infra 修改合理性 |
| 架构 Review | 架构变更提议时 | 技术负责人 | 决策合理性、影响范围 |

**分层原则**：技术负责人只做系统级和跨模块 review，模块内 review 委托 Reviewer Agent。

### Review 输出标准

- **LGTM** — 通过，无需修改
- **MUST FIX** — 必须修复后重新 review
- **SHOULD FIX** — 建议修改，修改后重新 review
- **OPTIONAL** — 可选优化，不阻塞进度

## 会话管理

### 基本原则

**每个角色、每个任务使用独立的新会话。** 不在一个会话中让 agent 切换角色或跨 Task 工作。CLAUDE.md 在每个会话开始时自动加载，是 agent 获取项目上下文的主要入口。

### 上下文加载规则

- **模块 agent 只加载必要文档**：CLAUDE.md + module-design/{module}.md
- 需要了解其他模块接口时，只读对应 module-design 的"接口契约"部分

### 什么时候必须开新会话

1. 切换角色时
2. 切换 Task 时（即使同一角色）
3. Review 不通过需要修复时
4. Agent 表现异常时
