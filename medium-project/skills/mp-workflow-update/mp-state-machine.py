#!/usr/bin/env python3
"""
中型项目 workflow 状态机。

解析状态变更描述 → 读取 workflow-state.md → 计算新状态 → 执行 Issue 操作 → 写回状态文件。

用法：python mp-state-machine.py "<状态变更描述>"

输出：JSON 格式 {"updated": {...}, "issue_ops": [...], "next": "..."}
供 mp-workflow-update skill 读取并转述给技术负责人。
"""

import json
import os
import re
import subprocess
import sys

# ── 状态文件读写 ─────────────────────────────────────────

STATE_FILE = "docs/workflow-state.md"

FIELDS = ["step", "substep", "module", "feature",
          "module_order", "feature_order", "current_milestone"]


def read_state():
    """读取 workflow-state.md，返回字段字典。"""
    state = {f: "" for f in FIELDS}
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            for field in FIELDS:
                if line.startswith(f"{field}:"):
                    val = line[len(field) + 1:].strip()
                    state[field] = val
                    break
    return state


def write_state(state):
    """将字段写回 workflow-state.md，保留原始结构。"""
    if not os.path.exists(STATE_FILE):
        print(f"Error: {STATE_FILE} not found", file=sys.stderr)
        sys.exit(1)
    with open(STATE_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        replaced = False
        for field in FIELDS:
            if stripped.startswith(f"{field}:"):
                new_lines.append(f"{field}: {state.get(field, '')}\n")
                replaced = True
                break
        if not replaced:
            new_lines.append(line)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def parse_list(val):
    """解析 [a, b, c] 格式的列表字符串。"""
    if not val:
        return []
    val = val.strip().strip("[]")
    return [x.strip() for x in val.split(",") if x.strip()]


def parse_feature_order(val):
    """解析 feature_order 字段。格式：{ web-app: [auth, product], admin: [dashboard] }"""
    if not val:
        return {}
    val = val.strip().strip("{}")
    result = {}
    for segment in re.split(r",\s*(?=\w+\s*:)", val):
        if ":" not in segment:
            continue
        mod, rest = segment.split(":", 1)
        result[mod.strip()] = parse_list(rest)
    return result


# ── Issue 操作 ────────────────────────────────────────────


def _gh(args):
    """执行 gh CLI 命令，返回 subprocess.CompletedProcess。"""
    return subprocess.run(["gh"] + args, capture_output=True, text=True)


def _issue_search(labels, title_keyword, state="open"):
    """按标签 + 标题关键词搜索 Issue，返回 [{number, title, state}]。"""
    cmd = ["issue", "list", "--state", state,
           "--json", "number,title,state", "--limit", "10"]
    for label in labels:
        cmd.extend(["--label", label])
    if title_keyword:
        cmd.extend(["--search", f"{title_keyword} in:title"])
    result = _gh(cmd)
    if result.returncode != 0:
        return []
    return json.loads(result.stdout or "[]")


def issue_close(number, comment="Review 通过，Task 完成。"):
    """关闭指定 Issue，可附带 comment。"""
    cmd = ["issue", "close", str(number)]
    if comment:
        cmd.extend(["--comment", comment])
    _gh(cmd)


def issue_find_and_close(labels, search_keyword, comment="Review 通过，阶段完成。"):
    """搜索 open Issue 并关闭。返回描述字符串。"""
    issues = _issue_search(labels, search_keyword)
    if issues:
        issue_close(issues[0]["number"], comment)
        return f"已关闭 #{issues[0]['number']}"
    return "未找到匹配的 open Issue（跳过）"


def has_open_integration_issues():
    """查询是否有 open 的 integration-test Issue。"""
    issues = _issue_search(["type:integration-test"], None)
    return len(issues) > 0


# ── 辅助函数 ──────────────────────────────────────────────


def next_in_list(lst, current):
    """返回列表中 current 之后的元素，如果是最后一个返回 None。"""
    if current not in lst:
        return None
    idx = lst.index(current)
    if idx + 1 < len(lst):
        return lst[idx + 1]
    return None


def is_last_in_list(lst, current):
    """判断 current 是否是列表最后一个。"""
    return current in lst and lst.index(current) == len(lst) - 1


def switch_to_next_module(state):
    """切换到下一模块的通用逻辑。返回 (updates_dict, description)。"""
    module_order = parse_list(state["module_order"])
    current = state["module"]
    if is_last_in_list(module_order, current):
        return {"step": "6", "substep": "", "module": "", "feature": ""}, "最后模块完成，进入 Step 6 E2E 测试"
    nxt = next_in_list(module_order, current)
    if nxt:
        return {"substep": "5b", "module": nxt, "feature": ""}, f"切换到模块 {nxt}"
    return {"substep": "5b", "feature": ""}, "切换到下一模块"


# ── 转换处理函数 ──────────────────────────────────────────


def handle(state, desc):
    """
    根据描述匹配转换规则，返回 (updates, issue_ops, message)。
    - updates: 要更新的字段 {field: value}
    - issue_ops: 已执行的 Issue 操作描述列表
    - message: 下一步提示
    """
    updates = {}
    ops = []
    msg = ""

    # ── Step 1 完成 ──
    if re.search(r"Step\s*1\s*完成", desc):
        updates = {"step": "2", "substep": ""}
        ops.append(issue_find_and_close(["type:prd-review"], "PRD Review"))
        msg = "下一步：调用 /mp-architecture 进行系统架构设计"
        return updates, ops, msg

    # ── Step 2 review 通过 ──
    if re.search(r"Step\s*2\s*review\s*通过", desc):
        updates = {"step": "3", "substep": ""}
        ops.append(issue_find_and_close(["type:architecture"], "架构设计"))
        msg = ("下一步：\n"
               "1. Agent 已提取模块列表，请确认 module_order 和 feature_order\n"
               "2. 调用 /mp-module-design 按依赖顺序逐个设计模块\n"
               "注意：需要 Agent 读取 architecture.md 提取模块列表，"
               "填写 module_order/feature_order 并批量创建 design Issue")
        return updates, ops, msg

    # ── {module} 模块设计 review 通过 ──
    m = re.match(r"(\S+)\s+(\S+)\s*模块设计\s*review\s*通过", desc)
    if m:
        module, feature = m.group(1), m.group(2)
        ops.append(issue_find_and_close(
            ["type:design", f"module:{module}"],
            f"模块设计: {module}/{feature}"))
        msg = f"下一步：继续设计下一个模块/feature，或调用 /mp-module-design --summary 进行汇总"
        return updates, ops, msg

    m = re.match(r"(\S+)\s*模块设计\s*review\s*通过", desc)
    if m:
        module = m.group(1)
        ops.append(issue_find_and_close(
            ["type:design", f"module:{module}"],
            f"模块设计: {module}"))
        msg = f"下一步：继续设计下一个模块，或调用 /mp-module-design --summary 进行汇总"
        return updates, ops, msg

    # ── 前端整体设计完成 ──
    if re.search(r"前端整体设计完成", desc):
        msg = "备注已记录。下一步：逐个设计前端 feature"
        return updates, ops, msg

    # ── Step 3 review 通过 ──
    if re.search(r"Step\s*3\s*review\s*通过", desc):
        updates = {"step": "4", "substep": "4a"}
        ops.append(issue_find_and_close(["type:design"], "模块设计: 汇总检查"))
        msg = "下一步：调用 /mp-scaffold 初始化项目脚手架"
        return updates, ops, msg

    # ── 脚手架 review 通过 ──
    if re.search(r"脚手架\s*review\s*通过", desc):
        updates = {"step": "4", "substep": "4b"}
        ops.append(issue_find_and_close(["type:scaffold"], "脚手架"))
        msg = "下一步：调用 /mp-task-split 拆分任务并创建 Issues"
        return updates, ops, msg

    # ── Issues review 通过 ──
    if re.search(r"Issues?\s*review\s*通过", desc):
        updates = {"step": "5", "substep": "5a", "module": "infra"}
        ops.append(issue_find_and_close(["type:task-split"], "任务拆分"))
        msg = "下一步：调用 /mp-impl-infra {issue-number} 实现 infra"
        return updates, ops, msg

    # ── infra #N review 通过 ──
    m = re.search(r"infra\s*#?(\d+)\s*review\s*通过", desc)
    if m:
        issue_num = m.group(1)
        module_order = parse_list(state["module_order"])
        nxt = next_in_list(module_order, "infra") or ""
        updates = {"substep": "5b", "module": nxt}
        issue_close(int(issue_num))
        ops.append(f"关闭 Task Issue #{issue_num}")
        msg = f"下一步：开始模块 {nxt} 的契约测试"
        return updates, ops, msg

    # ── {module} 契约测试 #N review 通过 ──
    m = re.search(r"(\S+)\s*契约测试\s*#?(\d+)\s*review\s*通过", desc)
    if m:
        issue_num = m.group(2)
        updates = {"substep": "5c"}
        issue_close(int(issue_num))
        ops.append(f"关闭 Task Issue #{issue_num}")
        msg = "下一步：开始实现 Task"
        return updates, ops, msg

    # ── Issue #N 实现完成 ──
    m = re.search(r"Issue\s*#?(\d+)\s*实现完成", desc)
    if m:
        updates = {"substep": "5c-review"}
        msg = f"下一步：调用 /mp-review-task 进行 Review"
        return updates, ops, msg

    # ── Issue #N review LGTM ──
    m = re.search(r"Issue\s*#?(\d+)\s*review\s*LGTM", desc)
    if m:
        issue_num = m.group(1)
        updates = {"substep": "5c"}
        issue_close(int(issue_num))
        ops.append(f"关闭 Task Issue #{issue_num}")
        msg = "下一步：继续下一个 Task 的实现"
        return updates, ops, msg

    # ── {module} 模块所有 Task 完成 ──
    m = re.match(r"(\S+)\s*模块所有\s*Task\s*完成", desc)
    if m:
        updates = {"substep": "5e"}
        msg = f"下一步：调用 /mp-review-module {m.group(1)} 进行模块 Review"
        return updates, ops, msg

    # ── {feature} 所有 Task 完成 ──
    m = re.match(r"(\S+)\s*所有\s*Task\s*完成", desc)
    if m:
        updates = {"substep": "5e"}
        msg = f"下一步：调用 /mp-review-feature 进行 Feature Review"
        return updates, ops, msg

    # ── {module} {feature} Feature Review LGTM ──
    m = re.match(r"(\S+)\s+(\S+)\s*Feature\s*Review\s*LGTM", desc)
    if m:
        module, feature = m.group(1), m.group(2)
        ops.append(issue_find_and_close(
            ["type:feature-review", f"module:{module}"],
            f"Feature Review: {module}/{feature}"))
        # 判断是否最后一个 feature
        fo = parse_feature_order(state["feature_order"])
        features = fo.get(module, [])
        if is_last_in_list(features, feature):
            updates = {"feature": "", "substep": "5e"}
            msg = f"所有 feature Review 通过。下一步：调用 /mp-review-module-frontend {module}"
        else:
            nxt = next_in_list(features, feature) or ""
            updates = {"feature": nxt, "substep": "5b"}
            msg = f"下一步：开始 feature {nxt} 的契约测试"
        return updates, ops, msg

    # ── {module} 模块 Review LGTM ──
    m = re.match(r"(\S+)\s*模块\s*Review\s*LGTM", desc)
    if m:
        module = m.group(1)
        ops.append(issue_find_and_close(
            ["type:module-review", f"module:{module}"],
            f"模块 Review: {module}"))
        if has_open_integration_issues():
            updates = {"substep": "5f"}
            msg = "存在未完成的 L2 集成测试 Issue。下一步：执行 L2 集成测试或开始下一模块"
        else:
            u, m2 = switch_to_next_module(state)
            updates = u
            msg = m2
        return updates, ops, msg

    # ── L2 集成测试 #N 完成 ──
    m = re.search(r"L2\s*集成测试\s*#?(\d+)\s*完成", desc)
    if m:
        issue_num = m.group(1)
        issue_close(int(issue_num))
        ops.append(f"关闭 Task Issue #{issue_num}")
        if has_open_integration_issues():
            updates = {"substep": "5f"}
            msg = "仍有未完成的 L2 集成测试。继续执行下一个 L2 或开始下一模块"
        else:
            u, m2 = switch_to_next_module(state)
            updates = u
            msg = m2
        return updates, ops, msg

    # ── 开始处理某模块 ──
    m = re.search(r"开始处理\s*(\S+)\s*模块", desc)
    if m:
        module = m.group(1)
        updates = {"module": module}
        if state.get("step") == "5":
            updates["substep"] = "5b"
        msg = f"已切换到模块 {module}"
        return updates, ops, msg

    # ── 开始处理某 feature ──
    m = re.search(r"开始处理\s*(\S+)\s+(\S+)\s*feature", desc)
    if m:
        module, feature = m.group(1), m.group(2)
        updates = {"module": module, "feature": feature}
        if state.get("step") == "5":
            updates["substep"] = "5b"
        msg = f"已切换到 {module}/{feature}"
        return updates, ops, msg

    # ── E2E 测试通过 ──
    if re.search(r"E2E\s*测试通过", desc):
        updates = {"step": "7"}
        ops.append(issue_find_and_close(["type:e2e"], "E2E 测试"))
        msg = "下一步：调用 /mp-review-acceptance 进行验收预检"
        return updates, ops, msg

    # ── 验收通过 ──
    if re.search(r"验收通过", desc):
        updates = {"step": "done"}
        ops.append(issue_find_and_close(["type:acceptance"], "验收预检"))
        msg = "项目完成！"
        return updates, ops, msg

    return None, None, None


# ── 主流程 ────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print("用法: python mp-state-machine.py \"<状态变更描述>\"", file=sys.stderr)
        sys.exit(1)

    desc = " ".join(sys.argv[1:])

    state = read_state()
    if state is None:
        print(json.dumps({"error": f"{STATE_FILE} 不存在，请先调用 /mp-workflow-update init"},
                         ensure_ascii=False))
        sys.exit(1)

    updates, ops, msg = handle(state, desc)

    if updates is None:
        print(json.dumps({"error": f"无法匹配状态变更描述: {desc}",
                          "hint": "请检查输入格式是否正确"},
                         ensure_ascii=False))
        sys.exit(1)

    # 应用更新
    old_state = dict(state)
    for k, v in updates.items():
        state[k] = v
    write_state(state)

    # 输出结果
    changed = {k: {"from": old_state[k], "to": v} for k, v in updates.items()
               if old_state.get(k) != v}
    result = {
        "updated": changed,
        "issue_ops": [op for op in ops if op],
        "next": msg,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
