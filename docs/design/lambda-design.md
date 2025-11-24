# Lambda関数設計

## 概要

FUREAIシステムは6つのLambda関数で構成されます。

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

## 1. BedrockTester

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
  "action": "bedrockTest",
  "question": "こんにちは。今日の天気はどうですか？"
}
```

### 出力例

```json
{
  "answer": "こんにちは！申し訳ございませんが、私はリアルタイムの天気情報にアクセスできません..."
}
```

### 環境変数
- なし

### IAM権限
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 2. PresignedUrlGenerator

### 責務
- S3 Presigned URL生成
- HTMLから直接S3にアップロード可能にする

### ファイル
`lambda/presigned_url_generator.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "action": "getPresignedUrl",
  "itemId": "tops_001",
  "fileType": "image/jpeg"
}
```

### 出力例

```json
{
  "uploadUrl": "https://fureai-clothing-images.s3.amazonaws.com/uploads/tops_001.jpg?X-Amz-...",
  "s3Key": "uploads/tops_001.jpg",
  "bucket": "fureai-clothing-images"
}
```

### 環境変数
- `BUCKET_NAME`: fureai-clothing-images

### IAM権限
- `s3:PutObject`
- `logs:*`

### 設定
- **タイムアウト**: 10秒
- **メモリ**: 128MB
- **ランタイム**: Python 3.12

---

## 3. ImageAnalyzer

### 責務
- 画像からAIが自動でデータ生成
- DynamoDBに自動登録

### ファイル
`lambda/image_analyzer.py`

### トリガー
- S3イベント（uploads/フォルダに画像アップロード時）

### 処理フロー

```
1. S3から画像取得
2. Bedrockで画像分析
   - itemName（例: 白シャツ）
   - category（tops/pants/outer）
   - color（white/black/brown等）
   - style（formal/casual/business_casual）
   - season（spring/summer/autumn/winter）
   - warmth（warm/cool）
3. DynamoDBに自動登録
```

### 入力
- S3イベント（自動）

### 出力例

```json
{
  "itemId": "tops_001",
  "data": {
    "itemName": "白シャツ",
    "category": "tops",
    "color": "white",
    "style": "formal",
    "season": ["spring", "summer", "autumn"],
    "warmth": "cool"
  },
  "message": "Successfully analyzed and registered"
}
```

### 環境変数
- `BUCKET_NAME`: fureai-clothing-images
- `TABLE_NAME`: ClothingItems

### IAM権限
- `s3:GetObject`
- `dynamodb:PutItem`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 60秒
- **メモリ**: 512MB
- **ランタイム**: Python 3.12

---

## 4. CoordinateRecommender

### 責務
- コーディネート提案（メイン機能）

### ファイル
`lambda/coordinate_recommender.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "schedule": "クライアント訪問",
  "weather": "気温25度 晴れ"
}
```

### 出力例

```json
{
  "tops": {
    "itemId": "tops_001",
    "reason": "茶シャツはフォーマルな印象"
  },
  "pants": {
    "itemId": "pants_002",
    "reason": "黒スラックスはフォーマルに最適"
  },
  "outer": {
    "itemId": null,
    "reason": "暖かいのでアウター不要"
  },
  "overall_comment": "クライアント訪問に最適なコーディネート"
}
```

### 環境変数
- `CLOTHING_TABLE`: ClothingItems
- `HISTORY_TABLE`: WearHistory

### IAM権限
- `dynamodb:Scan`
- `dynamodb:Query`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 256MB
- **ランタイム**: Python 3.12

---

## 5. WeatherAPIFetcher

### 責務
- OpenWeatherMap APIから現在の天気取得
- コーディネート提案

### ファイル
`lambda/weather_api_fetcher.py`

### トリガー
- Lambda Function URL (HTTPS)

### 入力例

```json
{
  "action": "weatherAPI",
  "location": "Tokyo"
}
```

### 出力例

```json
{
  "weather": {
    "temp": 20,
    "condition": "曇り",
    "humidity": 60,
    "source": "api"
  },
  "coordinate": {
    "tops": {
      "itemId": "tops_001",
      "reason": "茶シャツは適温"
    },
    "pants": {
      "itemId": "pants_001",
      "reason": "ベージュチノパンは快適"
    },
    "outer": {
      "itemId": null,
      "reason": "アウター不要"
    },
    "overall_comment": "東京の天気に最適なコーディネート"
  }
}
```

### 環境変数
- `CLOTHING_TABLE`: ClothingItems
- `WEATHER_API_KEY`: OpenWeatherMap APIキー（オプション）

### IAM権限
- `dynamodb:Scan`
- `bedrock:InvokeModel`
- `logs:*`

### 設定
- **タイムアウト**: 30秒
- **メモリ**: 256MB
- **ランタイム**: Python 3.12
- **依存**: requests（Lambdaレイヤー必要）

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

#### BedrockTester
```python
200: Bedrock応答成功
400: questionパラメータ不足
500: Bedrock呼び出し失敗
```

#### PresignedUrlGenerator
```python
200: Presigned URL生成成功
400: itemId/fileType不足
500: S3操作失敗
```

#### ImageAnalyzer
```python
200: 画像分析・登録成功
500: S3取得失敗 / Bedrock失敗 / DynamoDB登録失敗
```

#### CoordinateRecommender
```python
200: コーディネート提案成功
400: schedule/weather不足
500: DynamoDB取得失敗 / Bedrock失敗
```

#### WeatherAPIFetcher
```python
200: 天気取得・提案成功
400: locationパラメータ不足
500: OpenWeatherMap API失敗 / DynamoDB失敗 / Bedrock失敗
```

#### CalendarFetcher
```python
200: 予定・天気取得・提案成功
400: locationパラメータ不足
500: Google Calendar API失敗 / DynamoDB失敗 / Bedrock失敗
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

## 段階的テスト順序

1. **BedrockTester** - Bedrock単体
2. **ImageAnalyzer** - S3 + Bedrock + DynamoDB
3. **CoordinateRecommender** - DynamoDB + Bedrock
4. **WeatherAPIFetcher** - OpenWeatherMap API + DynamoDB + Bedrock
5. **CalendarFetcher** - Google Calendar API + 天気 + DynamoDB + Bedrock

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
| BedrockTester | 2秒 | 128MB | $0.04 |
| PresignedUrlGenerator | 1秒 | 128MB | $0.02 |
| ImageAnalyzer | 5秒 | 512MB | $0.42 |
| CoordinateRecommender | 3秒 | 256MB | $0.13 |
| WeatherAPIFetcher | 3秒 | 256MB | $0.13 |
| CalendarFetcher | 3秒 | 256MB | $0.13 |
| **合計** | - | - | **$0.87** |

※ Bedrock料金は別途（$0.003/1000入力トークン、$0.015/1000出力トークン）
