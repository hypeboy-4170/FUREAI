# 🚀 クイックスタートガイド

## 構成概要

```
単体テスト (個別機能確認)
├── 1. Bedrockテスト
├── 2. DBテスト
├── 3. S3テスト
├── 4. 天気テスト
└── 5. 予定テスト

全体統合テスト
└── 6. フルコーディネート提案
    └── S3 → DB → 天気 → 予定 → Bedrock → HTML
```

## セットアップ手順

### 1. AWS リソース作成

#### DynamoDBテーブル
```bash
テーブル名: fureai-clothing-items
パーティションキー: itemId (String)
```

#### S3バケット
```bash
バケット名: fureai-clothing-images
リージョン: ap-northeast-1
```

### 2. Lambda関数デプロイ

各Lambda関数を作成（Python 3.12）:

| 関数名 | ファイル | 説明 |
|--------|---------|------|
| fureai-bedrock-tester | bedrock_tester.py | Bedrock疎通 |
| fureai-db-tester | db_tester.py | DB疎通 |
| fureai-s3-tester | s3_tester.py | S3疎通 |
| fureai-weather-tester | weather_api_fetcher.py | 天気API |
| fureai-calendar-tester | calendar_fetcher.py | 予定API |
| fureai-full-coordinator | full_coordinator.py | **全体統合** |

#### 共通設定
- タイムアウト: 30秒
- 関数URL: 有効（認証: NONE, CORS有効）
- IAMロール: 以下の権限を追加

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": "bedrock:InvokeModel", "Resource": "*"},
    {"Effect": "Allow", "Action": "dynamodb:*", "Resource": "*"},
    {"Effect": "Allow", "Action": "s3:*", "Resource": "*"}
  ]
}
```

### 3. Bedrockモデル有効化

1. Amazon Bedrockコンソール (ap-northeast-1)
2. Model access → Manage model access
3. **Claude Sonnet 4.5** を有効化

### 4. Web UI設定

```bash
cd web
cp config.js.example config.js
# config.jsに各Lambda関数URLを設定
```

```javascript
window.LAMBDA_URLS = {
    bedrock: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    db: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    s3: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    weather: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    calendar: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    full: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/'
};
```

### 5. テスト実行

```bash
# ブラウザでindex.htmlを開く
start web/index.html
```

## テスト順序（推奨）

### ステップ1: 単体テスト
1. ✅ Bedrockテスト → AI疎通確認
2. ✅ DBテスト → DBデータだけでコーデ提案
3. ✅ S3テスト → 画像→Bedrock分析→DB登録→コーデ提案
4. ✅ 天気テスト → 外部API確認
5. ✅ 予定テスト → カレンダー確認

### ステップ2: 全体統合テスト
6. ✅ フルコーディネート提案 → すべて統合

## トラブルシューティング

### Bedrockエラー
- モデルアクセスが有効か確認
- IAMロールに`bedrock:InvokeModel`権限があるか確認

### DynamoDBエラー
- テーブル名が`fureai-clothing-items`か確認
- IAMロールにDynamoDB権限があるか確認

### S3エラー
- バケット名が`fureai-clothing-images`か確認
- IAMロールにS3権限があるか確認

### CORSエラー
- Lambda関数URLのCORS設定を確認
- 認証タイプが「NONE」か確認

## 次のステップ

- [ ] 実際の服画像をS3にアップロード
- [ ] DynamoDBにユーザー設定を登録
- [ ] OpenWeatherMap APIキーを設定
- [ ] Googleカレンダー連携を設定
- [ ] 全体統合テストで実データを使用

## 参考ドキュメント

- [Lambda関数詳細](lambda/README.md)
- [Web UI設定](web/README.md)
- [アーキテクチャ設計](docs/design/architecture.md)
