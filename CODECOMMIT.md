# CodeCommit へのコミット方法

## 🚀 初回セットアップ

### 1. CodeCommit リポジトリ作成

AWS コンソールで:
```
CodeCommit → リポジトリを作成
リポジトリ名: FUREAI
説明: Alexa音声コーデ提案システム
```

### 2. Git 認証情報設定

#### 方法A: HTTPS (推奨)
```bash
# IAM ユーザーの Git 認証情報を生成
AWS Console → IAM → ユーザー → 認証情報 → HTTPS Git 認証情報
```

#### 方法B: SSH
```bash
# SSH キー生成
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 公開鍵を IAM に登録
AWS Console → IAM → ユーザー → 認証情報 → SSH キー
```

### 3. Git 初期化

```bash
cd C:\Software\Workspace\FUREAI

# Git 初期化
git init

# CodeCommit リポジトリを追加
git remote add origin https://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/FUREAI

# または SSH の場合
git remote add origin ssh://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/FUREAI
```

## 📝 コミット手順

### 1. 変更をステージング

```bash
# 全ファイルを追加
git add .

# または特定のファイルのみ
git add lambda/ tests/ setup/
```

### 2. コミット

```bash
git commit -m "Initial commit: Alexa outfit recommendation system"
```

### 3. プッシュ

```bash
# 初回プッシュ
git push -u origin main

# 2回目以降
git push
```

## 🔄 日常的な作業フロー

```bash
# 1. 変更を確認
git status

# 2. 差分を確認
git diff

# 3. ステージング
git add .

# 4. コミット
git commit -m "Add: Bedrock integration"

# 5. プッシュ
git push
```

## 📋 コミットメッセージ規約

```
Add: 新機能追加
Fix: バグ修正
Update: 既存機能の更新
Refactor: リファクタリング
Docs: ドキュメント更新
Test: テスト追加・修正
```

例:
```bash
git commit -m "Add: Alexa mock simulator"
git commit -m "Fix: Weather API error handling"
git commit -m "Update: RDS table schema"
```

## 🌿 ブランチ戦略

```bash
# 開発ブランチ作成
git checkout -b develop

# 機能ブランチ作成
git checkout -b feature/alexa-integration

# マージ
git checkout main
git merge feature/alexa-integration

# プッシュ
git push origin main
```

## 🔍 便利なコマンド

```bash
# ログ確認
git log --oneline

# リモート確認
git remote -v

# ブランチ一覧
git branch -a

# 最新を取得
git pull

# 変更を取り消し
git checkout -- filename
```

## ⚠️ .gitignore 設定

以下のファイルは除外:
```
.env
*.pyc
__pycache__/
.vscode/
*.log
```

## 🎯 初回コミット例

```bash
cd C:\Software\Workspace\FUREAI

# Git 初期化
git init
git remote add origin https://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/FUREAI

# .gitignore 作成
echo .env > .gitignore
echo __pycache__/ >> .gitignore

# 全ファイルをコミット
git add .
git commit -m "Initial commit: FUREAI Alexa outfit recommendation system

- Add: Architecture documentation
- Add: Mock tests (Alexa, Weather API, Bedrock)
- Add: RDS table schemas
- Add: Sample data
- Add: Requirements and README"

# プッシュ
git push -u origin main
```

## 💡 トラブルシューティング

### 認証エラー
```bash
# 認証情報を再設定
git config --global credential.helper store
```

### プッシュエラー
```bash
# 最新を取得してからプッシュ
git pull --rebase origin main
git push
```

### リモートURL変更
```bash
git remote set-url origin https://new-url
```
