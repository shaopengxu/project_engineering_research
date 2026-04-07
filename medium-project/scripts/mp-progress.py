#!/usr/bin/env python3
"""
中型项目模块进度表生成器。

从 GitHub Issues 查询数据，按模块和类型统计进度，输出 markdown 表格。
用法：python scripts/mp-progress.py
"""

import json
import subprocess
import sys
from collections import defaultdict


def run_gh_issue_list():
    """获取所有 Issues（open + closed）。"""
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "all", "--limit", "200",
         "--json", "number,title,labels,state"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: gh issue list failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def extract_labels(issue, prefix):
    """提取指定前缀的标签值列表，如 prefix='module' 返回 ['user', 'order']。"""
    return [
        label["name"][len(prefix) + 1:]
        for label in issue.get("labels", [])
        if label["name"].startswith(prefix + ":")
    ]


def extract_feature_from_title(title):
    """从标题中提取 feature 名，如 '[web-app/auth] ...' → 'auth'。"""
    if "/" in title.split("]")[0] if "]" in title else "":
        bracket_part = title.split("]")[0].lstrip("[")
        parts = bracket_part.split("/")
        if len(parts) >= 2:
            return parts[1].strip()
    return None


def classify_status(issues_of_type):
    """根据一组同 type 的 Issues 判定状态。"""
    if not issues_of_type:
        return "-"
    total = len(issues_of_type)
    closed = sum(1 for i in issues_of_type if i["state"] == "CLOSED")
    if closed == total:
        return "done"
    if closed == 0:
        # 单个 Issue 的 type（design, module-review 等）
        if total == 1:
            return "open"
        return f"0/{total}"
    return f"{closed}/{total}"


def classify_single_status(issues_of_type):
    """单 Issue 类型的状态判定（design, feature-review, module-review, integration-test）。"""
    if not issues_of_type:
        return "-"
    issue = issues_of_type[0]
    if issue["state"] == "CLOSED":
        return "done"
    return "open"


def build_progress(issues):
    """构建模块进度数据。"""
    # 按 module 分组
    module_issues = defaultdict(list)
    for issue in issues:
        modules = extract_labels(issue, "module")
        types = extract_labels(issue, "type")
        if not modules:
            continue  # 无 module 标签 → 全局阶段 Issue，跳过
        for mod in modules:
            module_issues[mod].append(issue)

    progress = {}

    for module, mod_issues in module_issues.items():
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

        # 检测是否为前端模块（有 feature-review 或标题含 feature 路径）
        has_feature_review = bool(by_type.get("feature-review"))
        has_feature_in_title = any(
            extract_feature_from_title(i["title"])
            for i in mod_issues
        )
        is_frontend = has_feature_review or has_feature_in_title

        if is_frontend:
            # 前端模块：按 feature 拆行
            features = set()
            for issue in mod_issues:
                feat = extract_feature_from_title(issue["title"])
                if feat:
                    features.add(feat)

            # 模块级条目（design = 整体设计, module-review = 模块级 Review）
            design_issues = [
                i for i in by_type.get("design", [])
                if "/" not in i["title"].split("模块设计:")[-1] if "模块设计:" in i["title"] else True
            ]
            # 简化：design Issues 中标题不含 feature 的是整体设计
            overall_design = [
                i for i in by_type.get("design", [])
                if not extract_feature_from_title(i["title"])
            ]

            for feat in sorted(features):
                feat_prefix = f"{module}/{feat}"
                # 筛选该 feature 的 Issues
                feat_design = [
                    i for i in by_type.get("design", [])
                    if feat in i["title"]
                ]
                feat_contract = [
                    i for i in by_type.get("contract-test", [])
                    if feat in i["title"]
                ]
                feat_impl = [
                    i for i in by_type.get("impl", [])
                    if feat in i["title"]
                ]
                feat_review = [
                    i for i in by_type.get("feature-review", [])
                    if feat in i["title"]
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


def render_table(progress):
    """输出 markdown 表格。"""
    if not progress:
        print("（无模块进度数据，可能尚未创建 Issues）")
        return

    columns = ["设计", "契约测试", "实现", "Feature Review", "模块 Review", "L2"]
    header = "| 模块 | " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---"] * (len(columns) + 1)) + "|"

    print(header)
    print(separator)

    # 排序：infra 在前，后端模块，前端模块（含 feature）在后
    def sort_key(item):
        name = item[0]
        if name == "infra":
            return (0, name)
        if "/" in name:
            return (2, name)
        return (1, name)

    for name, cols in sorted(progress.items(), key=sort_key):
        row = f"| {name} | " + " | ".join(cols[c] for c in columns) + " |"
        print(row)

    print()
    print("> `done` = 全部完成, `3/5` = 5 个中完成了 3 个, `open` = Issue 已创建, `-` = 未开始, `N/A` = 不适用")


def main():
    issues = run_gh_issue_list()
    progress = build_progress(issues)
    render_table(progress)


if __name__ == "__main__":
    main()
