# Lambda関数設計

## 概要

FUREAIシステムは以下のLambda関数で構成されます。

### 実装状況
- ✅ **bedrock_tester** - 実装済み
- 📝 **db_tester** - 設計のみ
- 📝 **s3_tester** - 設計のみ
- 📝 **weather_api_fetcher** - 設計のみ
- 📝 **calendar_fetcher** - 設計のみ
- 📝 **coordinate_recommender** - 設計のみ
- 📝 **full_coordinator** - 設計のみ

---

## Lambda関数構成

```
Web (index.html)
  ↓
  ├→ BedrockTester (Bedrock疎通確認)
  │   └→ Bedrock (Claude 3.5 Sonnet)
  │
  ├→ PresignedUrlGenerator (画像アップロード)
  │   └→ S3 (Presigned URL生成)
  │       ↓
  │       ImageAnalyzer (S3トリガー)
  │       ├→ S3 (画像取得)
  │       ├→ Bedrock (画像分析)
  │       └→ DynamoDB (自動登録)
  │
  ├→ CoordinateRecommender (メイン機能)
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  ├→ WeatherAPIFetcher (OpenWeatherMap連携)
  │   ├→ OpenWeatherMap API (現在の天気)
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  └→ CalendarFetcher (Googleカレンダー連携)
      ├→ Google Calendar API (本日の予定)
      ├→ 天気情報 (簡易版)
      ├→ DynamoDB (ClothingItems)
      └→ Bedrock (コーディネート提案)
```

---

## 1. bedrock_tester ✅ 実装済み

### 責務
- Bedrock単体の疎通確認
- DynamoDB不要

### ファイル
`lambda/bedrock_tester.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "question": "こんにちは"
}
```

### 出力例

```json
{
  "answer": "こんにちは！何かお手伝いできることはありますか？"
}
```

### 環境変数
- `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`

### IAM権限
- `bedrock:InvokeModel`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12
- **関数URL**: 有効（認証なし、CORS有効）

---

## 2. db_tester 📝 設計のみ

### 責務
- DynamoDBデータ取得
- Bedrockでコーディネート提案

### ファイル
`lambda/db_tester.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{}
```

### 出力例

```json
{
  "dbItems": [
    {"itemId": "tops_001", "category": "tops", "color": "白"},
    {"itemId": "pants_001", "category": "pants", "color": "黒"}
  ],
  "recommendation": "白シャツと黒パンツの組み合わせがおすすめです"
}
```

### 環境変数
- `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
- `CLOTHING_TABLE`: `ClothingItems`

### IAM権限
- `dynamodb:Scan`
- `dynamodb:GetItem`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 3. s3_tester 📝 設計のみ

### 責務
- 画像アップロード
- Bedrockで画像分析
- DynamoDB登録
- コーディネート提案

### ファイル
`lambda/s3_tester.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "imageData": "data:image/jpeg;base64,..."
}
```

### 出力例

```json
{
  "s3Upload": {
    "bucket": "fureai-clothing-images",
    "key": "uploads/item_001.jpg"
  },
  "imageAnalysis": {
    "category": "tops",
    "color": "白",
    "season": "all",
    "formality": "business"
  },
  "dbRegistration": {
    "itemId": "item_001"
  },
  "recommendation": "白シャツを使ったコーディネート提案"
}
```

### 環境変数
- `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
- `CLOTHING_TABLE`: `ClothingItems`
- `BUCKET_NAME`: `fureai-clothing-images`

### IAM権限
- `s3:GetObject`
- `s3:PutObject`
- `dynamodb:PutItem`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 4. weather_api_fetcher 📝 設計のみ

### 責務
- OpenWeatherMap API呼び出し
- 天気情報取得

### ファイル
`lambda/weather_api_fetcher.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "location": "Tokyo"
}
```

### 出力例

```json
{
  "temp": 20,
  "condition": "曇り",
  "humidity": 60
}
```

### 環境変数
- なし

### IAM権限
- `logs:*`

### 設定
- **タイムアウト**: 10秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 5. calendar_fetcher 📝 設計のみ

### 責務
- Googleカレンダー API呼び出し
- 予定情報取得

### ファイル
`lambda/calendar_fetcher.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{}
```

### 出力例

```json
{
  "events": [
    {"time": "10:00", "summary": "会議"},
    {"time": "14:00", "summary": "プレゼン"}
  ]
}
```

### 環境変数
- なし

### IAM権限
- `logs:*`

### 設定
- **タイムアウト**: 10秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

## 6. coordinate_recommender 📝 設計のみ

### 責務
- コーディネート提案（メイン機能）

### ファイル
`lambda/coordinate_recommender.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "schedule": "会社でプレゼン",
  "weather": "15度 曇り"
}
```

### 出力例

```json
{
  "tops": {"itemId": "tops_001", "reason": "白シャツはフォーマル"},
  "pants": {"itemId": "pants_001", "reason": "黒パンツは定番"},
  "outer": {"itemId": "outer_001", "reason": "ジャケットで印象アップ"},
  "overall_comment": "プレゼンに最適なコーディネート"
}
```

### 環境変数
- `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
- `CLOTHING_TABLE`: `ClothingItems`

### IAM権限
- `dynamodb:Scan`
- `dynamodb:GetItem`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 7. full_coordinator 📝 設計のみ

### 責務
- S3 + DB + 天気 + 予定 → Bedrock → 統合提案

### ファイル
`lambda/full_coordinator.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "userId": "user001",
  "location": "Tokyo"
}
```

### 出力例

```json
{
  "data": {
    "clothing": {"count": 10},
    "weather": {"temp": 20, "condition": "晴れ"},
    "schedule": {"events": [{"time": "10:00", "summary": "会議"}]}
  },
  "recommendation": "本日のおすすめコーディネート..."
}
```

### 環境変数
- `MODEL_ID`: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
- `CLOTHING_TABLE`: `ClothingItems`
- `BUCKET_NAME`: `fureai-clothing-images`

### IAM権限
- `s3:GetObject`
- `dynamodb:Scan`
- `dynamodb:GetItem`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## HTTPステータスコード設計

### 成功レスポンス

| コード | 意味 | 使用ケース |
|--------|------|------------|
| **200** | OK | 正常処理完了 |

### クライアントエラー (4xx)

| コード | 意味 | 使用ケース | エラーメッセージ例 |
|--------|------|------------|--------------------|
| **400** | Bad Request | 必須パラメータ不足 | `{"error": "question is required"}` |
| **400** | Bad Request | 不正なJSON形式 | `{"error": "Invalid JSON format"}` |
| **400** | Bad Request | 不正なファイルタイプ | `{"error": "Invalid file type"}` |
| **404** | Not Found | リソース未存在 | `{"error": "Item not found"}` |

### サーバーエラー (5xx)

| コード | 意味 | 使用ケース | エラーメッセージ例 |
|--------|------|------------|--------------------|
| **500** | Internal Server Error | DynamoDB接続失敗 | `{"error": "Database connection failed"}` |
| **500** | Internal Server Error | Bedrock呼び出し失敗 | `{"error": "AI service unavailable"}` |
| **500** | Internal Server Error | S3操作失敗 | `{"error": "Storage service error"}` |
| **500** | Internal Server Error | 予期しないエラー | `{"error": "<例外メッセージ>"}` |

### 関数別ステータスコード

#### bedrock_tester ✅
```python
200: Bedrock応答成功
400: questionパラメータ不足
500: Bedrock呼び出し失敗
```

#### db_tester 📝
```python
200: DB取得・提案成功
500: DynamoDB失敗 / Bedrock失敗
```

#### s3_tester 📝
```python
200: S3アップロード・分析・登録・提案成功
400: imageData不足
500: S3失敗 / Bedrock失敗 / DynamoDB失敗
```

#### weather_api_fetcher 📝
```python
200: 天気取得成功
400: locationパラメータ不足
500: OpenWeatherMap API失敗
```

#### calendar_fetcher 📝
```python
200: 予定取得成功
500: Google Calendar API失敗
```

#### coordinate_recommender 📝
```python
200: コーディネート提案成功
400: schedule/weather不足
500: DynamoDB失敗 / Bedrock失敗
```

#### full_coordinator 📝
```python
200: 統合提案成功
400: userId/location不足
500: S3/DynamoDB/Bedrock失敗
```

### レスポンス形式

#### 成功時 (200)
```json
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS"
  },
  "body": "{\"answer\": \"...\"}"  // JSON文字列
}
```

#### エラー時 (4xx/5xx)
```json
{
  "statusCode": 400,
  "headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS"
  },
  "body": "{\"error\": \"question is required\"}"
}
```

### エラーハンドリング実装例

```python
try:
    # 必須パラメータチェック
    if not question:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'question is required'})
        }
    
    # 正常処理
    result = process_request()
    return {
        'statusCode': 200,
        'body': json.dumps(result, ensure_ascii=False)
    }
    
except ClientError as e:  # AWS SDK エラー
    return {
        'statusCode': 500,
        'body': json.dumps({'error': f'AWS service error: {str(e)}'})
    }
except Exception as e:  # その他のエラー
    return {
        'statusCode': 500,
        'body': json.dumps({'error': str(e)})
    }
```

---

## 段階的実装順序

1. ✅ **bedrock_tester** - Bedrock単体（実装済み）
2. 📝 **db_tester** - DynamoDB + Bedrock
3. 📝 **s3_tester** - S3 + Bedrock + DynamoDB
4. 📝 **weather_api_fetcher** - OpenWeatherMap API
5. 📝 **calendar_fetcher** - Google Calendar API
6. 📝 **coordinate_recommender** - メイン機能
7. 📝 **full_coordinator** - 全体統合

---

## デプロイ

### 自動デプロイ

```bash
./scripts/deploy_lambda.sh
```

---

## コスト見積もり

### 月間100回実行

| 関数 | 実行時間 | メモリ | コスト/月 |
|------|---------|--------|----------|
| bedrock_tester | 2秒 | 128MB | $0.04 |
| db_tester | 3秒 | 128MB | $0.06 |
| s3_tester | 5秒 | 128MB | $0.10 |
| weather_api_fetcher | 2秒 | 128MB | $0.04 |
| calendar_fetcher | 2秒 | 128MB | $0.04 |
| coordinate_recommender | 3秒 | 128MB | $0.06 |
| full_coordinator | 5秒 | 128MB | $0.10 |
| **合計** | - | - | **$0.44** |

※ Bedrock料金は別途（$0.003/1000入力トークン、$0.015/1000出力トークン）
