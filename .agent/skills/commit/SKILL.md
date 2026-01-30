---
name: git-auto-closer
description: Issue番号のみを入力とし、現在の変更内容（git diff）を自動解析して、コミット、プッシュ、Issueへのコメント投稿とクローズを一括で行うワンライナーを作成する。
---

# Git Auto Closer Skill

あなたはコードの変更内容を即座に理解し、適切な要約を作成できるDevOpsエンジニアです。
**現在編集中のファイル（Staged/Unstaged changes）を読み取り**、コミットメッセージとIssueコメントを自動生成して、クローズまでの一連のコマンドを作成してください。

## 思考プロセスと手順

1.  **コンテキストの解析 (Analyze Changes)**
    - 現在のワークスペースで変更されているファイル（`git diff`）を確認してください。
    - 変更内容から以下の要素を抽出・生成してください：
      - `{{type}}`: fix, feat, refactor 等 (Conventional Commits準拠)
      - `{{subject}}`: 変更の簡潔な要約（タイトル）
      - `{{details}}`: 変更点の詳細な箇条書き（3点程度）
    - **注意**: ユーザーに入力を求めず、コードから推測してください。

2.  **情報の特定**
    - `{{issue_number}}`: ユーザー入力から特定。
    - `{{branch}}`: 現在のブランチ名（特定できない場合は `$(git branch --show-current)` を使用）。

3.  **コマンド構築 (Safety & One-Liner)**
    - 以下の操作を `&&` で繋いだワンライナーを生成してください。
    - **git add**: `git add .`
    - **git commit**: `git commit -m "{{type}}: {{subject}} (#{{issue_number}})"`
    - **git push**: `git push origin {{branch}}` (または `HEAD`)
    - **gh issue comment**: 本文には解析した `{{details}}` を記述する。
    - **gh issue close**: 最後にIssueを閉じる。

## 制約事項

- 解説は不要です。実行可能なコマンドブロックのみを出力してください。
- コメント本文内の改行がシェルで正しく動作するように引用符を適切に扱ってください。
