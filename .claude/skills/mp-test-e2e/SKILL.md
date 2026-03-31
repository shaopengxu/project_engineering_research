---
name: mp-test-e2e
description: "Medium-project Step 6: 根据 PRD 验收标准编写 E2E 测试"
---

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
