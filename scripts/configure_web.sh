#!/bin/bash
# config.jsにLambda URLを自動設定するスクリプト

REGION="ap-northeast-1"

echo "=== Lambda URL自動設定 ==="
echo ""

# 各Lambda関数のURLを取得
echo "Lambda Function URLを取得中..."
BEDROCK_URL=$(aws lambda get-function-url-config --function-name BedrockTester --query 'FunctionUrl' --output text --region $REGION 2>/dev/null)
PRESIGNED_URL=$(aws lambda get-function-url-config --function-name PresignedUrlGenerator --query 'FunctionUrl' --output text --region $REGION 2>/dev/null)
COORDINATE_URL=$(aws lambda get-function-url-config --function-name CoordinateRecommender --query 'FunctionUrl' --output text --region $REGION 2>/dev/null)
WEATHER_URL=$(aws lambda get-function-url-config --function-name WeatherAPIFetcher --query 'FunctionUrl' --output text --region $REGION 2>/dev/null)
CALENDAR_URL=$(aws lambda get-function-url-config --function-name CalendarFetcher --query 'FunctionUrl' --output text --region $REGION 2>/dev/null)

if [ -z "$BEDROCK_URL" ] || [ "$BEDROCK_URL" == "None" ]; then
    echo "❌ エラー: Lambda Function URLが見つかりません"
    echo "先に ./scripts/deploy_lambda.sh を実行してください"
    exit 1
fi

echo "✓ BedrockTester: $BEDROCK_URL"
echo "✓ PresignedUrlGenerator: $PRESIGNED_URL"
echo "✓ CoordinateRecommender: $COORDINATE_URL"
echo "✓ WeatherAPIFetcher: $WEATHER_URL"
echo "✓ CalendarFetcher: $CALENDAR_URL"
echo ""

# config.jsを作成
cat > web/config.js << EOF
// Lambda Function URLs設定ファイル（自動生成）
// 再生成: ./scripts/configure_web.sh

const LAMBDA_URLS = {
    bedrock: '${BEDROCK_URL}',
    presigned: '${PRESIGNED_URL}',
    coordinate: '${COORDINATE_URL}',
    weather: '${WEATHER_URL}',
    calendar: '${CALENDAR_URL}'
};
EOF

echo "✓ web/config.js を作成しました"
echo ""
echo "=== 設定完了 ==="
echo ""
echo "次のステップ:"
echo "1. ブラウザで web/index.html を開く"
echo "2. テスト実行"
echo ""
