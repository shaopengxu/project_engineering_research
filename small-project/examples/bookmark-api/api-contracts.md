# Bookmark API 接口契约

> 使用模板 A（HTTP REST API）格式。

---

## 通用约定

### 认证方式
无需认证（单用户个人工具）。

### 响应格式
```json
// 成功
{ "data": { ... } }

// 失败
{ "error": { "code": "ERROR_CODE", "message": "描述" } }
```

### 分页约定
```json
// Request: GET /bookmarks?page=1&pageSize=20
// Response:
{
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}
```

- page 从 1 开始，默认 1
- pageSize 默认 20，最大 100
- page 或 pageSize 不合法时返回 400 错误

### HTTP 状态码
| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 参数错误 |
| 404 | 资源不存在 |
| 409 | 资源冲突（重复） |
| 500 | 服务器错误 |

---

## 书签接口

### 添加书签

`POST /bookmarks`

**描述**: 创建一条新的书签记录。

**认证**: 不需要

**Request**:
```json
{
  "url": "string, 必填, 书签 URL，必须是合法的 HTTP/HTTPS 格式",
  "title": "string, 必填, 书签标题，最长 200 字符",
  "description": "string, 可选, 书签描述，最长 1000 字符，默认空字符串"
}
```

**Response 201**:
```json
{
  "data": {
    "id": 1,
    "url": "https://example.com",
    "title": "示例网站",
    "description": "一个示例网站",
    "createdAt": "2026-03-28T10:00:00.000Z",
    "updatedAt": "2026-03-28T10:00:00.000Z"
  }
}
```

**业务规则**:
- url 必须以 `http://` 或 `https://` 开头，且符合 URL 格式
- url 前后空白会被去除
- title 前后空白会被去除，去除后不能为空
- description 如未提供，默认为空字符串
- createdAt 和 updatedAt 设为当前时间
- id 由数据库自增生成

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_URL | url 缺失或不是合法的 HTTP/HTTPS 格式 |
| 400 | INVALID_TITLE | title 缺失、为空或超过 200 字符 |
| 400 | INVALID_DESCRIPTION | description 超过 1000 字符 |
| 409 | DUPLICATE_URL | 该 URL 已存在 |

---

### 查询书签列表

`GET /bookmarks`

**描述**: 分页查询书签列表，支持按标签筛选和关键词搜索。

**认证**: 不需要

**Request**:
```
Query Parameters:
  page: number, 可选, 页码，从 1 开始，默认 1
  pageSize: number, 可选, 每页数量，默认 20，最大 100
  tag: string, 可选, 按标签名筛选（精确匹配，大小写不敏感）
  keyword: string, 可选, 搜索关键词，匹配标题和描述（模糊匹配）
```

**Response 200**:
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "url": "https://example.com",
        "title": "示例网站",
        "description": "一个示例网站",
        "tags": [
          { "id": 1, "name": "前端" },
          { "id": 3, "name": "工具" }
        ],
        "createdAt": "2026-03-28T10:00:00.000Z",
        "updatedAt": "2026-03-28T10:00:00.000Z"
      }
    ],
    "total": 50,
    "page": 1,
    "pageSize": 20
  }
}
```

**业务规则**:
- 默认按 createdAt 倒序排列（最新的在前）
- tag 筛选为精确匹配（大小写不敏感），只返回关联了该标签的书签
- keyword 搜索为模糊匹配，匹配 title 或 description 中包含该关键词的书签
- tag 和 keyword 可同时使用，取交集
- 列表中的每条书签包含关联的标签信息（id 和 name）
- 无结果时 items 为空数组，total 为 0

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_PAGE | page 不是正整数 |
| 400 | INVALID_PAGE_SIZE | pageSize 不是 1-100 之间的正整数 |

---

### 查看书签详情

`GET /bookmarks/:id`

**描述**: 获取单条书签的完整信息，包含关联的标签列表。

**认证**: 不需要

**Request**:
```
Path Parameters:
  id: number, 必填, 书签 ID
```

**Response 200**:
```json
{
  "data": {
    "id": 1,
    "url": "https://example.com",
    "title": "示例网站",
    "description": "一个示例网站",
    "tags": [
      { "id": 1, "name": "前端" },
      { "id": 3, "name": "工具" }
    ],
    "createdAt": "2026-03-28T10:00:00.000Z",
    "updatedAt": "2026-03-28T10:00:00.000Z"
  }
}
```

**业务规则**:
- 返回书签的完整信息，包含关联的所有标签（id 和 name）
- 未关联任何标签时 tags 为空数组
- id 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | id 不是正整数 |
| 404 | BOOKMARK_NOT_FOUND | 指定 ID 的书签不存在 |

---

### 更新书签

`PUT /bookmarks/:id`

**描述**: 更新指定书签的信息。

**认证**: 不需要

**Request**:
```json
{
  "url": "string, 可选, 新的书签 URL",
  "title": "string, 可选, 新的书签标题",
  "description": "string, 可选, 新的书签描述"
}
```

```
Path Parameters:
  id: number, 必填, 书签 ID
```

**Response 200**:
```json
{
  "data": {
    "id": 1,
    "url": "https://new-example.com",
    "title": "更新后的标题",
    "description": "更新后的描述",
    "tags": [
      { "id": 1, "name": "前端" },
      { "id": 3, "name": "工具" }
    ],
    "createdAt": "2026-03-28T10:00:00.000Z",
    "updatedAt": "2026-03-28T12:00:00.000Z"
  }
}
```

**业务规则**:
- 更新响应包含书签的完整信息（含关联标签）
- 至少提供一个可更新字段（url、title、description），否则返回 400
- 只更新提供的字段，未提供的字段保持不变
- url 如果提供，必须是合法的 HTTP/HTTPS 格式且不与其他书签重复
- title 如果提供，去除空白后不能为空且不超过 200 字符
- description 如果提供，不超过 1000 字符
- 更新 updatedAt 为当前时间
- id 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | id 不是正整数 |
| 400 | EMPTY_UPDATE | 未提供任何可更新字段 |
| 400 | INVALID_URL | url 不是合法的 HTTP/HTTPS 格式 |
| 400 | INVALID_TITLE | title 为空或超过 200 字符 |
| 400 | INVALID_DESCRIPTION | description 超过 1000 字符 |
| 404 | BOOKMARK_NOT_FOUND | 指定 ID 的书签不存在 |
| 409 | DUPLICATE_URL | 新 URL 已被其他书签使用 |

---

### 删除书签

`DELETE /bookmarks/:id`

**描述**: 删除指定书签及其与所有标签的关联关系。

**认证**: 不需要

**Request**:
```
Path Parameters:
  id: number, 必填, 书签 ID
```

**Response 200**:
```json
{
  "data": {
    "id": 1,
    "deleted": true
  }
}
```

**业务规则**:
- 删除书签记录，同时自动删除 bookmark_tag 表中该书签的所有关联记录（通过 ON DELETE CASCADE）
- 删除后 ID 不复用
- id 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | id 不是正整数 |
| 404 | BOOKMARK_NOT_FOUND | 指定 ID 的书签不存在 |

---

## 标签接口

### 创建标签

`POST /tags`

**描述**: 创建一个新的标签。

**认证**: 不需要

**Request**:
```json
{
  "name": "string, 必填, 标签名"
}
```

**Response 201**:
```json
{
  "data": {
    "id": 1,
    "name": "前端",
    "createdAt": "2026-03-28T10:00:00.000Z"
  }
}
```

**业务规则**:
- 标签名前后空白会被去除
- 去除空白后标签名不能为空
- 标签名统一转为小写存储（大小写不敏感去重）
- 标签名最长 50 个字符
- 标签名只允许中文、英文字母、数字、连字符（正则: `/^[\u4e00-\u9fa5a-z0-9-]+$/`）
- createdAt 设为当前时间

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_TAG_NAME | name 缺失、为空、超过 50 字符或包含非法字符 |
| 409 | DUPLICATE_TAG_NAME | 该标签名已存在（大小写不敏感比较） |

---

### 查询所有标签

`GET /tags`

**描述**: 获取所有标签列表，每个标签附带关联的书签数量。

**认证**: 不需要

**Request**: 无参数

**Response 200**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "前端",
      "bookmarkCount": 12,
      "createdAt": "2026-03-28T10:00:00.000Z"
    },
    {
      "id": 2,
      "name": "工具",
      "bookmarkCount": 5,
      "createdAt": "2026-03-28T11:00:00.000Z"
    }
  ]
}
```

**业务规则**:
- 返回所有标签，按 name 字母顺序排列
- bookmarkCount 为该标签当前关联的书签数量（通过 bookmark_tag 表计算）
- 无标签时返回空数组

**错误码**: 无（此接口不会产生业务错误）

---

### 删除标签

`DELETE /tags/:id`

**描述**: 删除指定标签，同时自动解除其与所有书签的关联关系。

**认证**: 不需要

**Request**:
```
Path Parameters:
  id: number, 必填, 标签 ID
```

**Response 200**:
```json
{
  "data": {
    "id": 1,
    "deleted": true
  }
}
```

**业务规则**:
- 删除标签记录，同时自动删除 bookmark_tag 表中该标签的所有关联记录（通过 ON DELETE CASCADE）
- 关联的书签本身不受影响，只是失去了与该标签的关联
- 删除后 ID 不复用
- id 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | id 不是正整数 |
| 404 | TAG_NOT_FOUND | 指定 ID 的标签不存在 |

---

## 书签-标签关联接口

### 给书签添加标签

`POST /bookmarks/:id/tags`

**描述**: 为指定书签关联一个标签。

**认证**: 不需要

**Request**:
```json
{
  "tagId": "number, 必填, 要关联的标签 ID"
}
```

```
Path Parameters:
  id: number, 必填, 书签 ID
```

**Response 201**:
```json
{
  "data": {
    "bookmarkId": 1,
    "tagId": 3,
    "tag": {
      "id": 3,
      "name": "工具"
    }
  }
}
```

**业务规则**:
- 书签和标签都必须存在
- 同一书签不能重复关联同一标签
- 一个书签最多关联 10 个标签，超出时返回 400
- id 和 tagId 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | 书签 id 不是正整数 |
| 400 | INVALID_TAG_ID | tagId 缺失或不是正整数 |
| 400 | TAG_LIMIT_EXCEEDED | 该书签已关联 10 个标签，无法继续添加 |
| 404 | BOOKMARK_NOT_FOUND | 指定 ID 的书签不存在 |
| 404 | TAG_NOT_FOUND | 指定 ID 的标签不存在 |
| 409 | DUPLICATE_BOOKMARK_TAG | 该书签已关联了该标签 |

---

### 移除书签的标签

`DELETE /bookmarks/:id/tags/:tagId`

**描述**: 解除指定书签与指定标签的关联关系。

**认证**: 不需要

**Request**:
```
Path Parameters:
  id: number, 必填, 书签 ID
  tagId: number, 必填, 标签 ID
```

**Response 200**:
```json
{
  "data": {
    "bookmarkId": 1,
    "tagId": 3,
    "removed": true
  }
}
```

**业务规则**:
- 书签和标签都必须存在
- 该关联关系必须存在（书签确实关联了该标签）
- 只删除关联关系，不删除书签或标签本身
- id 和 tagId 必须是正整数

**错误码**:
| 状态码 | error.code | 触发条件 |
|--------|-----------|---------|
| 400 | INVALID_ID | 书签 id 不是正整数 |
| 400 | INVALID_TAG_ID | tagId 不是正整数 |
| 404 | BOOKMARK_NOT_FOUND | 指定 ID 的书签不存在 |
| 404 | TAG_NOT_FOUND | 指定 ID 的标签不存在 |
| 404 | BOOKMARK_TAG_NOT_FOUND | 该书签未关联该标签 |

---

## 需求追溯表

| PRD 来源 | 业务规则 / 验收标准原文 | 对应契约章节 | 备注 |
|---------|----------------------|------------|------|
| 书签管理 - 规则1 | URL 必须是合法的 HTTP/HTTPS 格式 | 添加书签#业务规则, 更新书签#业务规则 | |
| 书签管理 - 规则2 | URL 不允许重复 | 添加书签#错误码 DUPLICATE_URL, 更新书签#错误码 DUPLICATE_URL | |
| 书签管理 - 规则3 | 标题最长 200 字符，描述最长 1000 字符 | 添加书签#错误码, 更新书签#错误码 | |
| 书签管理 - 规则4 | 删除书签时自动清除与所有标签的关联 | 删除书签#业务规则 | ON DELETE CASCADE |
| 书签管理 - 规则5 | 书签列表默认按创建时间倒序排列 | 查询书签列表#业务规则 | |
| 书签管理 - 验收1 | POST /bookmarks 添加书签，返回完整信息 | 添加书签#Response 201 | |
| 书签管理 - 验收2 | GET /bookmarks 分页列表，默认第 1 页每页 20 条 | 查询书签列表#Request + 通用约定#分页约定 | |
| 书签管理 - 验收3 | GET /bookmarks?tag=前端 按标签筛选 | 查询书签列表#业务规则 | |
| 书签管理 - 验收4 | GET /bookmarks?keyword=TypeScript 搜索 | 查询书签列表#业务规则 | |
| 书签管理 - 验收5 | GET /bookmarks/:id 详情含标签列表 | 查看书签详情#Response 200 | |
| 书签管理 - 验收6 | PUT /bookmarks/:id 更新标题、URL 或描述 | 更新书签#业务规则 | |
| 书签管理 - 验收7 | DELETE /bookmarks/:id 删除书签，关联被清除 | 删除书签#业务规则 | |
| 书签管理 - 验收8 | 重复 URL 返回 409 | 添加书签#错误码 DUPLICATE_URL | |
| 书签管理 - 验收9 | 不存在的 ID 返回 404 | 查看书签详情#错误码 BOOKMARK_NOT_FOUND | 其他接口同理 |
| 标签管理 - 规则1 | 标签名不允许重复（大小写不敏感，统一小写） | 创建标签#业务规则 | |
| 标签管理 - 规则2 | 标签名最长 50 字符，只允许中英文、数字、连字符 | 创建标签#错误码 INVALID_TAG_NAME | |
| 标签管理 - 规则3 | 删除标签时自动清除与所有书签的关联 | 删除标签#业务规则 | ON DELETE CASCADE |
| 标签管理 - 规则4 | 同一书签不能重复关联同一标签 | 给书签添加标签#错误码 DUPLICATE_BOOKMARK_TAG | |
| 标签管理 - 规则5 | 一个书签最多关联 10 个标签 | 给书签添加标签#错误码 TAG_LIMIT_EXCEEDED | |
| 标签管理 - 验收1 | POST /tags 创建标签 | 创建标签#Response 201 | |
| 标签管理 - 验收2 | GET /tags 获取标签列表及书签数量 | 查询所有标签#Response 200 | |
| 标签管理 - 验收3 | DELETE /tags/:id 删除标签，解除关联 | 删除标签#业务规则 | |
| 标签管理 - 验收4 | POST /bookmarks/:id/tags 为书签添加标签 | 给书签添加标签#Response 201 | |
| 标签管理 - 验收5 | DELETE /bookmarks/:id/tags/:tagId 移除标签 | 移除书签的标签#Response 200 | |
| 标签管理 - 验收6 | 重复标签名返回 409 | 创建标签#错误码 DUPLICATE_TAG_NAME | |
| 标签管理 - 验收7 | 重复关联返回 409 | 给书签添加标签#错误码 DUPLICATE_BOOKMARK_TAG | |
| 标签管理 - 验收8 | 10 个标签限制返回 400 | 给书签添加标签#错误码 TAG_LIMIT_EXCEEDED | |
