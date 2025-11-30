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

## 4. 環境変数

1. 「設定」→「環境変数」→「編集」
2. 必要に応じて追加:
   - `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
   - `CLOTHING_TABLE`: `ClothingItems`
3. 「保存」

## 5. IAM権限

1. 「設定」→「アクセス権限」
2. 実行ロール名をクリック
3. 「許可を追加」→「ポリシーをアタッチ」
4. 対応するポリシーをアタッチ (iam/フォルダ参照)

## 6. 関数URL作成

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

## 7. テスト

1. `web/index.html` をブラウザで開く
2. 対応するテストボタンをクリック
3. 成功を確認

## 各関数の設定まとめ

| 関数名 | タイムアウト | 環境変数 | IAMポリシー |
|--------|------------|---------|------------|
| bedrock-tester | 30秒 | MODEL_ID | bedrock-tester-policy.json |
| db-tester | 30秒 | MODEL_ID, CLOTHING_TABLE | db-tester-policy.json |
| s3-tester | 30秒 | MODEL_ID, CLOTHING_TABLE, BUCKET_NAME | s3-tester-policy.json |
| weather-fetcher | 10秒 | なし | weather-fetcher-policy.json |
| calendar-fetcher | 10秒 | なし | calendar-fetcher-policy.json |
| coordinate-recommender | 30秒 | MODEL_ID, CLOTHING_TABLE | coordinate-recommender-policy.json |
| full-coordinator | 30秒 | MODEL_ID, CLOTHING_TABLE, BUCKET_NAME | full-coordinator-policy.json |

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
