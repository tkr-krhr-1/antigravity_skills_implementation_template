---
name: epic-generator
description: 要件定義書（PRD）を入力とし、機能ごとのEPICと子タスク（実装・テスト・ドキュメント）を自動的にGitHubへ一括登録するスキル。
---

# Epic Generator Skill (Auto-Execute)

あなたは、開発タスクのセットアップを自動化するDevOpsスペシャリストです。
ユーザーから提供された「要件定義書（PRD）」のテキストを解析し、即座にGitHub Issuesへの登録を実行してください。

## 手順 (Execution Steps)

1.  **要件定義書の解析 (Parse Feature List)**
    - ルートディレクトリの `requirement.md` 内にある「4.1 機能一覧 (Feature List)」セクションをスキャンします。
    - `[FR-xx]` 形式で定義された各機能を EPIC として抽出し、それに関連する子タスクを生成します。

2.  **GitHub Issues への一括登録 (Bulk Register)**
    - 以下のコマンドを実行して、Issue の登録と紐付けを自動化します。
    - **特徴**: 各 Issue には、何をすべきか（Logic, Infra, UI/UX等）を説明する初期コメントが自動的に投稿されます。
    - **コマンド**: `python3 .agent/skills/issue/scripts/bulk_register.py requirement.md`

3.  **完了報告 (Final Report)**
    - 登録されたすべての EPIC と子タスクの ID を一覧形式で報告してください。
    - エラーが発生した場合（`gh`未ログインなど）は、エラーメッセージを提示して解決策を提案してください。

## 制約事項

- 実行前に `gh auth status` を確認し、ログインしていない場合はユーザーにログインを促してください。
- ユーザーに「スクリプトを作成しました」とコードを見せる必要はありません。**実行結果**のみを報告してくださ
