# Googleカレンダー連携セットアップ

## 1. Google Cloud Consoleでプロジェクト作成

1. https://console.cloud.google.com/ にアクセス
2. 新しいプロジェクト作成: `FUREAI`

## 2. Calendar API有効化

1. APIとサービス > ライブラリ
2. "Google Calendar API" を検索
3. 有効にする

## 3. OAuth 2.0認証情報作成

1. APIとサービス > 認証情報
2. 認証情報を作成 > OAuth クライアントID
3. アプリケーションの種類: Webアプリケーション
4. 承認済みのリダイレクトURI: `http://localhost:8080/callback`
5. クライアントIDとシークレットをダウンロード

## 4. トークン取得スクリプト実行

```bash
python scripts/get_calendar_token.py
```

ブラウザが開くのでGoogleアカウントでログイン → トークンが生成される

## 5. Lambda環境変数設定

```
GOOGLE_CALENDAR_TOKEN=ya29.a0AfH6SMB...
```

## 注意事項

- トークンは1時間で期限切れ（リフレッシュトークンで更新可能）
- 本番環境ではリフレッシュトークンを使用
- セキュリティのためトークンは暗号化推奨
