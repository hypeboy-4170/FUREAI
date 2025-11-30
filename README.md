# FUREAI - AIコーディネート提案システム

AIがあなたの予定と天気に合わせて、最適なコーディネートを提案するシステムです。

## 🎯 主な機能

### 単体テスト
1. **Bedrockテスト** - Claude Sonnet 4.5疎通確認
2. **DBテスト** - DBデータだけでコーデ提案
3. **S3テスト** - 画像→Bedrock分析→DB登録→コーデ提案
4. **天気テスト** - OpenWeatherMap API疎通確認
5. **予定テスト** - Googleカレンダー疎通確認

### 全体統合テスト
6. **フルコーディネート提案** - S3 + DB + 天気 + 予定 → Bedrock → HTML表示

## 📁 プロジェクト構成

```
FUREAI/
├── lambda/                    # Lambda関数
│   ├── bedrock_tester.py      # 1. Bedrock疎通テスト
│   ├── db_tester.py           # 2. DynamoDB疎通テスト
│   ├── s3_tester.py           # 3. S3疎通テスト
│   ├── weather_api_fetcher.py # 4. 天気API疎通テスト
│   ├── calendar_fetcher.py    # 5. 予定API疎通テスト
│   └── full_coordinator.py    # 6. 全体統合（メイン）
├── web/                       # Webインターフェース
│   ├── index.html             # テストUI
│   └── config.js.example      # 設定サンプル
├── docs/                      # ドキュメント
└── iam/                       # IAMポリシー
```

## 🚀 セットアップ

### 1. Lambda関数のデプロイ

各Lambda関数を作成し、以下の設定を行います:

#### 共通設定
- ランタイム: Python 3.12
- タイムアウト: 30秒
- 関数URL: 有効化 (認証: NONE, CORS有効)

#### 必要なIAMポリシー
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

### 2. Bedrockモデルアクセスの有効化

1. Amazon Bedrockコンソール (ap-northeast-1)
2. Model access → Manage model access
3. 以下のモデルを有効化:
   - Claude Sonnet 4.5
   - Claude 3.5 Sonnet v2
   - Claude 3.5 Sonnet v1

### 3. Web UIの設定

1. `web/config.js.example` を `web/config.js` にコピー
2. 各Lambda関数URLを設定:
```javascript
window.LAMBDA_URLS = {
    bedrock: 'https://...',
    db: 'https://...',
    s3: 'https://...',
    weather: 'https://...',
    calendar: 'https://...',
    full: 'https://...'  // 全体統合
};
```
3. `web/index.html` をブラウザで開く

## 🧪 テスト方法

### 単体テスト（個別機能確認）
1. `web/index.html` を開く
2. 各テストボタンをクリック:
   - Bedrockテスト
   - DBテスト
   - S3テスト
   - 天気テスト
   - 予定テスト

### 全体統合テスト
1. ユーザーIDと場所を入力
2. 「🚀 全体テスト実行」ボタンをクリック
3. S3 → DB → 天気 → 予定 → Bedrock の順に実行
4. AIのコーディネート提案が表示される

## 🔧 使用技術

- **AWS Lambda** - サーバーレス実行環境
- **Amazon Bedrock** - Claude Sonnet 4.5 AI
- **Python 3.12** - Lambda関数
- **HTML/JavaScript** - Webインターフェース

## 📝 モデル情報

- **使用モデル**: JP Anthropic Claude Sonnet 4.5
- **モデルID**: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`
- **リージョン**: ap-northeast-1 (東京)
- **推論タイプ**: INFERENCE_PROFILE

## 🔗 関連ドキュメント

- [Web UI設定手順](web/README.md)
- [Lambda関数詳細](lambda/README.md)
- [アーキテクチャ設計](docs/design/architecture.md)

## 📄 ライセンス

このプロジェクトは個人学習用です。
