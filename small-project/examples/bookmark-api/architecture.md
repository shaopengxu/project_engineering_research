# Bookmark API 架构文档

## 1. 技术选型

| 类别 | 选择 | 理由 |
|------|------|------|
| 语言 | TypeScript 5 | 类型安全，开发效率高，生态成熟 |
| 运行时 | Node.js 20 | LTS 版本，稳定且支持最新 ES 特性 |
| 框架 | Express | 社区最成熟的 Node.js HTTP 框架，中间件生态丰富，学习成本低 |
| 数据库 | SQLite (better-sqlite3) | 零配置，单文件存储，适合个人工具场景，同步 API 编码简单 |
| 测试 | Vitest + Supertest | Vitest 原生 TypeScript 支持且速度快；Supertest 是 Express 测试的事实标准 |
| 构建 | tsup | 零配置打包 TypeScript 项目，输出 ESM 格式 |

## 2. 模块划分

### 2.1 技术模块定义

#### bookmark
- **职责**: 实现书签的增删改查业务逻辑，管理书签与标签的关联关系
- **边界**: 包含书签 CRUD 和书签-标签关联的所有逻辑；不负责标签本身的管理（创建、删除标签）
- **对外接口**:
  - Controller: `POST /bookmarks`, `GET /bookmarks`, `GET /bookmarks/:id`, `PUT /bookmarks/:id`, `DELETE /bookmarks/:id`, `POST /bookmarks/:id/tags`, `DELETE /bookmarks/:id/tags/:tagId`
  - Service: `createBookmark(data)`, `getBookmarks(query)`, `getBookmarkById(id)`, `updateBookmark(id, data)`, `deleteBookmark(id)`, `addTagToBookmark(bookmarkId, tagId)`, `removeTagFromBookmark(bookmarkId, tagId)`

#### tag
- **职责**: 实现标签的创建、查询和删除业务逻辑
- **边界**: 只负责标签本身的 CRUD；不负责书签-标签关联（关联逻辑归属 bookmark 模块）
- **对外接口**:
  - Controller: `POST /tags`, `GET /tags`, `DELETE /tags/:id`
  - Service: `createTag(data)`, `getTags()`, `deleteTag(id)`

#### shared + infra
- **职责**: 提供共享类型与工具函数（shared/）以及数据库连接、错误处理中间件、统一响应格式、应用配置（infra/）。这是 src/ 下两个平级目录共同构成的基础设施层
- **边界**: 只放被多个模块共享的基础设施代码，不包含任何业务逻辑
- **对外接口**: `getDb()`, `AppError` 类, `errorHandler` 中间件, `successResponse()` / `errorResponse()` 辅助函数, `config` 配置对象

### 2.2 业务模块与技术模块映射

| 业务模块（PRD） | 技术模块 | 说明 |
|----------------|---------|------|
| 书签管理 | bookmark, shared + infra | bookmark 负责业务逻辑，shared + infra 提供数据库和中间件 |
| 标签管理 | tag, bookmark, shared + infra | tag 负责标签 CRUD；bookmark 负责书签-标签关联；shared + infra 提供基础设施 |

### 2.3 模块依赖关系

```
shared + infra（无依赖）
  ↑          ↑
bookmark    tag（各自依赖 shared + infra，互不直接依赖）
```

- bookmark 和 tag 都依赖 shared + infra 获取数据库连接和工具函数
- bookmark 和 tag 之间不直接互相调用，通过 bookmark_tag 关联表在数据库层面交互
- 书签-标签关联的业务逻辑（添加标签、移除标签）放在 bookmark 模块中
- 删除标签时，bookmark_tag 表中的关联记录通过 ON DELETE CASCADE 自动清除，tag 模块无需显式处理

### 2.4 共享层准入规则

shared/ 目录的准入标准：
- 只放被 **2 个以上模块** 使用的工具函数和类型定义
- 不放业务逻辑（业务逻辑应归属到具体业务模块）
- 每个文件 < 100 行，超过时应考虑拆分或归属到具体模块
- 新增 shared 内容时在 commit message 中说明被哪些模块使用

当前 shared + infra 包含的内容：
- `database.ts` — SQLite 连接初始化和表创建（bookmark、tag 模块都需要）
- `error.ts` — AppError 自定义错误类和错误处理中间件（所有 controller 都需要）
- `response.ts` — 统一响应格式辅助函数（所有 controller 都需要）
- `config.ts` — 应用配置（端口号、数据库路径等）
- `types.ts` — 共享类型定义（分页参数、统一响应结构等）

## 3. 目录结构

```
bookmark-api/
├── CLAUDE.md
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── api-contracts.md
│   └── task-board.md
├── src/
│   ├── modules/
│   │   ├── bookmark/
│   │   │   ├── bookmark.controller.ts
│   │   │   ├── bookmark.service.ts
│   │   │   ├── bookmark.repository.ts
│   │   │   ├── bookmark.types.ts
│   │   │   └── index.ts
│   │   └── tag/
│   │       ├── tag.controller.ts
│   │       ├── tag.service.ts
│   │       ├── tag.repository.ts
│   │       ├── tag.types.ts
│   │       └── index.ts
│   ├── shared/
│   │   ├── types.ts
│   │   └── utils/
│   │       └── validation.ts
│   ├── infra/
│   │   ├── database.ts
│   │   ├── error.ts
│   │   ├── response.ts
│   │   └── config.ts
│   └── app.ts
├── tests/
│   ├── bookmark/
│   │   ├── bookmark-crud.test.ts
│   │   └── bookmark-tag.test.ts
│   ├── tag/
│   │   └── tag-crud.test.ts
│   └── e2e/                         # Step 6 时创建
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

| 目录 | 用途 |
|------|------|
| src/modules/ | 业务模块，每个模块独立目录，包含 controller/service/repository |
| src/shared/ | 跨模块共享的类型定义和工具函数 |
| src/infra/ | 基础设施：数据库连接、错误处理、响应格式、配置 |
| src/app.ts | Express 应用入口，注册路由和中间件 |
| tests/ | 测试代码，按业务模块组织 |

## 4. 数据模型

### Bookmark
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | integer | PK, 自增 | 主键 |
| url | text | NOT NULL, UNIQUE | 书签 URL，唯一 |
| title | text | NOT NULL | 书签标题，最长 200 字符 |
| description | text | 默认空字符串 | 书签描述，最长 1000 字符 |
| createdAt | text (ISO 8601) | NOT NULL | 创建时间 |
| updatedAt | text (ISO 8601) | NOT NULL | 最后更新时间 |

### Tag
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | integer | PK, 自增 | 主键 |
| name | text | NOT NULL, UNIQUE | 标签名，小写存储，最长 50 字符 |
| createdAt | text (ISO 8601) | NOT NULL | 创建时间 |

### BookmarkTag（关联表）
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| bookmarkId | integer | FK → Bookmark.id, ON DELETE CASCADE | 关联书签 |
| tagId | integer | FK → Tag.id, ON DELETE CASCADE | 关联标签 |
| | | PRIMARY KEY (bookmarkId, tagId) | 联合主键，防止重复关联 |

### 模型关系
```
Bookmark 1 ← N BookmarkTag N → 1 Tag（多对多关系，通过关联表实现）
```

### 建表 SQL
```sql
CREATE TABLE IF NOT EXISTS bookmarks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  createdAt TEXT NOT NULL,
  updatedAt TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  createdAt TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookmark_tags (
  bookmarkId INTEGER NOT NULL,
  tagId INTEGER NOT NULL,
  PRIMARY KEY (bookmarkId, tagId),
  FOREIGN KEY (bookmarkId) REFERENCES bookmarks(id) ON DELETE CASCADE,
  FOREIGN KEY (tagId) REFERENCES tags(id) ON DELETE CASCADE
);
```

## 5. 关键设计决策

### 决策1: 使用 SQLite 而非 JSON 文件
- **问题**: 书签数据需要持久化，选择什么存储方案
- **方案**: 使用 SQLite（better-sqlite3）
- **理由**: 书签涉及多对多关联（书签-标签），需要按标签筛选和关键词搜索，JSON 文件难以高效实现这些查询；SQLite 零配置单文件存储，同步 API 编码简单，better-sqlite3 性能优于异步方案，适合个人工具场景

### 决策2: 书签-标签关联逻辑放在 bookmark 模块
- **问题**: 书签和标签的关联管理应该放在哪个模块
- **方案**: 放在 bookmark 模块中（`POST /bookmarks/:id/tags` 和 `DELETE /bookmarks/:id/tags/:tagId`）
- **理由**: 关联操作的主体是书签（"给书签添加标签"），路由路径也以 `/bookmarks` 为前缀，归属 bookmark 模块更符合 RESTful 语义；同时避免 bookmark 和 tag 模块之间产生双向依赖

### 决策3: 标签名统一存储为小写
- **问题**: 标签名大小写如何处理
- **方案**: 创建标签时统一转为小写存储
- **理由**: 避免出现"前端"和"前端"相似但大小写不同的标签（对于英文标签如 "JavaScript" vs "javascript"），简化去重逻辑；个人工具场景下大小写不敏感更符合直觉
