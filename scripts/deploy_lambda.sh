#!/bin/bash
# Lambda関数デプロイスクリプト

REGION="ap-northeast-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_NAME="FUREAILambdaExecutionRole"
BUCKET_NAME="fureai-clothing-images"

echo "=== Lambda関数デプロイ開始 ==="

# 1. IAMロール作成
echo ""
echo "1. IAMロール作成中..."

# 信頼ポリシー
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

# 実行ポリシー
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
        "dynamodb:Query",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/ClothingItems"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
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

zip -q bedrock_tester.zip bedrock_tester.py
zip -q presigned_url_generator.zip presigned_url_generator.py
zip -q image_analyzer.zip image_analyzer.py
zip -q coordinate_recommender.zip coordinate_recommender.py
zip -q weather_api_fetcher.zip weather_api_fetcher.py
zip -q calendar_fetcher.zip calendar_fetcher.py

echo "  ✓ 6関数のパッケージ作成完了"

# 3. Lambda関数作成
echo ""
echo "3. Lambda関数作成中..."

ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

# BedrockTester
aws lambda create-function \
  --function-name BedrockTester \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler bedrock_tester.lambda_handler \
  --zip-file fileb://bedrock_tester.zip \
  --timeout 30 \
  --memory-size 128 \
  --region $REGION > /dev/null 2>&1
echo "  ✓ BedrockTester"

# PresignedUrlGenerator
aws lambda create-function \
  --function-name PresignedUrlGenerator \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler presigned_url_generator.lambda_handler \
  --zip-file fileb://presigned_url_generator.zip \
  --timeout 10 \
  --memory-size 128 \
  --environment Variables={BUCKET_NAME=$BUCKET_NAME} \
  --region $REGION > /dev/null 2>&1
echo "  ✓ PresignedUrlGenerator"

# ImageAnalyzer
aws lambda create-function \
  --function-name ImageAnalyzer \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler image_analyzer.lambda_handler \
  --zip-file fileb://image_analyzer.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables={BUCKET_NAME=$BUCKET_NAME,TABLE_NAME=ClothingItems} \
  --region $REGION > /dev/null 2>&1
echo "  ✓ ImageAnalyzer"

# CoordinateRecommender
aws lambda create-function \
  --function-name CoordinateRecommender \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler coordinate_recommender.lambda_handler \
  --zip-file fileb://coordinate_recommender.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables={CLOTHING_TABLE=ClothingItems,HISTORY_TABLE=WearHistory} \
  --region $REGION > /dev/null 2>&1
echo "  ✓ CoordinateRecommender"

# WeatherAPIFetcher
aws lambda create-function \
  --function-name WeatherAPIFetcher \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler weather_api_fetcher.lambda_handler \
  --zip-file fileb://weather_api_fetcher.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables={CLOTHING_TABLE=ClothingItems} \
  --region $REGION > /dev/null 2>&1
echo "  ✓ WeatherAPIFetcher"

# CalendarFetcher
aws lambda create-function \
  --function-name CalendarFetcher \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler calendar_fetcher.lambda_handler \
  --zip-file fileb://calendar_fetcher.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables={CLOTHING_TABLE=ClothingItems} \
  --region $REGION > /dev/null 2>&1
echo "  ✓ CalendarFetcher"

# S3トリガー設定（ImageAnalyzerのみ）
echo ""
echo "4. S3トリガー設定中..."

aws lambda add-permission \
  --function-name ImageAnalyzer \
  --statement-id S3InvokeFunction \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::${BUCKET_NAME} \
  --region $REGION > /dev/null 2>&1

aws s3api put-bucket-notification-configuration \
  --bucket $BUCKET_NAME \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "LambdaFunctionArn": "arn:aws:lambda:'$REGION':'$ACCOUNT_ID':function:ImageAnalyzer",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [{
            "Name": "prefix",
            "Value": "uploads/"
          }]
        }
      }
    }]
  }' > /dev/null 2>&1

echo "  ✓ S3トリガー: uploads/* → ImageAnalyzer"

# 5. Function URL作成（5関数、ImageAnalyzerはS3トリガーのみ）
echo ""
echo "5. Function URL作成中..."

for func in BedrockTester PresignedUrlGenerator CoordinateRecommender WeatherAPIFetcher CalendarFetcher; do
  aws lambda create-function-url-config \
    --function-name $func \
    --auth-type NONE \
    --cors AllowOrigins='*',AllowMethods='POST,OPTIONS',AllowHeaders='Content-Type' \
    --region $REGION > /dev/null 2>&1
  
  aws lambda add-permission \
    --function-name $func \
    --statement-id FunctionURLAllowPublicAccess \
    --action lambda:InvokeFunctionUrl \
    --principal '*' \
    --function-url-auth-type NONE \
    --region $REGION > /dev/null 2>&1
  
  echo "  ✓ $func URL"
done

# クリーンアップ
rm -f *.zip
cd ..

# URL取得
BEDROCK_URL=$(aws lambda get-function-url-config --function-name BedrockTester --query 'FunctionUrl' --output text 2>/dev/null)

# 6. 結果表示
echo ""
echo "=== デプロイ完了 ==="
echo ""
echo "📋 次のステップ:"
echo ""
echo "1. web/index.html を開く"
echo "2. LAMBDA_URL を以下に設定:"
echo ""
echo "const LAMBDA_URL = '${BEDROCK_URL}';"
echo ""
echo "3. ブラウザでテスト実行"
echo ""
echo "=== リスク確認 ==="
echo "✓ ImageAnalyzerはS3トリガーのみ（uploads/*）"
echo "✓ 他の5関数はFunction URL経由で手動呼び出しのみ"
echo "✓ Lambda間の相互呼び出しなし → ループリスクなし"
echo ""
