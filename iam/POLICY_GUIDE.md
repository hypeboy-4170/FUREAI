# Lambda関数別IAMポリシー一覧

## 各関数に必要な権限

### 1. bedrock_tester
- **ファイル**: `bedrock-tester-policy.json`
- **権限**: Bedrock実行のみ
- **用途**: Bedrock疎通確認

### 2. db_tester
- **ファイル**: `db-tester-policy.json`
- **権限**: DynamoDB読み取り + Bedrock実行
- **用途**: DBデータでコーデ提案

### 3. s3_tester
- **ファイル**: `s3-tester-policy.json`
- **権限**: S3読み書き + Bedrock実行 + DynamoDB書き込み
- **用途**: 画像アップロード→分析→DB登録

### 4. weather_api_fetcher
- **ファイル**: `weather-fetcher-policy.json`
- **権限**: CloudWatch Logsのみ
- **用途**: 外部天気API呼び出し

### 5. calendar_fetcher
- **ファイル**: `calendar-fetcher-policy.json`
- **権限**: CloudWatch Logsのみ
- **用途**: 外部カレンダーAPI呼び出し

### 6. coordinate_recommender
- **ファイル**: `coordinate-recommender-policy.json`
- **権限**: DynamoDB読み取り + Bedrock実行
- **用途**: コーディネート提案（メイン機能）

### 7. full_coordinator
- **ファイル**: `full-coordinator-policy.json`
- **権限**: S3読み取り + DynamoDB読み取り + Bedrock実行
- **用途**: 全体統合テスト

## 設定方法

### AWSコンソール
1. IAM → ロール → Lambda実行ロールを選択
2. 「ポリシーをアタッチ」→「インラインポリシーの作成」
3. JSONタブで該当ポリシーをコピペ
4. ロールにアタッチ

## 共通権限

全ての関数に以下が含まれています：
- CloudWatch Logs書き込み（ログ出力用）
