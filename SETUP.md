# FUREAI UT環境セットアップ

## 🎯 目的

サンプルデータからコーディネート提案ができるか確認

---

## 🚀 セットアップ（1分）

```bash
# 1. DynamoDB + サンプルデータ作成
chmod +x scripts/*.sh
./scripts/setup_all.sh

# 2. Lambda関数デプロイ
./scripts/deploy_lambda.sh
```

```

### 期待結果

```json
{
  "statusCode": 200,
  "body": "{\"tops\": {\"itemId\": \"tops_001\", \"reason\": \"茶シャツはフォーマルな印象\"}, \"pants\": {\"itemId\": \"pants_002\", \"reason\": \"黒スラックスはフォーマルに最適\"}, \"outer\": {\"itemId\": null, \"reason\": \"暖かいのでアウター不要\"}, \"overall_comment\": \"会議に最適なコーディネート\"}"
}
```

---

## 📦 構成

| リソース | 名前 | 用途 |
|---------|------|------|
| DynamoDB | ClothingItems | サンプルデータ（7件） |
| Lambda | CoordinateRecommender | コーディネート提案 |
| IAM Role | FUREAILambdaExecutionRole | Lambda実行ロール |

---

## 🗑️ 削除

```bash
# DynamoDB削除
aws dynamodb delete-table --table-name ClothingItems

# Lambda削除
aws lambda delete-function --function-name CoordinateRecommender

# IAMロール削除
aws iam delete-role-policy --role-name FUREAILambdaExecutionRole --policy-name FUREAILambdaPolicy
aws iam delete-role --role-name FUREAILambdaExecutionRole
```

---

## 💰 コスト

月間100回実行: 約$0.60

- Lambda: $0.13
- DynamoDB: $0.01
- Bedrock: $0.45
