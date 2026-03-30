# GitHub Projects 配置指南

> 本指南用于 Step 1 初始化阶段，由技术负责人完成。

## 1. 创建 GitHub Project

```bash
# 创建 Project（Board 类型）
gh project create --title "{项目名称}" --owner "@me"

# 记录 Project Number（后续命令需要）
gh project list --owner "@me"
```

## 2. 配置自定义字段

在 GitHub Web UI 中操作（Project → Settings → Custom fields）：

| 字段名 | 类型 | 选项 |
|--------|------|------|
| Status | Single select | `Todo`, `In Progress`, `Review`, `Done`, `Blocked` |
| Module | Single select | `shared`, `{module-a}`, `{module-b}`, ... |
| Priority | Single select | `P0`, `P1`, `P2` |

## 3. 创建标签

```bash
# 任务类型标签
gh label create "type:contract-test" --color "1d76db" --description "契约测试任务"
gh label create "type:impl" --color "0e8a16" --description "实现任务"
gh label create "type:integration-test" --color "5319e7" --description "集成测试任务"
gh label create "type:e2e" --color "d93f0b" --description "E2E 测试任务"
gh label create "type:infra" --color "c5def5" --description "基础设施任务"

# 模块标签
gh label create "module:shared" --color "fbca04" --description "共享层"
gh label create "module:{module-a}" --color "f9d0c4" --description "{module-a} 模块"
gh label create "module:{module-b}" --color "c2e0c6" --description "{module-b} 模块"
# ... 为每个模块创建标签
```

## 4. 创建 Milestones（迭代管理）

```bash
# 如果项目需要多迭代
gh api repos/{owner}/{repo}/milestones -f title="Milestone 1: 核心模块" -f description="shared + {核心模块列表}"
gh api repos/{owner}/{repo}/milestones -f title="Milestone 2: 业务模块" -f description="{业务模块列表}"
```

## 5. 配置 Project 视图

在 GitHub Web UI 中操作：

**Board 视图**（默认）：
- 按 Status 字段分列（Todo / In Progress / Review / Done / Blocked）
- 用于日常 Task 状态追踪

**Table 视图**：
- 显示所有字段（Status, Module, Priority）
- 支持按 Module 分组和筛选
- 用于全局进度概览

**Roadmap 视图**（可选）：
- 按 Milestone 组织时间线
- 用于向产品经理展示进度

## 6. Issue 创建模板

### 契约测试 Issue

```bash
gh issue create \
  --title "[{module}] 契约测试: {接口名称}" \
  --label "type:contract-test,module:{module}" \
  --milestone "{milestone}" \
  --project "{project-name}" \
  --body "$(cat <<'EOF'
## 任务描述
为 {接口名称} 编写契约测试。

## 所属模块
{module}

## 依赖
无（契约测试可独立编写）

## 对应契约章节
module-design/{module}.md 中的 "{接口名称}" 章节

## 需通过测试
- [ ] 正常流程测试
- [ ] 异常流程测试（错误码覆盖）
EOF
)"
```

### 实现 Issue

```bash
gh issue create \
  --title "[{module}] 实现: {任务描述}" \
  --label "type:impl,module:{module}" \
  --milestone "{milestone}" \
  --project "{project-name}" \
  --body "$(cat <<'EOF'
## 任务描述
{一句话描述}

## 所属模块
{module}

## 依赖
- Depends on #{issue-number}

## 需通过测试
- [ ] 契约测试: tests/contracts/{module}/{test-file}
- [ ] L1 集成测试: tests/integration/{module}/{test-file}

## 验收标准
- [ ] {criterion 1}
- [ ] {criterion 2}
EOF
)"
```

### 集成测试 Issue

```bash
gh issue create \
  --title "[integration] L2: {关键路径描述}" \
  --label "type:integration-test" \
  --milestone "{milestone}" \
  --project "{project-name}" \
  --body "$(cat <<'EOF'
## 任务描述
验证 {module-a} → {module-b} 的关键路径集成。

## 涉及模块
{module-a}, {module-b}

## 依赖
- Depends on #{module-a-impl-issue}
- Depends on #{module-b-impl-issue}

## 测试路径
tests/integration/paths/{path-name}.test.ts

## 验收标准
- [ ] 真实模块间调用（不 Mock）
- [ ] 覆盖正常流程和关键异常流程
EOF
)"
```

## 7. Agent 与 GitHub Issues 的交互模式

### Agent 报告进度

```bash
# 开始任务时
gh issue comment {NUMBER} --body "开始实现。"

# 完成任务时
gh issue comment {NUMBER} --body "实现完成。所有契约测试通过，L1 集成测试通过。"

# 阻塞时
gh issue comment {NUMBER} --body "阻塞：需要 #{dep-issue} 完成后才能继续。原因: {具体原因}"

# 发现接口问题时
gh issue comment {NUMBER} --body "发现接口需要调整: {描述变更内容和原因}。请技术负责人评估影响范围。"

# 需要 shared 层变更时
gh issue comment {NUMBER} --body "需要新增共享工具函数: {函数描述和用途}。当前已在模块内部临时实现，标注 TODO。"
```

### 技术负责人管理

```bash
# 查看待处理的 Issues
gh issue list --state open --label "type:impl"

# 按模块筛选
gh issue list --state open --label "module:{module-name}"

# 查看阻塞的 Issues
gh issue list --state open --search "阻塞 in:comments"

# 关闭已完成的 Issue
gh issue close {NUMBER} --comment "Review 通过，Task 完成。"
```

