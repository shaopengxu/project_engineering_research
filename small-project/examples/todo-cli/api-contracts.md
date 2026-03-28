# Todo CLI 接口契约

> 使用模板 B（CLI 工具）格式。

---

## 通用约定

### 全局选项
| 选项 | 缩写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| --help | -h | boolean | false | 显示帮助信息 |
| --version | -V | boolean | false | 显示版本号 |

### 退出码
| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 业务错误（如任务不存在） |
| 2 | 参数错误（如缺少必填参数） |

### 输出约定
- 正常结果输出到 stdout
- 错误和日志输出到 stderr
- `todo list` 支持 `--json` 输出 JSON 格式

### 环境变量
| 变量 | 说明 | 默认值 |
|------|------|--------|
| TODO_FILE | 自定义存储文件路径 | ~/.todo.json |

---

## 任务管理命令

### `todo add <title>`

**描述**: 添加一条新的待办任务。

**参数 (Arguments)**:
| 参数 | 必填 | 说明 |
|------|------|------|
| title | 是 | 任务标题，非空字符串 |

**选项 (Options)**: 无

**标准输出 (stdout)**:
```
Added: #1 买牛奶
```

**业务规则**:
- 任务 ID 自增分配，从 1 开始
- 新任务默认状态为 todo
- 创建时间和更新时间设为当前时间
- 标题前后空白会被去除
- 去除空白后标题不能为空

**错误场景**:
| 退出码 | 错误信息 | 触发条件 |
|--------|---------|---------|
| 2 | Error: missing argument 'title' | 未提供 title 参数 |
| 1 | Error: title cannot be empty | title 为空或只包含空白字符 |

**示例**:
```bash
# 添加一条待办
$ todo add "买牛奶"
Added: #1 买牛奶

# 添加另一条待办
$ todo add "写周报"
Added: #2 写周报
```

---

### `todo list [--status <status>] [--json]`

**描述**: 列出待办任务，支持按状态筛选和 JSON 格式输出。

**参数 (Arguments)**: 无

**选项 (Options)**:
| 选项 | 缩写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| --status | -s | string | 无 | 按状态筛选，可选值: todo, done |
| --json | | boolean | false | 以 JSON 格式输出 |

**标准输出 (stdout)**:
```
ID  Status  Title
1   [ ]     买牛奶
2   [x]     写周报
3   [ ]     看文档

Total: 3 tasks (2 todo, 1 done)
```

**JSON 输出** (`--json`):
```json
[
  {
    "id": 1,
    "title": "买牛奶",
    "status": "todo",
    "createdAt": "2026-03-28T10:00:00.000Z",
    "updatedAt": "2026-03-28T10:00:00.000Z"
  }
]
```

**业务规则**:
- 无筛选时返回所有任务
- `--status todo` 只返回未完成的任务
- `--status done` 只返回已完成的任务
- 列表按 ID 升序排列
- 没有任务时显示 "No tasks found"
- `--json` 模式下无任务时输出空数组 `[]`

**错误场景**:
| 退出码 | 错误信息 | 触发条件 |
|--------|---------|---------|
| 2 | Error: invalid status 'xxx', expected 'todo' or 'done' | --status 的值不是 todo 或 done |

**示例**:
```bash
# 列出所有任务
$ todo list
ID  Status  Title
1   [ ]     买牛奶
2   [x]     写周报

Total: 2 tasks (1 todo, 1 done)

# 只看未完成的
$ todo list --status todo
ID  Status  Title
1   [ ]     买牛奶

Total: 1 task (1 todo, 0 done)

# JSON 格式输出
$ todo list --json
[
  {
    "id": 1,
    "title": "买牛奶",
    "status": "todo",
    "createdAt": "2026-03-28T10:00:00.000Z",
    "updatedAt": "2026-03-28T10:00:00.000Z"
  }
]

# 没有任务时
$ todo list
No tasks found
```

---

### `todo done <id>`

**描述**: 将指定任务标记为已完成。

**参数 (Arguments)**:
| 参数 | 必填 | 说明 |
|------|------|------|
| id | 是 | 任务 ID，正整数 |

**选项 (Options)**: 无

**标准输出 (stdout)**:
```
Done: #1 买牛奶
```

**业务规则**:
- 将任务状态从 todo 改为 done
- 更新 updatedAt 为当前时间
- 对已完成的任务再次执行 done 不报错，输出提示 "Already done: #1 买牛奶"
- ID 必须是正整数

**错误场景**:
| 退出码 | 错误信息 | 触发条件 |
|--------|---------|---------|
| 2 | Error: missing argument 'id' | 未提供 id 参数 |
| 2 | Error: invalid id 'xxx', expected a positive integer | id 不是正整数 |
| 1 | Error: task #99 not found | 指定 ID 的任务不存在 |

**示例**:
```bash
# 标记任务完成
$ todo done 1
Done: #1 买牛奶

# 重复标记
$ todo done 1
Already done: #1 买牛奶

# 任务不存在
$ todo done 99
Error: task #99 not found
```

---

### `todo delete <id>`

**描述**: 删除指定任务。

**参数 (Arguments)**:
| 参数 | 必填 | 说明 |
|------|------|------|
| id | 是 | 任务 ID，正整数 |

**选项 (Options)**: 无

**标准输出 (stdout)**:
```
Deleted: #1 买牛奶
```

**业务规则**:
- 从列表中永久删除任务
- 删除后 ID 不复用
- ID 必须是正整数

**错误场景**:
| 退出码 | 错误信息 | 触发条件 |
|--------|---------|---------|
| 2 | Error: missing argument 'id' | 未提供 id 参数 |
| 2 | Error: invalid id 'xxx', expected a positive integer | id 不是正整数 |
| 1 | Error: task #99 not found | 指定 ID 的任务不存在 |

**示例**:
```bash
# 删除任务
$ todo delete 1
Deleted: #1 买牛奶

# 删除不存在的任务
$ todo delete 1
Error: task #1 not found
```

---

## storage 模块内部接口

> 以下接口为模块间调用接口，供 task 模块使用。

### `load(): TodoList`

**描述**: 从 JSON 文件加载任务数据。

**返回值**: TodoList 对象，包含 nextId 和 todos 数组。

**业务规则**:
- 文件不存在时返回初始数据 `{ nextId: 1, todos: [] }`
- 文件内容为空或不合法 JSON 时返回初始数据
- 存储文件路径从环境变量 `TODO_FILE` 读取，未设置时使用 `~/.todo.json`

### `save(data: TodoList): void`

**描述**: 将任务数据写入 JSON 文件。

**业务规则**:
- 以格式化的 JSON 写入（2 空格缩进），便于人工查看
- 如果目标目录不存在，自动创建
- 写入失败时抛出错误
