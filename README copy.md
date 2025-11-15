# FUREAI - Alexa音声コーデ提案システム

Alexaに「服ちょうだい」と話しかけると、天気・予定・着用履歴を考慮したコーディネートをAIが提案するシステム。

## 🎯 システム構成

- **音声UI**: Amazon Alexa
- **バックエンド**: AWS Lambda (Python)
- **AI**: Amazon Bedrock (Claude 3.5)
- **DB**: Amazon RDS (PostgreSQL)
- **ストレージ**: Amazon S3
- **外部API**: 天気・予定情報

## 📋 必要なもの

- Python 3.11+
- AWS アカウント
- Alexa Developer アカウント
- 天気API キー (OpenWeatherMap)

## 🚀 クイックスタート

### 1. 環境構築

```bash
pip install -r requirements.txt
```

### 2. テスト実行

各テストファイルはモック用と本番用の両方に対応しています。

```bash
# 1. 音声インターフェース（Alexa）テスト
python tests/test_01_voice_interface.py

# 2. 天気APIテスト
python tests/test_02_weather_api.py

# 3. Bedrock AIテスト
python tests/test_03_bedrock_ai.py

# 4. Lambda関数テスト
python tests/test_04_lambda_function.py

# 5. システム統合テスト
python tests/test_05_system_integration.py
```

### 3. RDSセットアップ

```bash
# テーブル作成
psql -h your-rds-endpoint -U postgres -f setup/create_tables.sql

# サンプルデータ投入
psql -h your-rds-endpoint -U postgres -f setup/sample_data.sql
```

## 💻 開発フェーズ

### Phase 1: モック開発（現在）
テキスト入力で各コンポーネントを個別にテスト

### Phase 2: Lambda統合
全コンポーネントをLambdaで統合

### Phase 3: Alexa連携
音声入出力の実装

## 📁 ファイル構成

```
FUREAI/
├── lambda/                          # Lambda関数
├── tests/                           # テストファイル
│   ├── test_01_voice_interface.py   # Alexaスキルテスト（モック/本番）
│   ├── test_02_weather_api.py       # 天気APIテスト（モック/本番）
│   ├── test_03_bedrock_ai.py        # Bedrock AIテスト（モック/本番）
│   ├── test_04_lambda_function.py   # Lambda関数テスト（モック/本番）
│   └── test_05_system_integration.py # システム統合テスト（モック/本番）
├── setup/                           # セットアップスクリプト
└── requirements.txt
```

## 🔍 テスト方法

各テストファイルを実行すると、モードを選択できます：
- **1. モックテスト**: ローカル環境で固定データを使用
- **2. 本番テスト**: 実際のAWSサービスを使用

### 例: 音声インターフェーステスト
```bash
python tests/test_01_voice_interface.py
# 選択 (1/2): 1  ← モックテスト
# 選択 (1/2): 2  ← 本番テスト（Alexa連携）
```

### 推奨テスト順序
1. `test_01_voice_interface.py` - Alexaスキル動作確認
2. `test_02_weather_api.py` - 天気API接続確認
3. `test_03_bedrock_ai.py` - AI提案機能確認
4. `test_04_lambda_function.py` - Lambda統合確認
5. `test_05_system_integration.py` - 全体統合確認

## 📚 ドキュメント

- [ARCHITECTURE.md](ARCHITECTURE.md) - システム設計詳細

## ⚠️ 注意事項

- RDSは本番環境のみ使用（開発中はモックデータ）
- Bedrock利用にはAWS申請が必要
- 天気APIは無料枠あり

## 🎯 今後の拡張

- 画像認識による服の自動登録
- 洗濯状況の管理
- コーデ評価フィードバック
