import sys
import re
import subprocess
import os

def run_gh_command(args):
    """ghコマンドを実行して結果（URL等）を返す"""
    try:
        result = subprocess.run(
            ["gh"] + args,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing gh command: {e.stderr}")
        sys.exit(1)

def parse_prd_feature_list(file_path):
    """PRDファイルから「4.1 機能一覧」セクションを抽出し、各機能をパースする"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 「4.1 機能一覧」セクションを抽出
    feature_section_match = re.search(r'### 4\.1 機能一覧.*?\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
    if not feature_section_match:
        print("Could not find section '4.1 機能一覧'.")
        return []

    section_text = feature_section_match.group(1).strip()
    features = []
    
    # "- **[FR-01] タイトル**: 説明" のパターンを抽出
    pattern = re.compile(r'-\s+\*\*\[(FR-\d+)\]\s+(.*?)\*\*:\s+(.*)')
    
    for line in section_text.split('\n'):
        match = pattern.match(line.strip())
        if match:
            features.append({
                "id": match.group(1),
                "title": match.group(2).strip(),
                "description": match.group(3).strip()
            })
    
    return features

def register_tasks(features):
    print(f"Found {len(features)} features in Feature List. Starting registration...")
    
    for feature in features:
        # 1. EPIC登録
        epic_title = f"🎯 [{feature['id']}] {feature['title']}"
        print(f"Creating EPIC: {epic_title}...")
        
        epic_url = run_gh_command([
            "issue", "create",
            "--title", epic_title,
            "--body", f"## 機能概要\n{feature['description']}\n\nこの機能の実装を完了させるためのEPICです。",
            "--label", "epic"
        ])
        epic_id = epic_url.split('/')[-1]
        
        # 親タスクへの案内コメント
        run_gh_command([
            "issue", "comment", epic_id,
            "--body", f"## 🎯 EPIC開始\n機能 ID: {feature['id']}\n機能名: {feature['title']}\n\n配下の子タスク（Logic, Infra, UI, Test, Doc）を順次進めてください。"
        ])

        # 2. 子タスクの定義
        child_tasks = [
            {"type": "⚙️ Logic", "label": "feature", "desc": "Domain/Application層（型定義、バリデーション、ユースケース）の実装"},
            {"type": "⚙️ Infrastructure", "label": "feature", "desc": "Infrastructure層（Repository実装、外部ストレージ連携）の実装"},
            {"type": "⚙️ UI/UX", "label": "feature", "desc": "Presentation層（コンポーネント、ページ、アニメーション）の実装"},
            {"type": "🧪 Test", "label": "test", "desc": "単体テストおよび統合テストの実装"},
            {"type": "🏁 Doc", "label": "documentation", "desc": "READMEや仕様ドキュメントの更新"}
        ]

        # 3. 子タスク作成 & コメント追加
        for task in child_tasks:
            child_title = f"{task['type']} - {feature['title']}"
            child_body = f"{task['desc']}\n\nParent: #{epic_id}"
            
            child_url = run_gh_command([
                "issue", "create",
                "--title", child_title,
                "--body", child_body,
                "--label", task['label']
            ])
            child_id = child_url.split('/')[-1]
            
            # 子タスクへの具体的な指示コメント
            run_gh_command([
                "issue", "comment", child_id,
                "--body", f"## 🛠 実行内容\n- **対象**: {task['type']}\n- **目的**: {feature['title']} の{task['type']}部分の実装\n- **親Issue**: #{epic_id}"
            ])

            # EPIC側への進捗管理追記（チェックリスト）
            run_gh_command([
                "issue", "comment", epic_id,
                "--body", f"- [ ] #{child_id} {child_title}"
            ])
            
            print(f"    -> Created Child #{child_id} ({task['type']})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bulk_register.py <prd_file_path>")
        sys.exit(1)
        
    prd_file = sys.argv[1]
    features = parse_prd_feature_list(prd_file)
    
    if not features:
        print("No features found in '4.1 機能一覧'. Check the format.")
        sys.exit(0)
        
    register_tasks(features)
    print("\n=== Bulk Registration Completed ===")
