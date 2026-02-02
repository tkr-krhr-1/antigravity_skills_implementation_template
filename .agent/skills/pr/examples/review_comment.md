# シニアエンジニアによるレビューコメント例

## 出力例

### 🤖 Senior Engineer Auto-Review

PR作成お疲れ様です。実装内容を確認しました。
全体的にクリーンアーキテクチャに則った良い構成ですが、数点、セキュリティとパフォーマンスの観点で懸念があります。

### ⚠️ 重要課題 (Must Fix)

**1. エラーハンドリングの不足 (`src/api/handler.ts`)**
```typescript
try {
  await processData(input);
} catch (e) {
  console.log(e); // 🚨 ここ
}
エラーをログに出すだけで処理を続行していますが、これは危険です。呼び出し元にエラーを伝播させるか、適切なステータスコード（500等）を返却すべきです。
💡 改善提案 (Suggestion)
2. N+1問題の可能性 (src/services/user.ts) ループ内で getUserDetail(id) を都度呼び出しています。 IDリストを作成し、getUsersByIds(ids) のように一括取得するクエリに変更することで、DBアクセス回数を劇的に減らせます。
📝 質問
• const MAX_RETRY = 3; となっていますが、この回数の根拠はありますか？外部APIのレートリミットを考慮すると、指数バックオフ（Exponential Backoff）の導入を検討しても良いかもしれません。
