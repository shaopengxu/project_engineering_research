#!/usr/bin/env python3
"""
中型项目模块进度表生成器。

从 GitHub Issues + workflow-state.md 生成模块进度表。
用法：python mp-progress.py
"""

import json
import os
import re
import subprocess
import sys
from collections import defaultdict

STATE_FILE = "docs/workflow-state.md"


# ── workflow-state 读取 ───────────────────────────────────


def read_state_fields():
    """读取 workflow-state.md 中的 module_order 和 feature_order。"""
    module_order = []
    feature_order = {}
    if not os.path.exists(STATE_FILE):
        return module_order, feature_order
    with open(STATE_FILE, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("module_order:"):
                val = stripped[len("module_order:"):].strip()
                module_order = _parse_list(val)
            elif stripped.startswith("feature_order:"):
                val = stripped[len("feature_order:"):].strip()
                feature_order = _parse_feature_order(val)
    return module_order, feature_order


def _parse_list(val):
    if not val:
        return []
    val = val.strip().strip("[]")
    return [x.strip() for x in val.split(",") if x.strip()]


def _parse_feature_order(val):
    if not val:
        return {}
    val = val.strip().strip("{}")
    result = {}
    for segment in re.split(r"\],\s*", val):
        segment = segment.strip()
        if ":" not in segment:
            continue
        mod, rest = segment.split(":", 1)
        result[mod.strip()] = _parse_list(rest.strip() + "]")
    return result


# ── GitHub Issues 查询 ────────────────────────────────────


def run_gh_issue_list():
    """获取所有 Issues（open + closed）。"""
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "all", "--limit", "500",
         "--json", "number,title,labels,state"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: gh issue list failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    issues = json.loads(result.stdout)
    if len(issues) == 500:
        print("Warning: Issue 数量达到 500 上限，可能有截断", file=sys.stderr)
    return issues


# ── 标签和标题解析 ────────────────────────────────────────


def extract_labels(issue, prefix):
    """提取指定前缀的标签值列表，如 prefix='module' 返回 ['user', 'order']。"""
    return [
        label["name"][len(prefix) + 1:]
        for label in issue.get("labels", [])
        if label["name"].startswith(prefix + ":")
    ]


def extract_feature_from_title(title):
    """从标题中提取 feature 名，如 '[web-app/auth] ...' → 'auth'。"""
    if "]" not in title:
        return None
    bracket_part = title.split("]")[0].lstrip("[")
    if "/" not in bracket_part:
        return None
    parts = bracket_part.split("/")
    if len(parts) >= 2:
        return parts[1].strip()
    return None


# ── 状态判定 ──────────────────────────────────────────────


def classify_status(issues_of_type):
    """多 Issue 类型（contract-test、impl）的状态判定。"""
    if not issues_of_type:
        return "-"
    total = len(issues_of_type)
    closed = sum(1 for i in issues_of_type if i["state"] == "CLOSED")
    if closed == total:
        return "done"
    if closed == 0:
        if total == 1:
            return "open"
        return f"0/{total}"
    return f"{closed}/{total}"


def classify_single_status(issues_of_type):
    """单 Issue 类型（design、feature-review、module-review、integration-test）的状态判定。"""
    if not issues_of_type:
        return "-"
    issue = issues_of_type[0]
    if issue["state"] == "CLOSED":
        return "done"
    return "open"


# ── 进度构建 ──────────────────────────────────────────────


def build_progress(issues, module_order, feature_order):
    """构建模块进度数据。"""
    frontend_modules = set(feature_order.keys())

    # 按 module 分组
    module_issues = defaultdict(list)
    for issue in issues:
        modules = extract_labels(issue, "module")
        if not modules:
            continue
        for mod in modules:
            module_issues[mod].append(issue)

    progress = {}

    # 确定要显示的模块列表：优先用 module_order，否则从 Issues 推导
    all_modules = module_order if module_order else sorted(module_issues.keys())

    for module in all_modules:
        mod_issues = module_issues.get(module, [])

        # 按 type 分组
        by_type = defaultdict(list)
        for issue in mod_issues:
            for t in extract_labels(issue, "type"):
                by_type[t].append(issue)

        # infra 特殊处理
        if module == "infra":
            infra_status = classify_status(by_type.get("infra", []))
            progress["infra"] = {
                "设计": "N/A",
                "契约测试": "N/A",
                "实现": infra_status,
                "Feature Review": "N/A",
                "模块 Review": "N/A",
                "L2": "N/A",
            }
            continue

        is_frontend = module in frontend_modules

        if is_frontend:
            # 前端模块：按 feature 拆行
            # 优先从 feature_order 获取 feature 列表，保证完整且有序
            features = feature_order.get(module, [])
            if not features:
                # fallback：从 Issue 标题提取
                features = sorted({
                    extract_feature_from_title(i["title"])
                    for i in mod_issues
                    if extract_feature_from_title(i["title"])
                })

            # 整体设计 Issue（标题不含 feature 路径）
            overall_design = [
                i for i in by_type.get("design", [])
                if not extract_feature_from_title(i["title"])
            ]

            if not features:
                # 前端模块但无 feature 信息：作为普通行显示
                progress[module] = {
                    "设计": classify_single_status(by_type.get("design", [])),
                    "契约测试": classify_status(by_type.get("contract-test", [])),
                    "实现": classify_status(by_type.get("impl", [])),
                    "Feature Review": "-",
                    "模块 Review": classify_single_status(by_type.get("module-review", [])),
                    "L2": classify_single_status(by_type.get("integration-test", [])),
                }
                continue

            for feat in features:
                feat_prefix = f"{module}/{feat}"
                # 精确匹配 feature（通过解析标题中的方括号内容）
                feat_design = [
                    i for i in by_type.get("design", [])
                    if extract_feature_from_title(i["title"]) == feat
                ]
                feat_contract = [
                    i for i in by_type.get("contract-test", [])
                    if extract_feature_from_title(i["title"]) == feat
                ]
                feat_impl = [
                    i for i in by_type.get("impl", [])
                    if extract_feature_from_title(i["title"]) == feat
                ]
                feat_review = [
                    i for i in by_type.get("feature-review", [])
                    if extract_feature_from_title(i["title"]) == feat
                        or feat in i["title"]  # Feature Review 标题格式不同
                ]

                progress[feat_prefix] = {
                    "设计": classify_single_status(feat_design) if feat_design else classify_single_status(overall_design),
                    "契约测试": classify_status(feat_contract),
                    "实现": classify_status(feat_impl),
                    "Feature Review": classify_single_status(feat_review),
                    "模块 Review": classify_single_status(by_type.get("module-review", [])),
                    "L2": classify_single_status(by_type.get("integration-test", [])),
                }
        else:
            # 后端模块
            progress[module] = {
                "设计": classify_single_status(by_type.get("design", [])),
                "契约测试": classify_status(by_type.get("contract-test", [])),
                "实现": classify_status(by_type.get("impl", [])),
                "Feature Review": "N/A",
                "模块 Review": classify_single_status(by_type.get("module-review", [])),
                "L2": classify_single_status(by_type.get("integration-test", [])),
            }

    return progress


def render_table(progress, module_order):
    """输出 markdown 表格。"""
    if not progress:
        print("（无模块进度数据，可能尚未创建 Issues）")
        return

    columns = ["设计", "契约测试", "实现", "Feature Review", "模块 Review", "L2"]
    header = "| 模块 | " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---"] * (len(columns) + 1)) + "|"

    print(header)
    print(separator)

    # 排序：按 module_order 顺序，前端 feature 紧跟其模块
    if module_order:
        def sort_key(item):
            name = item[0]
            base_module = name.split("/")[0]
            try:
                idx = module_order.index(base_module)
            except ValueError:
                idx = len(module_order)
            # feature 排在模块名之后（模块名本身不出现在 progress 中，feature 按序排列）
            suffix = name.split("/")[1] if "/" in name else ""
            return (idx, suffix)
    else:
        def sort_key(item):
            name = item[0]
            if name == "infra":
                return (0, "", name)
            if "/" in name:
                return (2, name.split("/")[0], name)
            return (1, "", name)

    for name, cols in sorted(progress.items(), key=sort_key):
        row = f"| {name} | " + " | ".join(cols[c] for c in columns) + " |"
        print(row)

    print()
    print("> `done` = 全部完成, `3/5` = 5 个中完成了 3 个, `open` = Issue 已创建, `-` = 未开始, `N/A` = 不适用")


def main():
    module_order, feature_order = read_state_fields()
    issues = run_gh_issue_list()
    progress = build_progress(issues, module_order, feature_order)
    render_table(progress, module_order)


if __name__ == "__main__":
    main()
