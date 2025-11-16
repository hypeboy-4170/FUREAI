# FUREAI アーキテクチャ設計書

## 📋 システム概要

音声でAlexaに「服ちょうだい」と話しかけると、天気・予定・着用履歴を考慮したコーディネートをAIが提案するシステム。

## 🏗️ システムアーキテクチャ

```
┌─────────────┐
│   ユーザー   │ 「服ちょうだい」
└──────┬──────┘
       │ 音声
       ↓
┌─────────────┐
│    Alexa    │ 音声認識
└──────┬──────┘
       │ Alexa Skills Kit
       ↓
┌─────────────┐
│   Lambda    │ メイン処理
└──────┬──────┘
       │
       ├─→ 📦 DynamoDB (服データ・履歴)
       ├─→ 🖼️ S3 (服の写真)
       ├─→ 🌤️ 外部API (天気・予定)
       └─→ 🤖 Bedrock (AIエージェント + ナレッジベース)
              │
              └─→ コーディネート提案
```

## 📊 データフロー

```
1. ユーザー → Alexa
   「きょうのこーでえらんで」

2. Alexa → Lambda
   {
     "intent": "GetOutfit",
     "userId": "user123"
   }

3. Lambda → 各サービス
   ├─ DynamoDB: 服データ・着用履歴取得
   ├─ S3: 服の写真URL取得
   └─ 外部API: 天気・予定取得

4. Lambda → Bedrock
   {
     "weather": "晴れ 26度",
     "schedule": "午後に会議",
     "clothes": [...],
     "history": [...]
   }

5. Bedrock → Lambda
   {
     "items": ["shirt_white", "pants_gray"],
     "explanation": "晴れで会議があるため..."
   }

6. Lambda → Alexa → ユーザー
```

## 🗄️ データベース設計 (DynamoDB)

### テーブル: clothes

```json
{
  "userId": "user123",
  "clothesId": "shirt_001",
  "s3Key": "users/user123/shirt_001.jpg",
  "category": "tops",
  "color": "white",
  "tags": ["formal", "summer"],
  "createdAt": "2025-01-10T12:00:00Z"
}
```

**キー設計**:

- Partition Key: `userId`
- Sort Key: `clothesId`

**設計方針**:

- サーバーレスでLambda連携に最適
- S3写真 + メタデータでAI判断しやすく
- 自動スケール・低レイテンシ

## 📁 ファイル構成

```
FUREAI/
├── lambda/
│   ├── hello_world.py                 # Alexa疎通確認用Lambda関数
│   └── README.md
├── docs/
│   ├── architecture.mmd               # Mermaidアーキテクチャ図
│   └── architecture.html              # アーキテクチャ図表示用
├── .env                               # 環境変数
├── .gitignore
├── requirements.txt                   # Python依存関係
├── README.md
├── ARCHITECTURE.md                    # 本設計書
├── DEPLOYMENT.md                      # デプロイ手順
├── TESTING.md                         # テスト手順
└── SETUP.md                           # 開発環境セットアップ
```

## 🔧 技術スタック

| レイヤー | 技術 |
|---------|------|
| 音声UI | Amazon Alexa |
| バックエンド | AWS Lambda (Python 3.14) |
| AI | Amazon Bedrock (Claude 3.5) |
| データベース | Amazon DynamoDB |
| ストレージ | Amazon S3 |
| 外部API | OpenWeatherMap (無料), Google Calendar (無料) |
| フレームワーク | boto3 |

## 🚀 開発フェーズ

### Phase 1: 基本環境構築（完了）

- ✅ Lambda関数作成（hello_world.py）
- ✅ Alexaスキル作成
- ✅ Alexa⇒Lambda疎通確認
- ✅ 環境変数設定（.env）
- ✅ ドキュメント整備

### Phase 2: データ連携（次）

- DynamoDBテーブル作成
- S3バケット作成
- サンプルデータ投入
- LambdaからDynamoDB/S3接続

### Phase 3: AI連携

- Bedrockクライアント実装
- 外部API連携（天気・Google Calendar）
- コーデ提案ロジック実装

### Phase 4: 本番運用

- エラーハンドリング
- CloudWatchログ監視
- パフォーマンス最適化

## 📝 実装優先順位

1. **DynamoDBテーブル作成** → AWS Console
2. **S3バケット作成** → AWS Console
3. **DynamoDBデータ取得** → `dynamodb_client.py`
4. **Bedrock AI連携** → `bedrock_client.py`
5. **天気API連携** → `weather_api.py`
6. **Lambda統合** → `handler.py`

## 🚢 デプロイ構成

**現状**: 手動デプロイ（AWS Console）

- Lambda: ConsoleからZIPアップロード
- Alexa: Developer Consoleで設定
- 注意: 組織のSCPでCLI/SDKからの操作が制限

詳細は [DEPLOYMENT.md](DEPLOYMENT.md) を参照。

## ✅ 現在の状態

- Lambda関数: デプロイ済み
- Alexaスキル: 設定済み
- 呼び出し名: `コーディネート`
- インテント: `GetOutfitIntent`
- 使用例: 「コーディネート で えらん で」

## 🎯 次のステップ

1. DynamoDBテーブル作成 (AWS Console)
2. S3バケット作成 (AWS Console)
3. サンプルデータ投入
4. Lambda関数実装開始
