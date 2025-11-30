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
| db_tester | 📐 設計のみ | DBデータでコーデ提案 |
| s3_tester | 📐 設計のみ | 画像→分析→DB→提案 |
| weather_api_fetcher | 📐 設計のみ | 天気API（モック） |
| calendar_fetcher | 📐 設計のみ | 予定API（モック） |
| full_coordinator | 📐 設計のみ | 全体統合 |

---

## 📝 やるべきこと

### 🚀 CloudShellで自動作成（推奨）

#### 1. ファイルのアップロード

CloudShellに以下のファイルをアップロード:
- `scripts/setup_lambda_env.sh`
- `iam/*.json`（全ポリシーファイル）

**アップロード方法:**
- CloudShell右上「アクション」→「ファイルのアップロード」
- または、ドラッグ&ドロップ

#### 2. 実行権限を付与

```bash
chmod +x *.sh
```

#### 3. Lambda関数を作成（6回実行）

```bash
./setup_lambda_env.sh
# 関数名を入力: fureai-bedrock-tester
# 作成しますか？ y

./setup_lambda_env.sh
# 関数名を入力: fureai-db-tester
# 作成しますか？ y

./setup_lambda_env.sh
# 関数名を入力: fureai-s3-tester
# 作成しますか？ y

./setup_lambda_env.sh
# 関数名を入力: fureai-weather-fetcher
# 作成しますか？ y

./setup_lambda_env.sh
# 関数名を入力: fureai-calendar-fetcher
# 作成しますか？ y

./setup_lambda_env.sh
# 関数名を入力: fureai-full-coordinator
# 作成しますか？ y
```

**自動で実行される処理:**
- ✅ IAMロール作成（関数名-role）
- ✅ ポリシー適用（関数名に応じて自動選択）
- ✅ Lambda関数作成（Python 3.12、タイムアウト30秒）
- ✅ 環境変数設定（BUCKET_NAME, TABLE_NAME, MODEL_ID）

#### 4. Lambda関数コードをデプロイ

AWSコンソール → Lambda → 各関数:
1. `lambda/`フォルダの対応する`.py`ファイルをコピー
2. `lambda_function.py`に貼り付け
3. 「Deploy」をクリック

#### 5. 関数URLを作成

各Lambda関数で:
- 「設定」→「関数URL」→「関数URLを作成」
- 認証タイプ: NONE
- CORS: 有効（Allow origin: `*`, Allow methods: `POST`）

#### 6. Web UIに設定

発行された関数URLを`web/config.js`に貼り付け

---

### 🔧 手動作成（AWSコンソール）

#### 1. Lambda関数の作成

各Lambda関数をAWSコンソールで作成してください。

#### 手順
1. **Lambda関数作成**
   - ランタイム: Python 3.12
   - タイムアウト: 30秒
   - メモリ: 128MB

2. **環境変数の設定** ⭐重要
   - Lambda関数 → 「設定」タブ → 「環境変数」
   - 「編集」をクリック
   - 以下の3つを追加:
   ```
   キー: BUCKET_NAME     値: fureai-clothing-images
   キー: TABLE_NAME      値: clothing_data_ptn1
   キー: MODEL_ID        値: jp.anthropic.claude-sonnet-4-5-20250929-v1:0
   ```
   - 「保存」をクリック
   - **全Lambda関数で同じ設定が必要です**

3. **コードのデプロイ**
   - `lambda/` フォルダ内の対応する `.py` ファイルをコピー
   - Lambda関数の `lambda_function.py` に貼り付け
   - 「Deploy」ボタンをクリック

4. **IAMロールの設定**
   - Lambda実行ロールに以下の権限を追加:
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

5. **関数URLの作成**
   - 認証タイプ: NONE
   - CORS: 有効
     - Allow origin: `*`
     - Allow methods: `POST`
     - Allow headers: `content-type`
     - Max age: `300`

6. **Web UIに設定**
   - 発行された関数URLを `web/config.js` に貼り付け

### 2. テスト

`web/index.html` をブラウザで開いてテストしてください。

---

## 📂 ファイル構成

```
FUREAI/
├── lambda/                    # Lambda関数
│   ├── bedrock_tester.py      # 1. Bedrock疎通テスト
│   ├── db_tester.py           # 2. DBデータでコーデ提案
│   ├── s3_tester.py           # 3. 画像→分析→DB→提案
│   ├── weather_api_fetcher.py # 4. 天気API
│   ├── calendar_fetcher.py    # 5. 予定API
│   ├── full_coordinator.py    # 6. 全体統合
│   ├── .env.example           # 環境変数の例
│   └── README.md              # Lambda関数ドキュメント
├── web/                       # Web UI
│   ├── index.html             # テストUI
│   ├── config.js.example      # Lambda URL設定例
│   └── README.md              # Web UIドキュメント
├── docs/                      # ドキュメント
├── iam/                       # IAMポリシー
├── README.md                  # このファイル
├── SECRETS_MANAGEMENT.md      # 機密情報管理
└── .gitignore                 # Git除外設定
```

---

## 📚 ドキュメント一覧

### 🔴 必須（最初に読む）
- [README.md](README.md) - このファイル
- [機密情報管理](SECRETS_MANAGEMENT.md) - config.js管理方法

### 🟡 重要（開発時に参照）
- [Lambda関数ドキュメント](lambda/README.md) - 各関数の詳細
- [Web UIドキュメント](web/README.md) - テスト方法
- [環境変数の例](lambda/.env.example) - Lambda設定

---

## 🔐 機密情報の管理

**重要**: Lambda関数URLなどの機密情報は[SECRETS_MANAGEMENT.md](SECRETS_MANAGEMENT.md)を参照してください。

- `web/config.js` - Gitにコミットしない（`.gitignore`で除外済み）
- Slackのチーム内チャンネルで共有
- 詳細: [SECRETS_MANAGEMENT.md](SECRETS_MANAGEMENT.md)

---

## 🛠️ 構築フロー

### CloudShell自動作成の場合

```
1. CloudShellでスクリプト実行（6回）
   ↓
2. Lambda関数コードをデプロイ
   ↓
3. 関数URL作成
   ↓
4. Web UI設定（web/config.js）
   ↓
5. テスト実行（web/index.html）
```

### 手動作成の場合

```
1. Lambda関数作成
   ↓
2. 環境変数設定（BUCKET_NAME, TABLE_NAME, MODEL_ID）
   ↓
3. コードデプロイ（lambda/*.py）
   ↓
4. IAMロール設定
   ↓
5. 関数URL作成
   ↓
6. Web UI設定（web/config.js）
   ↓
7. テスト実行（web/index.html）
```

---

## 💡 Lambda関数名とポリシーファイルのマッピング

| Lambda関数名 | 使用されるポリシーファイル |
|---|---|
| `fureai-bedrock-tester` | `bedrock-tester-policy.json` |
| `fureai-db-tester` | `db-tester-policy.json` |
| `fureai-s3-tester` | `s3-tester-policy.json` |
| `fureai-weather-fetcher` | `weather-fetcher-policy.json` |
| `fureai-calendar-fetcher` | `calendar-fetcher-policy.json` |
| `fureai-full-coordinator` | `full-coordinator-policy.json` |

**ポイント:** 関数名に含まれるキーワード（bedrock, db, s3など）で自動判定されます

---

## 🧪 テスト方法

1. `web/index.html` をブラウザで開く
2. 各テストボタンをクリック:
   - Bedrockテスト
   - DBテスト
   - S3テスト（画像選択必須）
   - 天気テスト
   - 予定テスト
   - 全体統合テスト

---

## ⚠️ よくあるエラー

### KeyError: 'BUCKET_NAME'
→ Lambda関数の環境変数を設定してください

### 502 Bad Gateway
→ タイムアウトを30秒に変更してください

### CORS エラー（Access-Control-Allow-Origin contains multiple values）
→ Lambda関数コードからCORSヘッダーを削除してください（修正済み）

### AccessDeniedException
→ IAM権限とBedrockモデルアクセスを確認してください

### InvalidParameterValueException: The role cannot be assumed
→ IAMロール作成直後のエラー。15秒待機後に再実行してください

### ResourceConflictException: resource is in Pending state
→ Lambda関数作成直後のエラー。10秒待機後に再実行してください

### ポリシーファイルが見つかりません
→ CloudShellで`ls -la`を実行し、JSONファイルが同じディレクトリにあるか確認してください

---

## 🔧 CloudShell便利コマンド

```bash
# 現在のディレクトリ確認
pwd

# ファイル一覧
ls -la

# すべてのファイルを削除（クリーンアップ）
rm -rf *

# 実行権限を付与
chmod +x *.sh

# JSONファイルの内容確認
cat bedrock-tester-policy.json
```

---

## 📞 サポート

質問や問題がある場合は、以下のドキュメントを参照してください：
- [機密情報管理](SECRETS_MANAGEMENT.md)
- [Lambda関数ドキュメント](lambda/README.md)
- [Web UIドキュメント](web/README.md)
- [スクリプトドキュメント](scripts/README.md)

---

## 📄 ライセンス

このプロジェクトは個人学習用です。
