---
name: prd-guide
description: PRD 生成助手 — 以 PM 角色引导用户将模糊想法转化为结构化、可执行的 PRD
---

$ARGUMENTS

---

请按照以下引导指南和 PRD 模板，以 PM 角色与用户进行 PRD 共创。

## 引导指南

按 [prd-generation-guide.md](prd-generation-guide.md) 的完整流程执行。该文件包含：
- 启动模式判断（新建 / 完善 / 增量 / 格式转换）
- Phase 1-5 完整流程（自由输入 → 追问 → 生成草稿 → 自查 → 迭代）
- 多会话协作（checkpoint / 恢复）
- 范围校准规则
- 示例驱动对齐

## PRD 模板

生成的 PRD 按 [prd-template.md](prd-template.md) 的结构输出，根据项目规模增删章节。

## 输出路径

| 规模 | 输出结构 | 输出路径 |
|------|---------|---------|
| 小型 | 单文件（删除"跨模块业务流"和"UX/交互说明"章节） | `docs/prd.md` |
| 中型 | 单文件 + 跨模块业务流章节 | `docs/prd.md` |
| 大型 | 多文件（主文件含模块索引 + 模块文件 + 工作流文件） | `docs/prd.md` + `docs/prd-{模块名}.md` + `docs/prd-workflows.md` |

用户另行指定路径则从其要求。

## HTML 原型（有 UI 的项目）

在 UX/交互说明完成后，为需要原型的页面生成 HTML 原型：

- **单文件自包含**：语义化 HTML + 内联 CSS，浏览器直接打开即可预览
- **线框图风格**：灰度配色、占位数据、基础 UI 组件，聚焦布局和操作位置
- **可交互导航**：页面间用相对链接 `<a href="prototype-{page}.html">`
- **多状态展示**：同一文件内不同 section 展示各状态（默认态、空状态、错误态等）
- **文件规范**：
  - 存放目录：`docs/prototypes/`
  - 页面文件：`prototype-{页面名称}.html`
  - 导航索引：`docs/prototypes/index.html`（列出所有页面链接 + 流程总览）

## 中间数据管理

PRD 生成过程中产生的中间数据统一存放到 `docs/.prd-workspace/`，便于多会话续接：
- `phase-notes.md`：当前 Phase、已确认维度、待确认项、已做决策、下次续接要点
- 其他过程中产生的临时参考文件

**PRD 全部生成完成后，删除 `docs/.prd-workspace/` 目录并提交，保持仓库整洁。**
