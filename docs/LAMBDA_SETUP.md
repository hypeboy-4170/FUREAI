# Lambda関数作成手順

## 1. Lambda関数の作成

### AWSコンソール
1. Lambda → 「関数の作成」
2. 「一から作成」を選択
3. 設定:
   - **関数名**: `fureai-bedrock-tester` (例)
   - **ランタイム**: Python 3.12
   - **アーキテクチャ**: x86_64
4. 「関数の作成」

## 2. コードのデプロイ

1. 「コード」タブ
2. `lambda_function.py` の内容を削除
3. 対応する `.py` ファイルの内容をコピペ
4. 「Deploy」ボタンをクリック

## 3. 一般設定

1. 「設定」→「一般設定」→「編集」
2. 設定:
   - **タイムアウト**: 30秒
   - **メモリ**: 128 MB (デフォルトでOK)
3. 「保存」

## 4. IAM権限

1. 「設定」→「アクセス権限」
2. 実行ロール名をクリック
3. 「許可を追加」→「ポリシーをアタッチ」
4. 対応するポリシーをアタッチ (iam/フォルダ参照)

## 5. 関数URL作成

1. 「設定」→「関数URL」→「関数URLを作成」
2. 設定:
   - **認証タイプ**: NONE
   - **CORS を設定**: ✅ 有効
     - Allow origin: `*`
     - Allow methods: `POST`
     - Allow headers: `content-type`
     - Max age: `300`
3. 「保存」
4. 発行されたURLをコピー → `web/config.js` に貼り付け

## 6. テスト

1. `web/index.html` をブラウザで開く
2. 対応するテストボタンをクリック
3. 成功を確認

## 各関数の設定まとめ

| 関数名 | タイムアウト | IAMポリシー |
|--------|------------|------------|
| bedrock-tester | 30秒 | bedrock-tester-policy.json |
| db-tester | 30秒 | db-tester-policy.json |
| s3-tester | 30秒 | s3-tester-policy.json |
| weather-fetcher | 30秒 | weather-fetcher-policy.json |
| calendar-fetcher | 30秒 | calendar-fetcher-policy.json |
| coordinate-recommender | 30秒 | coordinate-recommender-policy.json |
| full-coordinator | 30秒 | full-coordinator-policy.json |

## トラブルシューティング

### 502 Bad Gateway
- CloudWatch Logsを確認
- タイムアウトが短すぎる → 30秒に変更
- IAM権限不足 → ポリシーを確認

### CORS エラー
- 関数URLのCORS設定を確認
- Allow headers に `content-type` を追加

### AccessDeniedException
- IAM権限を確認
- Bedrockモデルアクセスを有効化
