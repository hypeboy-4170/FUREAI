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
       ├─→ 📦 RDS (服データ・履歴)
       ├─→ 🖼️ S3 (服の写真)
       ├─→ 🌤️ 外部API (天気・予定)
       └─→ 🤖 Bedrock (AIエージェント + ナレッジベース)
              │
              └─→ コーディネート提案
```

## 📊 データフロー

```
1. ユーザー → Alexa
   「服ちょうだい」

2. Alexa → Lambda
   {
     "intent": "GetOutfit",
     "userId": "user123"
   }

3. Lambda → 各サービス
   ├─ RDS: 服データ・着用履歴取得
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
   「今日は白いシャツとグレーのパンツがおすすめです」
```

## 🗄️ データベース設計 (RDS)

### テーブル: clothes (洋服一覧)

```sql
CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    s3_key VARCHAR(200) NOT NULL,     -- S3写真パス
    category VARCHAR(50),              -- tops/bottoms/outer/shoes
    color VARCHAR(50),                 -- white/black/navy等
    tags VARCHAR(200),                 -- formal/casual/summer等
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**設計方針**:
- S3写真 + メタデータ（カテゴリ・色・タグ）でAIが判断しやすく
- 画像分析コスト削減のため事前分類
- 履歴テーブルは不要（将来必要なら追加）

## 📁 ファイル構成

```
FUREAI/
├── lambda/
│   ├── handler.py              # Lambda メインハンドラー
│   ├── bedrock_client.py       # Bedrock AI 通信
│   ├── rds_client.py           # RDS データ取得
│   ├── s3_client.py            # S3 画像URL取得
│   └── external_api.py         # 天気・予定API
├── tests/
│   ├── test_alexa_mock.py      # Alexaモック（テキスト入力）
│   ├── test_weather_api.py     # 天気API確認
│   ├── test_bedrock.py         # Bedrock動作確認
│   └── test_integration.py     # 統合テスト
├── setup/
│   ├── create_tables.sql       # RDS テーブル作成
│   ├── sample_data.sql         # サンプルデータ
│   └── deploy_lambda.sh        # Lambda デプロイ
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

## 🔧 技術スタック

| レイヤー | 技術 |
|---------|------|
| 音声UI | Amazon Alexa |
| バックエンド | AWS Lambda (Python 3.11) |
| AI | Amazon Bedrock (Claude 3.5) |
| データベース | Amazon RDS (PostgreSQL) |
| ストレージ | Amazon S3 |
| 外部API | OpenWeatherMap, Google Calendar |
| フレームワーク | boto3, psycopg2 |

## 🚀 開発フェーズ

### Phase 1: モック開発（現在）

- ✅ テキスト入力でAlexaスキルをシミュレート
- ✅ 天気APIの動作確認
- ✅ Bedrock AIの応答確認
- ✅ RDSデータ取得確認

### Phase 2: Lambda統合

- Lambda関数の実装
- RDS/S3との接続
- Bedrock統合

### Phase 3: Alexa連携

- Alexaスキルの作成
- 音声入出力の実装

### Phase 4: 本番運用

- エラーハンドリング
- ログ・監視
- パフォーマンス最適化

## 📝 実装優先順位

1. **RDSデータ取得** → `rds_client.py`
2. **Bedrock AI連携** → `bedrock_client.py`
3. **天気API連携** → `external_api.py`
4. **Lambda統合** → `handler.py`
5. **Alexaスキル** → Alexa Developer Console

## 🎯 次のステップ

1. RDSテーブル作成
2. サンプルデータ投入
3. Bedrockクライアント実装
4. 統合テスト実行
