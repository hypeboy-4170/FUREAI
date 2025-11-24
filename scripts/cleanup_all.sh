#!/bin/bash
# FUREAI 全リソース削除スクリプト

REGION="ap-northeast-1"
BUCKET_NAME="fureai-clothing-images"
ROLE_NAME="FUREAILambdaExecutionRole"

echo "=== FUREAI リソース削除開始 ==="
echo ""
echo "⚠️  警告: 全てのリソースが削除されます"
echo ""
read -p "続行しますか？ (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "キャンセルしました"
    exit 0
fi

# 1. Lambda関数削除
echo ""
echo "1. Lambda関数削除中..."

for func in BedrockTester PresignedUrlGenerator ImageAnalyzer CoordinateRecommender WeatherAPIFetcher CalendarFetcher; do
    aws lambda delete-function --function-name $func --region $REGION > /dev/null 2>&1 && echo "  ✓ $func" || echo "  - $func (存在しない)"
done

# 2. IAMロール削除
echo ""
echo "2. IAMロール削除中..."

aws iam delete-role-policy --role-name $ROLE_NAME --policy-name FUREAILambdaPolicy > /dev/null 2>&1
aws iam delete-role --role-name $ROLE_NAME > /dev/null 2>&1 && echo "  ✓ $ROLE_NAME" || echo "  - $ROLE_NAME (存在しない)"

# 3. S3バケット削除
echo ""
echo "3. S3バケット削除中..."

aws s3 rm s3://$BUCKET_NAME --recursive > /dev/null 2>&1
aws s3 rb s3://$BUCKET_NAME --region $REGION > /dev/null 2>&1 && echo "  ✓ $BUCKET_NAME" || echo "  - $BUCKET_NAME (存在しない)"

# 4. DynamoDBテーブル削除
echo ""
echo "4. DynamoDBテーブル削除中..."

aws dynamodb delete-table --table-name ClothingItems --region $REGION > /dev/null 2>&1 && echo "  ✓ ClothingItems" || echo "  - ClothingItems (存在しない)"
aws dynamodb delete-table --table-name WearHistory --region $REGION > /dev/null 2>&1 && echo "  ✓ WearHistory" || echo "  - WearHistory (存在しない)"

echo ""
echo "=== 削除完了 ==="
