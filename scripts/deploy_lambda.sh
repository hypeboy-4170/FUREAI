#!/bin/bash
REGION="ap-northeast-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_NAME="FUREAILambdaExecutionRole"

echo "=== Lambda関数デプロイ開始 ==="

# 1. IAMロール作成
echo ""
echo "1. IAMロール作成中..."

cat > /tmp/trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file:///tmp/trust-policy.json \
  > /dev/null 2>&1

cat > /tmp/lambda-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:Scan",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/ClothingItems"
    },
    {
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel"],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name $ROLE_NAME \
  --policy-name FUREAILambdaPolicy \
  --policy-document file:///tmp/lambda-policy.json \
  > /dev/null 2>&1

echo "  ✓ IAMロール: $ROLE_NAME"
echo "  待機中（10秒）..."
sleep 10

# 2. Lambda関数パッケージ作成
echo ""
echo "2. Lambda関数パッケージ作成中..."

cd lambda
zip -q coordinate_recommender.zip coordinate_recommender.py
echo "  ✓ coordinate_recommender.zip"

# 3. Lambda関数作成
echo ""
echo "3. Lambda関数作成中..."

ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

aws lambda create-function \
  --function-name CoordinateRecommender \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler coordinate_recommender.lambda_handler \
  --zip-file fileb://coordinate_recommender.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables={CLOTHING_TABLE=ClothingItems} \
  --region $REGION \
  > /dev/null 2>&1

echo "  ✓ CoordinateRecommender"

rm coordinate_recommender.zip
cd ..

echo ""
echo "=== デプロイ完了 ==="
echo ""
echo "テスト実行:"
echo "aws lambda invoke --function-name CoordinateRecommender --payload '{\"body\": \"{\\\"schedule\\\": \\\"会議\\\", \\\"weather\\\": \\\"20度 晴れ\\\"}\"}' response.json"
