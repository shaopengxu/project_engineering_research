# 任务管理：GitHub Projects

使用 GitHub Projects + GitHub Issues 管理任务：

- **存储与状态追踪**：GitHub Issues，无并发瓶颈
- **依赖关系**：Issue body 中 `Depends on #N` + Sub-issues
- **程序化访问**：`gh` CLI + GraphQL API，AI agent 可直接操作
- **可视化**：Board（看板）/ Table（表格）/ Roadmap（时间线）视图
- **状态更新**：通过标签、Project 字段、Issue Comment

## GitHub Project 配置

**Project 自定义字段**：

| 字段 | 类型 | 选项 |
|------|------|------|
| Status | 单选 | Todo, In Progress, Review, Done, Blocked |
| Module | 单选 | infra, {module-a}, {module-b}, web-app, admin, ... |
| Priority | 单选 | P0, P1, P2 |

**Issue 标签**：

| 标签 | 用途 |
|------|------|
| `type:contract-test` | 契约测试任务 |
| `type:impl` | 实现任务 |
| `type:integration-test` | 集成测试任务 |
| `type:e2e` | E2E 测试任务 |
| `type:infra` | 基础设施任务 |
| `module:{name}` | 所属模块 |

**Issue body 模板**：

```markdown
## 任务描述
{一句话描述}

## 所属模块
{module name}

## 依赖
- Depends on #{issue-number}

## 需通过测试
- [ ] 契约测试: {test file/suite}
- [ ] L1 集成测试: {if applicable}

## 验收标准
- [ ] {criterion 1}
- [ ] {criterion 2}
```

## Agent 与 GitHub Issues 的交互

**技术负责人操作**：

```bash
# 创建 GitHub Project
gh project create --title "{项目名}" --owner "@me"

# 批量创建 Issues
gh issue create --title "[infra] 初始化基础设施" \
  --body "..." --label "type:infra,module:infra" \
  --project "{项目名}"

gh issue create --title "[user] 实现用户注册接口" \
  --body "Depends on #1\n..." --label "type:impl,module:user" \
  --project "{项目名}"

# 查看项目进度
gh issue list --state open --label "module:user"
```

**Agent 操作**：

```bash
# 报告任务完成
gh issue comment {NUMBER} --body "实现完成。所有契约测试通过，L1 集成测试通过。"

# 报告阻塞
gh issue comment {NUMBER} --body "阻塞：需要 #{dep-issue} 的接口完成后才能继续。"

# 报告接口变更需求
gh issue comment {NUMBER} --body "发现接口需要调整：{描述变更}。请技术负责人评估影响范围。"
```

**状态管理原则**：Agent 通过 Issue comment 报告进展，**技术负责人负责更新 Project Board 状态**。

## 依赖关系管理

**依赖声明**：Issue body 中用 `Depends on #N` 标注前置依赖。

**Sub-issues 层级**：将模块的多个 Task 组织为父子关系：

```
#10 [user] 用户模块实现                ← 父 Issue（模块粒度）
  ├── #11 [user] 实现 repository 层
  ├── #12 [user] 实现 service 层      ← Depends on #11
  └── #13 [user] 实现 controller 层   ← Depends on #12
```
