# 入力例
ユーザー: 「Issue #102 を完了して。」
（※背景：ユーザーは `search_service.py` を修正し、Elasticsearchのクエリロジックを変更している状態）

# 出力例
```bash
git add . && \
git commit -m "perf: 検索クエリの最適化と高速化 (#102)" && \
git push origin $(git branch --show-current) && \
gh issue comment 102 --body "## 実装内容
- Elasticsearchのクエリビルダを見直し、ネスティングを解消
- 検索結果にサムネイル画像URLを含めるようレスポンス型を変更
- 不要なデバッグログの削除

実装内容に基づきIssueをクローズします。" && \
gh issue close 102