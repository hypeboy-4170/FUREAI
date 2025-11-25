#!/bin/bash
REGION="ap-northeast-1"

echo "=== UT環境セットアップ開始 ==="

# 1. DynamoDBテーブル作成
echo ""
echo "1. DynamoDBテーブル作成中..."
aws dynamodb create-table \
  --table-name ClothingItems \
  --attribute-definitions AttributeName=itemId,AttributeType=S \
  --key-schema AttributeName=itemId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION > /dev/null 2>&1

echo "  ✓ ClothingItems"
echo "  待機中（30秒）..."
sleep 30

# 2. サンプルデータ投入（7件）
echo ""
echo "2. サンプルデータ投入中..."

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_001"},"itemName":{"S":"茶シャツ"},"category":{"S":"tops"},"color":{"S":"brown"},"style":{"S":"formal"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"}}' --region $REGION
echo "  ✓ tops_001: 茶シャツ"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_002"},"itemName":{"S":"黒ニット"},"category":{"S":"tops"},"color":{"S":"black"},"style":{"S":"casual"},"season":{"L":[{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"warm"}}' --region $REGION
echo "  ✓ tops_002: 黒ニット"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_003"},"itemName":{"S":"グレーTシャツ"},"category":{"S":"tops"},"color":{"S":"gray"},"style":{"S":"casual"},"season":{"L":[{"S":"spring"},{"S":"summer"}]},"warmth":{"S":"cool"}}' --region $REGION
echo "  ✓ tops_003: グレーTシャツ"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_001"},"itemName":{"S":"ベージュチノパン"},"category":{"S":"pants"},"color":{"S":"beige"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"}}' --region $REGION
echo "  ✓ pants_001: ベージュチノパン"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_002"},"itemName":{"S":"黒スラックス"},"category":{"S":"pants"},"color":{"S":"black"},"style":{"S":"formal"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"cool"}}' --region $REGION
echo "  ✓ pants_002: 黒スラックス"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_001"},"itemName":{"S":"トレンチコート"},"category":{"S":"outer"},"color":{"S":"beige"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"autumn"}]},"warmth":{"S":"warm"}}' --region $REGION
echo "  ✓ outer_001: トレンチコート"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_002"},"itemName":{"S":"ダウンジャケット"},"category":{"S":"outer"},"color":{"S":"navy"},"style":{"S":"casual"},"season":{"L":[{"S":"winter"}]},"warmth":{"S":"warm"}}' --region $REGION
echo "  ✓ outer_002: ダウンジャケット"

# 3. 確認
echo ""
echo "3. セットアップ確認..."
ITEM_COUNT=$(aws dynamodb scan --table-name ClothingItems --select COUNT --query 'Count' --output text --region $REGION)
echo "  ✓ ClothingItems: ${ITEM_COUNT}件"

echo ""
echo "=== セットアップ完了 ==="
