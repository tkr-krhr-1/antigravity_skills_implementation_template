import subprocess
import re
import json
import sys

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return ""

def main():
    # 1. 現在のブランチ名を取得
    branch = run_cmd("git symbolic-ref --short HEAD")
    if not branch:
        print("Error: Not a git repository or detached HEAD.")
        sys.exit(1)

    # 2. ブランチ名からIssue番号を抽出 (例: feature/123-login -> 123)
    issue_id = ""
    issue_info = "Issue情報なし"
    match = re.search(r'(\d+)', branch)
    if match:
        issue_id = match.group(1)
        # GitHub CLIでIssueの内容を取得
        raw_issue = run_cmd(f"gh issue view {issue_id} --json title,body")
        if raw_issue:
            data = json.loads(raw_issue)
            issue_info = f"Title: {data.get('title')}\nBody:\n{data.get('body')}"

    # 3. mainブランチとの差分コミットログを取得
    # (mainが存在しない場合はorigin/mainなどを適宜調整)
    commits = run_cmd("git log origin/main..HEAD --no-merges --pretty=format:'- %s'")
    if not commits:
        commits = "変更コミットが見つかりませんでした（mainと同期している可能性があります）。"

    # 4. 変更ファイル統計
    stats = run_cmd("git diff --stat origin/main..HEAD")

    # LLMへの入力として整形して出力
    output = f"""
=== CONTEXT START ===
Current Branch: {branch}
Target Issue ID: {issue_id}

[Linked Issue Content]
{issue_info}

[Commit History]
{commits}

[Changed Files Stats]
{stats}
=== CONTEXT END ===
"""
    print(output)

if __name__ == "__main__":
    main()