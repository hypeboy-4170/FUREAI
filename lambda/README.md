# Lambda関数一覧

## 単体テスト用Lambda関数

### 1. bedrock_tester.py
- **機能**: Bedrock (Claude Sonnet 4.5) 疎通確認
- **入力**: `{ "question": "質問文" }`
- **出力**: `{ "answer": "AIの回答" }`
- **必要な権限**: `bedrock:InvokeModel`

### 2. db_tester.py
- **機能**: DBデータだけでコーデ提案
- **入力**: なし
- **出力**: `{ "dbItems": [...], "recommendation": "AI提案" }`
- **必要な権限**: `dynamodb:Scan`, `bedrock:InvokeModel`
- **テーブル**: `fureai-clothing-items`

### 3. s3_tester.py
- **機能**: 画像→Bedrock分析→DB登録→コーデ提案
- **入力**: `{ "imageData": "base64..." }`
- **出力**: `{ "s3Upload": {...}, "imageAnalysis": {...}, "dbRegistration": {...}, "recommendation": "..." }`
- **必要な権限**: `s3:PutObject`, `bedrock:InvokeModel`, `dynamodb:PutItem`
- **バケット**: `fureai-clothing-images`
- **テーブル**: `fureai-clothing-items`
- **フロー**: S3アップロード → Bedrockで画像分析 → DB登録 → AIコーデ提案

### 4. weather_api_fetcher.py
- **機能**: OpenWeatherMap API疎通確認
- **入力**: `{ "location": "Tokyo" }`
- **出力**: `{ "temp": 20, "condition": "晴れ", "humidity": 60 }`
- **必要な権限**: なし（外部API呼び出し）

### 5. calendar_fetcher.py
- **機能**: Googleカレンダー疎通確認
- **入力**: なし
- **出力**: `{ "events": [...] }`
- **必要な権限**: なし（外部API呼び出し）

## 全体統合Lambda関数

### 6. full_coordinator.py ⭐
- **機能**: 全体統合（S3 + DB + 天気 + 予定 → Bedrock）
- **入力**: `{ "userId": "user001", "location": "Tokyo" }`
- **出力**: 
```json
{
  "data": {
    "clothing": {...},
    "user": {...},
    "weather": {...},
    "schedule": {...}
  },
  "recommendation": "AIの提案"
}
```
- **必要な権限**: 
  - `bedrock:InvokeModel`
  - `dynamodb:GetItem`
  - `s3:ListObjects`, `s3:GetObject`

## デプロイ手順

1. Lambda関数を作成
2. コードをアップロード
3. **環境変数を設定**:
   - `BUCKET_NAME`: fureai-clothing-images
   - `TABLE_NAME`: fureai-clothing-items
   - `MODEL_ID`: jp.anthropic.claude-sonnet-4-5-20250929-v1:0
4. 関数URLを有効化（認証: NONE, CORS有効）
5. タイムアウトを30秒に設定
6. IAMロールに必要な権限を追加
7. `web/config.js`に関数URLを設定

## IAMポリシー例

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:*:table/fureai-clothing-items"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::fureai-clothing-images",
        "arn:aws:s3:::fureai-clothing-images/*"
      ]
    }
  ]
}
```
