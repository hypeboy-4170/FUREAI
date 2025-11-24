#!/bin/bash
# FUREAI 初期セットアップスクリプト（オールインワン）

REGION="ap-northeast-1"
BUCKET_NAME="fureai-clothing-images"

echo "=== FUREAI セットアップ開始 ==="

# 1. DynamoDBテーブル作成
echo ""
echo "1. DynamoDBテーブル作成中..."
aws dynamodb create-table \
  --table-name ClothingItems \
  --attribute-definitions AttributeName=itemId,AttributeType=S \
  --key-schema AttributeName=itemId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION > /dev/null 2>&1

aws dynamodb create-table \
  --table-name WearHistory \
  --attribute-definitions \
    AttributeName=itemId,AttributeType=S \
    AttributeName=wornDate,AttributeType=S \
  --key-schema \
    AttributeName=itemId,KeyType=HASH \
    AttributeName=wornDate,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION > /dev/null 2>&1

echo "  ✓ ClothingItems"
echo "  ✓ WearHistory"
echo "  待機中（30秒）..."
sleep 30

# 2. サンプルデータ投入（imageKey含む）
echo ""
echo "2. サンプルデータ投入中..."

# トップス（6種類）
aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_001"},"itemName":{"S":"茶シャツ"},"category":{"S":"tops"},"color":{"S":"brown"},"style":{"S":"formal"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/tops_001.jpg"}}' --region $REGION
echo "  ✓ tops_001: 茶シャツ（フォーマル・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_002"},"itemName":{"S":"黒ニット"},"category":{"S":"tops"},"color":{"S":"black"},"style":{"S":"casual"},"season":{"L":[{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/tops_002.jpg"}}' --region $REGION
echo "  ✓ tops_002: 黒ニット（カジュアル・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_003"},"itemName":{"S":"グレーTシャツ"},"category":{"S":"tops"},"color":{"S":"gray"},"style":{"S":"casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/tops_003.jpg"}}' --region $REGION
echo "  ✓ tops_003: グレーTシャツ（カジュアル・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_004"},"itemName":{"S":"ネイビーポロシャツ"},"category":{"S":"tops"},"color":{"S":"navy"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"summer"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/tops_004.jpg"}}' --region $REGION
echo "  ✓ tops_004: ネイビーポロシャツ（ビジカジ・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_005"},"itemName":{"S":"ベージュセーター"},"category":{"S":"tops"},"color":{"S":"beige"},"style":{"S":"casual"},"season":{"L":[{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/tops_005.jpg"}}' --region $REGION
echo "  ✓ tops_005: ベージュセーター（カジュアル・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"tops_006"},"itemName":{"S":"ストライプシャツ"},"category":{"S":"tops"},"color":{"S":"blue"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/tops_006.jpg"}}' --region $REGION
echo "  ✓ tops_006: ストライプシャツ（ビジカジ・涼しい）"

# ボトムス（5種類）
aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_001"},"itemName":{"S":"ベージュチノパン"},"category":{"S":"pants"},"color":{"S":"beige"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/pants_001.jpg"}}' --region $REGION
echo "  ✓ pants_001: ベージュチノパン（ビジカジ・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_002"},"itemName":{"S":"黒スラックス"},"category":{"S":"pants"},"color":{"S":"black"},"style":{"S":"formal"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/pants_002.jpg"}}' --region $REGION
echo "  ✓ pants_002: 黒スラックス（フォーマル・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_003"},"itemName":{"S":"デニムパンツ"},"category":{"S":"pants"},"color":{"S":"blue"},"style":{"S":"casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/pants_003.jpg"}}' --region $REGION
echo "  ✓ pants_003: デニムパンツ（カジュアル・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_004"},"itemName":{"S":"グレースラックス"},"category":{"S":"pants"},"color":{"S":"gray"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"summer"},{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"cool"},"imageKey":{"S":"uploads/pants_004.jpg"}}' --region $REGION
echo "  ✓ pants_004: グレースラックス（ビジカジ・涼しい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"pants_005"},"itemName":{"S":"コーデュロイパンツ"},"category":{"S":"pants"},"color":{"S":"brown"},"style":{"S":"casual"},"season":{"L":[{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/pants_005.jpg"}}' --region $REGION
echo "  ✓ pants_005: コーデュロイパンツ（カジュアル・暖かい）"

# アウター（5種類）
aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_001"},"itemName":{"S":"トレンチコート"},"category":{"S":"outer"},"color":{"S":"beige"},"style":{"S":"formal"},"season":{"L":[{"S":"spring"},{"S":"autumn"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/outer_001.jpg"}}' --region $REGION
echo "  ✓ outer_001: トレンチコート（フォーマル・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_002"},"itemName":{"S":"ダウンジャケット"},"category":{"S":"outer"},"color":{"S":"black"},"style":{"S":"casual"},"season":{"L":[{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/outer_002.jpg"}}' --region $REGION
echo "  ✓ outer_002: ダウンジャケット（カジュアル・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_003"},"itemName":{"S":"ネイビージャケット"},"category":{"S":"outer"},"color":{"S":"navy"},"style":{"S":"business_casual"},"season":{"L":[{"S":"spring"},{"S":"autumn"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/outer_003.jpg"}}' --region $REGION
echo "  ✓ outer_003: ネイビージャケット（ビジカジ・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_004"},"itemName":{"S":"レザージャケット"},"category":{"S":"outer"},"color":{"S":"black"},"style":{"S":"casual"},"season":{"L":[{"S":"autumn"},{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/outer_004.jpg"}}' --region $REGION
echo "  ✓ outer_004: レザージャケット（カジュアル・暖かい）"

aws dynamodb put-item --table-name ClothingItems --item '{"itemId":{"S":"outer_005"},"itemName":{"S":"ウールコート"},"category":{"S":"outer"},"color":{"S":"gray"},"style":{"S":"formal"},"season":{"L":[{"S":"winter"}]},"warmth":{"S":"warm"},"imageKey":{"S":"uploads/outer_005.jpg"}}' --region $REGION
echo "  ✓ outer_005: ウールコート（フォーマル・暖かい）"

# 3. S3バケット作成
echo ""
echo "3. S3バケット作成中..."
aws s3 mb s3://$BUCKET_NAME --region $REGION > /dev/null 2>&1
echo "  ✓ $BUCKET_NAME"

# 4. 確認
echo ""
echo "4. セットアップ確認..."
ITEM_COUNT=$(aws dynamodb scan --table-name ClothingItems --select COUNT --query 'Count' --output text --region $REGION)
echo "  ✓ ClothingItems: ${ITEM_COUNT}件"

aws s3 ls s3://$BUCKET_NAME > /dev/null 2>&1 && echo "  ✓ S3バケット: 存在" || echo "  ✗ S3バケット: 未作成"

echo ""
echo "=== セットアップ完了 ==="
