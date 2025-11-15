# Lambda関数デプロイ手順

## 1. パッケージ作成

```bash
cd lambda
pip install -r requirements.txt -t .
zip -r function.zip .
```

## 2. Lambda関数作成（AWS Console）

1. Lambda > 関数の作成
2. 関数名: `fureai-outfit-handler`
3. ランタイム: Python 3.11
4. function.zipをアップロード

## 3. 環境変数設定

- `WEATHER_API_KEY`: OpenWeatherMap APIキー
- `CITY`: Tokyo

## 4. IAM権限追加

- `AmazonBedrockFullAccess`
- `AmazonS3ReadOnlyAccess`（将来用）
- `AmazonRDSDataFullAccess`（将来用）

## 5. テストイベント

```json
{
  "userId": "user_test_001"
}
```
