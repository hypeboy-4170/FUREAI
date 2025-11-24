# FUREAI ファイル構成一覧

## 📁 ディレクトリ構成

```
FUREAI/
├── config/          # 設定ファイル
├── docs/            # ドキュメント
├── iam/             # IAMポリシー
├── lambda/          # Lambda関数コード
├── scripts/         # セットアップスクリプト
└── web/             # Webフロントエンド
```

---

## 📄 ファイル詳細

### ルートディレクトリ
| ファイル | 説明 |
|---------|------|
| `README.md` | プロジェクト概要 |
| `requirements.txt` | Python依存パッケージ |
| `.env.example` | 環境変数テンプレート |
| `.gitignore` | Git除外設定 |
| **`FILE_STRUCTURE.md`** | **このファイル（全体構成説明）** |

---

### 📂 config/ - 設定ファイル
| ファイル | 説明 | 用途 |
|---------|------|------|
| `lambda-env-vars.json` | Lambda環境変数 | Lambda関数の環境変数設定 |
| `README.md` | 設定ガイド | 設定方法の説明 |

---

### 📂 docs/ - ドキュメント

#### 📂 docs/design/ - 設計書
| ファイル | 説明 | 対象者 |
|---------|------|--------|
| `architecture.md` | システム全体アーキテクチャ | 全員 |
| `data-model.md` | データモデル設計 | 開発者 |
| `lambda-design.md` | Lambda関数設計 | 開発者 |
| `dynamodb-design.md` | DynamoDB設計 | 開発者 |
| `s3-design.md` | S3設計 | 開発者 |
| `bedrock-design.md` | Bedrock設計 | 開発者 |

#### 📂 docs/procedures/ - 手順書
| ファイル | 説明 | 難易度 |
|---------|------|--------|
| `quickstart.md` | CloudShellクイックスタート | ⭐ 初心者 |
| `console-setup.md` | コンソールのみでの構築 | ⭐ 初心者 |
| `dynamodb-setup.md` | DynamoDB構築手順 | ⭐⭐ 中級 |
| `s3-setup.md` | S3構築手順 | ⭐⭐ 中級 |
| `lambda-setup.md` | Lambda構築手順 | ⭐⭐⭐ 上級 |
| `bedrock-setup.md` | Bedrock設定手順 | ⭐⭐ 中級 |
| `verification.md` | 動作確認手順 | ⭐ 初心者 |

#### 📂 docs/その他
| ファイル | 説明 | 対象者 |
|---------|------|--------|
| `architecture.mmd` | アーキテクチャ図（Mermaid） | 設計者 |
| `architecture.html` | アーキテクチャ図（HTML） | 設計者 |
| `image-handling.md` | 画像処理仕様 | 開発者 |
| `image-upload-workflow.md` | 画像アップロードフロー | 開発者 |
| `image-usage-concept.md` | 画像利用コンセプト | 企画者 |
| `test-scenarios.md` | テストシナリオ | QA |

---

### 📂 iam/ - IAMポリシー
| ファイル | 説明 | 用途 |
|---------|------|------|
| `lambda-execution-policy.json` | Lambda実行ポリシー | Lambda IAMロール設定 |

---

### 📂 lambda/ - Lambda関数
| ファイル | 説明 | 機能 |
|---------|------|------|
| `coordinate_recommender.py` | コーディネート推薦Lambda | AI提案のメイン処理 |
| `external_api_fetcher.py` | 外部API取得Lambda | 天気API連携（将来用） |
| `README.md` | Lambda説明 | 関数の使い方 |

---

### 📂 scripts/ - セットアップスクリプト
| ファイル | 説明 | 実行タイミング |
|---------|------|--------------|
| `setup_all.sh` | 一括セットアップ | 初回構築時 |
| `verify_image_registration.sh` | 画像登録確認 | 画像登録後 |
| `README.md` | スクリプト説明 | - |

---

### 📂 web/ - Webフロントエンド
| ファイル | 説明 | 用途 |
|---------|------|------|
| `index.html` | Webアプリ | ユーザーインターフェース |

---

## 🚀 クイックスタート

### 1. 初めての方（構築）
1. `docs/procedures/quickstart.md` を読む
2. `scripts/setup_all.sh` を実行
3. `web/index.html` をブラウザで開く

### 2. 設計を理解したい方
1. `docs/design/architecture.md` - 全体像
2. `docs/design/data-model.md` - データ構造
3. `docs/design/lambda-design.md` - Lambda設計

### 3. Lambda開発者
1. `docs/procedures/lambda-setup.md` を読む
2. `lambda/coordinate_recommender.py` を編集
3. `config/lambda-env-vars.json` で環境変数設定

---

## 📌 重要ファイル優先度

### 🔴 必須（最初に読む）
- `README.md` - プロジェクト概要
- `docs/procedures/quickstart.md` - 構築手順
- `docs/design/architecture.md` - システム全体像

### 🟡 重要（開発時に参照）
- `docs/design/data-model.md` - データ構造
- `docs/design/lambda-design.md` - Lambda設計
- `lambda/coordinate_recommender.py` - メインロジック

### 🟢 参考（必要に応じて）
- `docs/procedures/` - 各種構築手順
- `docs/design/` - 各サービス詳細設計
- `docs/test-scenarios.md` - テスト方法
