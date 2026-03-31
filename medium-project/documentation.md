# 文档策略

## 文档清单

| 文档 | 谁写 | 谁 Review | 是否必须 |
|------|------|-----------|---------|
| PRD (prd.md) | 产品经理 | 产品经理 | 必须 |
| CLAUDE.md | 技术负责人 + Architect agent | 技术负责人 | 必须 |
| README.md | 技术负责人 | 无需 review | 推荐 |
| 系统架构 (architecture.md) | Architect agent | 技术负责人 | 必须 |
| 模块设计 + 接口契约 (module-design/{module}.md) | Architect agent | 技术负责人 | 必须 |
| GitHub Issues | Architect agent + 技术负责人 | 技术负责人 | 必须 |
| 契约测试 + 集成测试 + E2E 测试 | Tester agent | 技术负责人 | 必须 |
| 单元测试 | Implementer agent | Reviewer agent | 按需 |
| 业务代码 | Implementer agent | Reviewer agent + 技术负责人（跨模块时） | 必须 |

> **CLAUDE.md vs README.md**：CLAUDE.md 面向 AI Agent，包含约定和禁止事项；README.md 面向人类开发者，包含快速上手指南。两者定位不同，不可互相替代。

## 文档分层

### CLAUDE.md 分层

**全局 CLAUDE.md（< 100 行）** — 所有 agent 自动加载：

```markdown
# Project: {项目名}
## 一句话描述
## Tech Stack
## 项目文档
## 常用命令
## 项目结构（只列顶层目录和模块名，不展开）
## 代码规范
## 架构约定
## 测试环境
## Git 规则
## 共享代码修改规则
## 不要做的事
## 错误处理规则
```

### 文档拆分

**architecture.md**：系统级内容（模块划分、依赖关系图、部署架构、跨模块数据流、接口通用约定、接口依赖矩阵、需求追溯表）。

**module-design/{module}.md**：每个模块的内部设计（分层、数据模型）+ 该模块的完整接口契约（五要素）。

### 跨模块 agent 的信息边界

Module-B 的 agent 关于 Module-A **需要知道的**：

- 公开接口签名和返回类型
- 错误码定义
- 相关数据模型

**不需要知道的**：

- 内部实现逻辑、目录结构、单元测试、技术债

这些信息通过 `module-design/{module-a}.md` 中的"接口契约"和"消费的外部接口"部分提供。

## 文档变更传播规则

核心原则：**先更新文档 → 再更新测试 → 最后更新实现。** 按模块依赖顺序处理，被依赖的模块优先。

### 接口契约变更

1. 查看 architecture.md 的**接口依赖矩阵**，识别所有受影响的消费方模块
2. 更新提供方的 module-design/{module}.md 中的接口定义
3. 更新消费方的 module-design 中的"消费的外部接口"
4. 同步更新 architecture.md 的接口依赖矩阵（如影响范围变化）
5. 在受影响模块的 GitHub Issue 中 comment 变更通知
6. Tester agent 新会话更新契约测试
7. 已完成的实现如涉及变更接口，标记 Issue 为"需更新"

### architecture.md 变更

1. 评估是否影响模块划分和依赖关系
2. 更新受影响的 module-design/{module}.md
3. 更新 CLAUDE.md 中的项目结构（如有变化）

### 变更记录

- 在相关 GitHub Issue 中 comment 变更原因和影响范围
- commit message 标注：`docs(<module>): {变更内容}，影响范围: #{issue-list}`
