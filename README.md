# FUREAI - AIコーディネート提案システム

## 📋 プロジェクト概要

FUREAIは、AWS Lambda + Bedrock + DynamoDBを使用したAIコーディネート提案システムです。
ユーザーの予定や天気に合わせて、最適な服装を提案します。

---

## 🚀 クイックスタート

### 前提条件
- AWSアカウント
- Bedrockモデルアクセス有効化（Claude Sonnet 4.5）
- Lambda関数作成権限

### 実装状況

| Lambda関数 | 状態 | 説明 |
|-----------|------|------|
| bedrock_tester | ✅ 実装済み | Bedrock疎通テスト |
| db_tester | 📝 設計済み | DB疎通テスト |
| s3_tester | 📝 設計済み | S3疎通テスト |
| weather_api_fetcher | 📝 設計済み | 天気API疎通テスト |
| calendar_fetcher | 📝 設計済み | 予定API疎通テスト |
| coordinate_recommender | 📝 設計済み | コーディネート提案 |
| full_coordinator | 📝 設計済み | 全体統合テスト |

---

## 📝 やるべきこと

### 1. Lambda関数の作成

各Lambda関数をAWSコンソールで作成してください。

#### 手順
1. **Lambda関数作成**
   - `docs/design/LAMBDA_SETUP.md` を参照
   - 関数名は `docs/design/architecture.md` を参照
   - タイムアウト: 30秒
   - メモリ: 128MB
   - ランタイム: Python 3.12

2. **コードのデプロイ**
   - `lambda/` フォルダ内の対応する `.py` ファイルをコピー
   - Lambda関数の `lambda_function.py` に貼り付け
   - 「Deploy」ボタンをクリック

3. **IAMロールの設定**
   - `iam/` フォルダ内の対応する `-policy.json` を参照
   - Lambda実行ロールにポリシーをアタッチ

4. **関数URLの作成**
   - 認証タイプ: NONE
   - CORS: 有効
     - Allow origin: `*`
     - Allow methods: `POST`
     - Allow headers: `content-type`
     - Max age: `300`

5. **Web UIに設定**
   - 発行された関数URLを `web/config.js` に貼り付け

### 2. コーディング

未実装の関数を実装してください。

#### 参考ドキュメント
- **実装チェックリスト**: `docs/LAMBDA_IMPLEMENTATION_CHECKLIST.md`
  - 各関数で実装すべき項目
  - 必要なimport
  - 処理フロー
  - 実装例

- **設計書**: `docs/design/lambda-design.md`
  - ステータスコード設計
  - 入出力仕様
  - エラーハンドリング

#### 実装優先順位
1. ✅ `bedrock_tester` - 実装済み
2. 📝 `db_tester` - DynamoDB + Bedrock（次に実装推奨）
3. 📝 `weather_api_fetcher` - モック実装で簡単
4. 📝 `calendar_fetcher` - モック実装で簡単
5. 📝 `coordinate_recommender` - メイン機能
6. 📝 `s3_tester` - 複雑（画像処理）
7. 📝 `full_coordinator` - 最も複雑（全統合）

### 3. テスト

`web/index.html` をブラウザで開いてテストしてください。

#### テスト手順
- **テストガイド**: `web/TESTING_GUIDE.md`
  - 各テストの実行方法
  - 期待結果
  - トラブルシューティング

---

## 📂 ファイル構成

詳細は `FILE_STRUCTURE.md` を参照してください。

```
FUREAI/
├── lambda/          # Lambda関数コード（.py）
├── iam/             # IAMポリシー（.json）
├── docs/            # ドキュメント
│   ├── design/      # 設計書
│   │   ├── architecture.md
│   │   ├── lambda-design.md
│   │   └── LAMBDA_SETUP.md
│   └── LAMBDA_IMPLEMENTATION_CHECKLIST.md
└── web/             # Web UI
    ├── index.html
    ├── config.js
    └── TESTING_GUIDE.md
```

---

## 📚 ドキュメント一覧

### 🔴 必須（最初に読む）
- `README.md` - このファイル
- `docs/design/architecture.md` - システム全体像
- `docs/design/LAMBDA_SETUP.md` - Lambda関数作成手順

### 🟡 重要（開発時に参照）
- `docs/LAMBDA_IMPLEMENTATION_CHECKLIST.md` - 実装チェックリスト
- `docs/design/lambda-design.md` - Lambda設計
- `iam/POLICY_GUIDE.md` - IAM権限ガイド

### 🟢 参考（必要に応じて）
- `web/TESTING_GUIDE.md` - Web UIテスト手順
- `FILE_STRUCTURE.md` - ファイル構成説明

---

## 🛠️ 構築フロー

```
1. Lambda関数作成
   ↓
2. コードデプロイ（lambda/*.py）
   ↓
3. IAMロール設定（iam/*-policy.json）
   ↓
4. 関数URL作成
   ↓
5. Web UI設定（web/config.js）
   ↓
6. テスト実行（web/index.html）
```

---

## 💡 Tips

### Lambda関数名の例
- `fureai-bedrock-tester`
- `fureai-db-tester`
- `fureai-s3-tester`
- `fureai-weather-fetcher`
- `fureai-calendar-fetcher`
- `fureai-coordinate-recommender`
- `fureai-full-coordinator`

### よくあるエラー

#### 502 Bad Gateway
- タイムアウトが3秒（デフォルト）のまま → 30秒に変更
- CloudWatch Logsでエラー詳細を確認

#### CORS エラー
- 関数URLのCORS設定を確認
- Allow headers に `content-type` を追加

#### AccessDeniedException
- IAM権限を確認
- Bedrockモデルアクセスを有効化

---

## 📞 サポート

質問や問題がある場合は、以下のドキュメントを参照してください：
- `docs/design/LAMBDA_SETUP.md` - トラブルシューティング
- `web/TESTING_GUIDE.md` - デバッグ方法

---

## 📄 ライセンス

このプロジェクトは個人学習用です。
