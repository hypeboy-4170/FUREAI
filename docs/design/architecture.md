# FUREAI システムアーキテクチャ

## システム構成

### Lambda関数: 6つ

| Lambda関数 | 責務 | トリガー | テスト種別 |
|-----------|------|---------|----------|
| **BedrockTester** | Bedrock疎通確認 | Lambda Function URL | 単体 |
| **PresignedUrlGenerator** | S3署名付きURL生成 | Lambda Function URL | 単体 |
| **ImageAnalyzer** | 画像分析・自動登録 | S3イベント | 単体 |
| **CoordinateRecommender** | コーディネート提案 | Lambda Function URL | システム |
| **WeatherAPIFetcher** | 天気API連携 | Lambda Function URL | システム |
| **CalendarFetcher** | カレンダー連携 | Lambda Function URL | システム |

### データフロー

```
Web UI (index.html)
  ↓
  ├→ BedrockTester (Lambda Function URL)
  │   └→ Bedrock (Claude 3.5 Sonnet)
  │
  ├→ PresignedUrlGenerator (Lambda Function URL)
  │   └→ S3 (Presigned URL生成)
  │       ↓
  │       画像アップロード（HTML → S3直接）
  │       ↓
  │       ImageAnalyzer (S3トリガー)
  │       ├→ S3 (画像取得)
  │       ├→ Bedrock (画像分析)
  │       └→ DynamoDB (自動登録)
  │
  ├→ CoordinateRecommender (Lambda Function URL)
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  ├→ WeatherAPIFetcher (Lambda Function URL)
  │   ├→ OpenWeatherMap API (現在の天気)
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  └→ CalendarFetcher (Lambda Function URL)
      ├→ Google Calendar API (本日の予定)
      ├→ 天気情報 (簡易版)
      ├→ DynamoDB (ClothingItems)
      └→ Bedrock (コーディネート提案)
```

---

## データ登録方法

### 方法1: 画像アップロード（自動分析）

**HTML UIから**:
1. itemIdを入力（例: tops_001）
2. 画像ファイルを選択
3. 「S3にアップロード」ボタンをクリック
4. ImageAnalyzerが自動で画像分析
5. DynamoDBに自動登録

**AWS CLIから**:
```bash
# S3に画像アップロード（ImageAnalyzerが自動トリガー）
aws s3 cp tops_001.jpg s3://fureai-clothing-images/uploads/tops_001.jpg
```

### 方法2: 手動でDynamoDBに登録

```bash
# imageKeyを含めてデータ投入
aws dynamodb put-item --table-name ClothingItems --item '{
  "itemId": {"S": "tops_001"},
  "imageKey": {"S": "uploads/tops_001.jpg"},
  "itemName": {"S": "茶シャツ"},
  "category": {"S": "tops"},
  "color": {"S": "brown"},
  "style": {"S": "formal"},
  "season": {"L": [{"S": "spring"}, {"S": "summer"}, {"S": "autumn"}]},
  "warmth": {"S": "cool"}
}'
```

---

## アーキテクチャの特徴

### 1. API Gateway不要
- **Lambda Function URL**を使用
- 各Lambda関数に直接HTTPSアクセス
- CORS設定はLambda内で実装
- コスト削減（API Gateway料金不要）

### 2. 段階的テスト可能
- **単体テスト**: Bedrock、S3、画像分析を個別に検証
- **システムテスト**: 手動入力、天気API、カレンダー連携を統合検証

### 3. 自動化と手動のハイブリッド
- **自動**: 画像アップロード → AI分析 → DB登録
- **手動**: AWS CLIでデータ直接投入も可能

### 4. 外部API統合
- **OpenWeatherMap**: 現在の天気を自動取得
- **Google Calendar**: 本日の予定を自動取得（モック対応）

---

## DynamoDBデータ構造

### ClothingItems（7アイテム）

```json
{
  "itemId": "tops_001",
  "imageKey": "uploads/tops_001.jpg",
  "itemName": "茶シャツ",
  "category": "tops",
  "color": "brown",
  "style": "formal",
  "season": ["spring", "summer", "autumn"],
  "warmth": "cool"
}
```

**サンプルデータ一覧**:
- tops_001: 茶シャツ（formal）
- tops_002: 黒ニット（casual）
- tops_003: グレーTシャツ（casual）
- pants_001: ベージュチノパン（business_casual）
- pants_002: 黒スラックス（formal）
- outer_001: トレンチコート（business_casual）
- outer_002: ダウンジャケット（casual）

### WearHistory

```json
{
  "itemId": "tops_001",
  "wornDate": "2025-01-20"
}
```

---

## セットアップ手順

### 1. DynamoDB + S3作成

```bash
# CloudShellで実行
cd FUREAI
chmod +x scripts/*.sh
./scripts/setup_all.sh
```

**実行内容**:
- DynamoDBテーブル作成（ClothingItems, WearHistory）
- サンプルデータ7件投入（**imageKey含む**）
- S3バケット作成

### 2. Lambda関数デプロイ

```bash
./scripts/deploy_lambda.sh
```

**作成される関数**:
- BedrockTester
- PresignedUrlGenerator
- ImageAnalyzer
- CoordinateRecommender
- WeatherAPIFetcher
- CalendarFetcher

### 3. Lambda Function URL設定

各Lambda関数にFunction URLを作成（スクリプトで自動実行）:
```bash
aws lambda create-function-url-config \
  --function-name BedrockTester \
  --auth-type NONE \
  --cors AllowOrigins='*'
```

### 4. HTMLにLambda URL設定

`web/index.html`を開いて、Lambda URLを設定:
```javascript
const LAMBDA_URL = 'https://YOUR_URL.lambda-url.ap-northeast-1.on.aws/';
```

### 5. テスト実行

1. `web/index.html`をブラウザで開く
2. 単体テスト実行（Bedrock疎通確認）
3. 画像アップロードテスト
4. システムテスト（テストシナリオ選択）

---

## まとめ

### 最終構成

```
HTML UI → Lambda Function URL → Lambda関数 → AWS Services
```

### Lambda関数数

- **単体テスト用**: 3つ（BedrockTester, PresignedUrlGenerator, ImageAnalyzer）
- **システムテスト用**: 3つ（CoordinateRecommender, WeatherAPIFetcher, CalendarFetcher）
- **合計**: 6つ

### データ登録

- **自動**: HTMLから画像アップロード → AI分析 → DB登録
- **手動**: AWS CLIでDynamoDBに直接投入も可能

### コスト見積もり（月間100回実行）

| サービス | 料金 |
|---------|------|
| Lambda | $0.87 |
| DynamoDB | $0.01 |
| S3 | $0.01 |
| Bedrock | $0.45 |
| **合計** | **$1.34** |

※ 無料利用枠内であれば実質無料

これが段階的テスト可能で効率的な構成です！
