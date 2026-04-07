#!/usr/bin/env python3
"""
GitHub Issue 通用工具 — 搜索/创建/关闭/评论。

供 medium-project 各 skill 调用，封装 search-or-create 等常用模式。

用法示例：
  # 搜索 Issue，未找到则创建，并写入 comment
  python mp-issue-helper.py find-or-create \
    --label "type:architecture" --search "架构设计" \
    --create-title "架构设计" --create-body "跟踪架构 Review。" \
    --comment "Review 结果..."

  # 搜索 Issue 并关闭
  python mp-issue-helper.py find-and-close \
    --label "type:architecture" --search "架构设计"

  # 直接关闭指定 Issue
  python mp-issue-helper.py close --issue 42

  # 对指定 Issue 添加 comment
  python mp-issue-helper.py comment --issue 42 --body "Review 结果..."
"""

import argparse
import json
import subprocess
import sys


def gh(args, check=True):
    """执行 gh CLI 命令，返回 stdout。"""
    result = subprocess.run(
        ["gh"] + args, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"gh {' '.join(args)} failed: {result.stderr}", file=sys.stderr)
    return result


def issue_search(labels, title_keyword, state="open"):
    """按标签 + 标题关键词搜索 Issue，返回 [{number, title, state}]。"""
    cmd = ["issue", "list", "--state", state,
           "--json", "number,title,state", "--limit", "10"]
    for label in labels:
        cmd.extend(["--label", label])
    if title_keyword:
        cmd.extend(["--search", f"{title_keyword} in:title"])
    result = gh(cmd, check=False)
    if result.returncode != 0:
        return []
    return json.loads(result.stdout or "[]")


def issue_create(title, labels, body=""):
    """创建 Issue，返回 Issue 编号。"""
    cmd = ["issue", "create", "--title", title, "--body", body]
    if labels:
        cmd.extend(["--label", ",".join(labels)])
    result = gh(cmd)
    if result.returncode != 0:
        return None
    # gh 输出格式：https://github.com/owner/repo/issues/42
    url = result.stdout.strip()
    try:
        return int(url.rstrip("/").split("/")[-1])
    except (ValueError, IndexError):
        return None


def issue_close(number, comment=None):
    """关闭 Issue，可附带 comment。"""
    cmd = ["issue", "close", str(number)]
    if comment:
        cmd.extend(["--comment", comment])
    gh(cmd)


def issue_comment(number, body):
    """对 Issue 添加 comment。"""
    gh(["issue", "comment", str(number), "--body", body])


# ── 高级操作 ──────────────────────────────────────────────


def find_or_create(labels, title_keyword, create_title=None, create_body=""):
    """搜索 Issue，未找到则创建。返回 Issue 编号。"""
    issues = issue_search(labels, title_keyword)
    if issues:
        return issues[0]["number"]
    if create_title:
        return issue_create(create_title, labels, create_body)
    return None


def find_and_close(labels, title_keyword, comment="Review 通过，阶段完成。"):
    """搜索 open Issue 并关闭。返回关闭的 Issue 编号，未找到返回 None。"""
    issues = issue_search(labels, title_keyword, state="open")
    if issues:
        issue_close(issues[0]["number"], comment)
        return issues[0]["number"]
    return None


# ── CLI ───────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="GitHub Issue 通用工具")
    sub = parser.add_subparsers(dest="command", required=True)

    # find-or-create
    p1 = sub.add_parser("find-or-create",
                        help="搜索 Issue，未找到则创建，可附带 comment")
    p1.add_argument("--label", action="append", required=True,
                    help="标签（可多次指定）")
    p1.add_argument("--search", required=True, help="标题搜索关键词")
    p1.add_argument("--create-title", help="未找到时创建的标题")
    p1.add_argument("--create-body", default="", help="未找到时创建的 body")
    p1.add_argument("--comment", help="写入 Issue 的 comment")

    # find-and-close
    p2 = sub.add_parser("find-and-close", help="搜索 open Issue 并关闭")
    p2.add_argument("--label", action="append", required=True)
    p2.add_argument("--search", required=True)
    p2.add_argument("--close-comment", default="Review 通过，阶段完成。")

    # close
    p3 = sub.add_parser("close", help="关闭指定 Issue")
    p3.add_argument("--issue", type=int, required=True)
    p3.add_argument("--close-comment", default="Review 通过，Task 完成。")

    # comment
    p4 = sub.add_parser("comment", help="对指定 Issue 添加 comment")
    p4.add_argument("--issue", type=int, required=True)
    p4.add_argument("--body", required=True)

    args = parser.parse_args()

    if args.command == "find-or-create":
        num = find_or_create(args.label, args.search,
                             args.create_title, args.create_body)
        if num is None:
            print("未找到且未指定 --create-title，无操作", file=sys.stderr)
            sys.exit(1)
        if args.comment:
            issue_comment(num, args.comment)
        print(num)

    elif args.command == "find-and-close":
        num = find_and_close(args.label, args.search, args.close_comment)
        if num:
            print(f"已关闭 #{num}")
        else:
            print("未找到匹配的 open Issue（跳过）")

    elif args.command == "close":
        issue_close(args.issue, args.close_comment)
        print(f"已关闭 #{args.issue}")

    elif args.command == "comment":
        issue_comment(args.issue, args.body)
        print(f"已评论 #{args.issue}")


if __name__ == "__main__":
    main()
