# FUREAI ファイル構成一覧

## 📁 ディレクトリ構成

```
FUREAI/
├── docs/            # ドキュメント
├── iam/             # IAMポリシー
├── lambda/          # Lambda関数コード
└── web/             # Webフロントエンド
```

---

## 📄 ファイル詳細

### ルートディレクトリ
| ファイル | 説明 |
|---------|------|
| `README.md` | プロジェクト概要 |
| **`FILE_STRUCTURE.md`** | **このファイル（全体構成説明）** |

---

### 📂 docs/design/
| ファイル | 説明 |
|---------|------|
| `architecture.md` | システム全体アーキテクチャ |
| `lambda-design.md` | Lambda関数設計 |
| **`LAMBDA_SETUP.md`** | **Lambda関数作成手順** |

---

### 📂 iam/ - IAMポリシー
| ファイル | 説明 | 用途 |
|---------|------|------|
| `bedrock-tester-policy.json` | Bedrock疎通テスト用 | bedrock_tester Lambda |
| `db-tester-policy.json` | DB疎通テスト用 | db_tester Lambda |
| `s3-tester-policy.json` | S3疎通テスト用 | s3_tester Lambda |
| `weather-fetcher-policy.json` | 天気API用 | weather_api_fetcher Lambda |
| `calendar-fetcher-policy.json` | カレンダーAPI用 | calendar_fetcher Lambda |
| `coordinate-recommender-policy.json` | コーデ提案用 | coordinate_recommender Lambda |
| `full-coordinator-policy.json` | 全体統合用 | full_coordinator Lambda |
| **`POLICY_GUIDE.md`** | **IAMポリシーガイド** | **全Lambda関数の権限説明** |

---

### 📂 lambda/ - Lambda関数
| ファイル | 説明 | 状態 |
|---------|------|------|
| `bedrock_tester.py` | Bedrock疎通テスト | ✅ 実装済み |
| `db_tester.py` | DB疎通テスト | 📝 設計のみ |
| `s3_tester.py` | S3疎通テスト | 📝 設計のみ |
| `weather_api_fetcher.py` | 天気API疎通テスト | 📝 設計のみ |
| `calendar_fetcher.py` | 予定API疎通テスト | 📝 設計のみ |
| `coordinate_recommender.py` | コーディネート提案 | 📝 設計のみ |
| `full_coordinator.py` | 全体統合テスト | 📝 設計のみ |
| `README.md` | Lambda説明 | - |

---

### 📂 web/ - Webフロントエンド
| ファイル | 説明 | 用途 |
|---------|------|------|
| `index.html` | Webアプリ | ユーザーインターフェース |
| `config.js` | Lambda関数URL設定 | 関数URLを設定 |
| **`TESTING_GUIDE.md`** | **Web UIテスト手順** | **テスト方法説明** |

---

## 🚀 クイックスタート

### 1. Lambda関数作成
1. `docs/design/LAMBDA_SETUP.md` を読む
2. Lambda関数を作成
3. `lambda/bedrock_tester.py` をデプロイ

### 2. Web UIテスト
1. `web/config.js` にLambda関数URLを設定
2. `web/index.html` をブラウザで開く
3. `web/TESTING_GUIDE.md` を参照してテスト

### 3. 設計を理解したい方
1. `docs/design/architecture.md` - 全体像
2. `docs/design/lambda-design.md` - Lambda設計
3. `iam/POLICY_GUIDE.md` - IAM権限

---

## 📌 重要ファイル優先度

### 🔴 必須（最初に読む）
- `README.md` - プロジェクト概要
- `docs/design/architecture.md` - システム全体像
- `docs/design/LAMBDA_SETUP.md` - Lambda関数作成手順

### 🟡 重要（開発時に参照）
- `docs/design/lambda-design.md` - Lambda設計
- `iam/POLICY_GUIDE.md` - IAM権限ガイド
- `lambda/bedrock_tester.py` - 実装例

### 🟢 参考（必要に応じて）
- `web/TESTING_GUIDE.md` - Web UIテスト手順
- `web/config.js` - Lambda関数URL設定
