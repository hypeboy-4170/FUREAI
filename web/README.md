# Web UI設定手順

## 概要

FUREAIのテストUIです。単体テストと全体統合テストを実行できます。

## セットアップ

### 1. config.jsの作成

```bash
cp config.js.example config.js
```

### 2. Lambda関数URLの設定

`config.js`を編集して、各Lambda関数のURLを設定します:

```javascript
window.LAMBDA_URLS = {
    // 単体テスト用
    bedrock: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    db: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    s3: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    weather: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    calendar: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    
    // 全体統合テスト用
    full: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/'
};
```

### 3. ブラウザで開く

```bash
# Windowsの場合
start index.html

# macOS/Linuxの場合
open index.html
```

## テスト項目

### 🧪 単体テスト

各AWS機能を個別にテストします:

1. **Bedrockテスト** - AI疎通確認
2. **DBテスト** - DynamoDB読み書き
3. **S3テスト** - S3読み書き
4. **天気テスト** - OpenWeatherMap API
5. **予定テスト** - Googleカレンダー

### 🎯 全体統合テスト

すべての機能を統合してテストします:

1. S3から服データ取得
2. DynamoDBからユーザー設定取得
3. 天気API呼び出し
4. 予定API呼び出し
5. 全データをBedrockに投げる
6. AIの提案をHTML表示

## トラブルシューティング

### config.jsが読み込めない

- `config.js.example`を`config.js`にコピーしたか確認
- Lambda関数URLが正しく設定されているか確認

### CORSエラーが出る

Lambda関数の設定で以下を確認:
- 関数URLが有効化されている
- CORS設定が有効
- 認証タイプが「NONE」

### タイムアウトエラー

Lambda関数のタイムアウトを30秒以上に設定してください。

## ファイル構成

```
web/
├── index.html          # メインUI
├── config.js.example   # 設定サンプル
├── config.js           # 実際の設定（gitignore）
└── README.md           # このファイル
```
