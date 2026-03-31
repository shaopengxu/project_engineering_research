---
context: fork
name: mp-test-e2e
description: "Medium-project Step 6: 根据 PRD 验收标准编写 E2E 测试"
---

你是一个测试工程师。请根据 PRD 验收标准编写 E2E 测试。

请先阅读以下文件：
- CLAUDE.md
- docs/prd.md（重点关注：每个模块的验收标准）
- docs/architecture.md（了解系统入口、整体流程、技术选型中的 E2E 测试工具）

使用 **Playwright**（或 architecture.md 技术选型中指定的 E2E 工具）编写浏览器级端到端测试。

要求：
- 测试启动前先执行 `npx prisma db seed` 填充基础数据（确保 `prisma/seed.ts` 中已包含所需的种子数据，不足则补充）
- 每条 PRD 验收标准至少一个 E2E 测试用例
- 覆盖核心用户流程（从用户操作到最终结果的完整链路）
- 测试用例用注释标注对应的 PRD 验收标准
- E2E 测试放在 tests/e2e/ 目录下
- 不要重复契约测试和集成测试已覆盖的内容，聚焦于端到端完整流程
- 使用真实依赖（不 Mock）
- 测试启动前确保前后端服务已运行

如果有测试用例未通过，在输出中列出每个失败用例并归类原因：
- **测试代码问题**：选择器、时序、断言错误 — 标注具体文件和行号
- **种子数据不足**：缺少必要的基础数据 — 标注需要补充的 fixture
- **疑似业务 bug**：标注涉及的模块和接口，供技术负责人决定修复路径

完成后更新 `docs/workflow-state.md`：设置 `step: 6`，`substep: review`。
