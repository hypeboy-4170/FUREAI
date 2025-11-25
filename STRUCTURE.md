# ファイル構成

```
FUREAI/
├── lambda/
│   └── coordinate_recommender.py    # Lambda関数（コーディネート提案）
├── scripts/
│   ├── setup_all.sh                 # DynamoDB・IAM・Lambda一括セットアップ
│   └── deploy_lambda.sh             # Lambda関数デプロイ
├── iam/
│   └── lambda-execution-policy.json # Lambda実行ロールのポリシー
├── SETUP.md                         # セットアップ手順
└── STRUCTURE.md                     # このファイル
```

## 各ファイルの役割

### lambda/coordinate_recommender.py
- DynamoDBから衣類データ取得
- Bedrockでコーディネート提案
- 入力: schedule（予定）、weather（天気）
- 出力: tops/pants/outerの提案JSON

### scripts/setup_all.sh
- DynamoDBテーブル作成（ClothingItems）
- サンプルデータ投入（7件）
- IAMロール作成
- Lambda関数作成

### scripts/deploy_lambda.sh
- Lambda関数コード更新専用

### iam/lambda-execution-policy.json
- DynamoDB読み取り権限
- Bedrock実行権限
- CloudWatch Logs書き込み権限
