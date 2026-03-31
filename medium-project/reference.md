# 速查与参考

## 每步的输入、产出与退出标准

| Step | 执行者 | 输入 | 产出 | 退出标准 |
|------|--------|------|------|---------|
| 1 | 人 + Architect | — | PRD, CLAUDE.md（基础）, GitHub Project | PRD 按模块组织含验收标准；CLAUDE.md 基础部分确认；Project 已创建 |
| 2 | Architect | PRD, CLAUDE.md | architecture.md | 模块划分清晰；依赖单向无环；数据流完整 |
| 3 | Architect | architecture.md, PRD | module-design/*.md | 每模块内部设计 + 接口契约完整；数据模型清晰 |
| 4 | Architect | 架构 + 模块设计 | 脚手架, Issues | 脚手架能运行；Issues 含依赖关系 |
| 5 | Tester + Impl + Reviewer | module-design + 测试 | 契约测试 + 业务代码 + L1/L2 集成测试 | 按模块串行：契约测试通过 → L1 通过 → 模块 Review 通过 → L2 通过 |
| 6 | Tester + 技术负责人 | PRD 验收标准 | E2E 测试, README.md | 核心路径 E2E 通过；README.md 完成 |
| 7 | 产品经理 | PRD | 验收确认 | 分批验收全部通过 |

## 常见故障与恢复

### Agent 会话崩溃

1. 检查 git 状态：`git status` + `git log` 确认最后 commit
2. 有未提交的改动且质量可接受 → 提交后新会话继续
3. 有未提交的改动但质量不确定 → `git stash`，新会话重新开始
4. 无未提交改动 → 新会话重新开始

### 实现过程中发现架构有问题

1. Agent 停止实现，在 Issue comment 中报告
2. 技术负责人评估影响范围
3. 回退到 Step 2/3：新会话修订架构文档
4. 按变更传播规则：文档 → 测试 → 实现

### infra 变更需求

1. Implementer agent 在 Issue comment 中说明需求
2. 技术负责人评估后确认或拒绝

### Agent 产出质量不达标

1. 给出具体修改要求（引用 Issue 编号、契约章节、代码行号）
2. 反复出现同类问题 → 在 CLAUDE.md 中增加针对性约束
3. 质量仍不达标 → 将 Task 拆得更小，或技术负责人手动完成关键部分

## CI 集成建议

### 流水线策略

```
每次 push 到 main:
  lint + 全量契约测试 + 单元测试 + L1/L2 集成测试

定期 / 手动触发:
  全量测试 + E2E 测试
```

### GitHub Actions 示例

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

> 以上为 Node.js 项目示例。其他技术栈替换对应的 setup 和命令即可。测试命令应只运行已完成 Task 的测试（通过测试目录或标签过滤）。
