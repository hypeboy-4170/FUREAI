#!/bin/bash

# Lambda関数作成 + 環境変数設定スクリプト

echo "========================================"
echo "FUREAI Lambda作成・設定スクリプト"
echo "========================================"
echo ""

# 環境変数の値
BUCKET_NAME="fureai-clothing-images"
TABLE_NAME="clothing_data_ptn1"
MODEL_ID="jp.anthropic.claude-sonnet-4-5-20250929-v1:0"
REGION="ap-northeast-1"

echo "設定する環境変数:"
echo "  BUCKET_NAME = $BUCKET_NAME"
echo "  TABLE_NAME  = $TABLE_NAME"
echo "  MODEL_ID    = $MODEL_ID"
echo ""

# Lambda関数名を入力
echo "Lambda関数名を入力してください"
echo "例: fureai-bedrock-tester"
read -p "> " FUNCTION_NAME

if [ -z "$FUNCTION_NAME" ]; then
    echo "エラー: 関数名が入力されていません"
    exit 1
fi

# Lambda関数が存在するか確認
echo ""
echo "[$FUNCTION_NAME] 存在確認中..."
aws lambda get-function --function-name "$FUNCTION_NAME" --region $REGION > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "関数が存在しません。作成しますか？ (y/n)"
    read -p "> " CREATE_FUNCTION
    
    if [ "$CREATE_FUNCTION" = "y" ]; then
        # IAMロール名を関数名から生成
        ROLE_NAME="${FUNCTION_NAME}-role"
        
        echo ""
        echo "IAMロール [$ROLE_NAME] を作成中..."
        
        # 信頼ポリシー作成
        cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
        
        # IAMロール作成
        aws iam create-role \
            --role-name "$ROLE_NAME" \
            --assume-role-policy-document file://trust-policy.json > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "✓ IAMロールを作成しました"
        else
            echo "IAMロールが既に存在します"
        fi
        
        # アカウントID取得
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"
        
        # ポリシーファイルを関数名から判定
        POLICY_FILE=""
        if [[ "$FUNCTION_NAME" == *"bedrock"* ]]; then
            POLICY_FILE="bedrock-tester-policy.json"
        elif [[ "$FUNCTION_NAME" == *"db"* ]]; then
            POLICY_FILE="db-tester-policy.json"
        elif [[ "$FUNCTION_NAME" == *"s3"* ]]; then
            POLICY_FILE="s3-tester-policy.json"
        elif [[ "$FUNCTION_NAME" == *"weather"* ]]; then
            POLICY_FILE="weather-fetcher-policy.json"
        elif [[ "$FUNCTION_NAME" == *"calendar"* ]]; then
            POLICY_FILE="calendar-fetcher-policy.json"
        elif [[ "$FUNCTION_NAME" == *"full"* ]] || [[ "$FUNCTION_NAME" == *"coordinator"* ]]; then
            POLICY_FILE="full-coordinator-policy.json"
        fi
        
        # ポリシーファイルが存在するか確認
        if [ -n "$POLICY_FILE" ] && [ -f "$POLICY_FILE" ]; then
            echo "ポリシー [$POLICY_FILE] を適用中..."
            aws iam put-role-policy \
                --role-name "$ROLE_NAME" \
                --policy-name "${FUNCTION_NAME}-policy" \
                --policy-document file://$POLICY_FILE > /dev/null
            echo "✓ ポリシーを適用しました"
        else
            echo "警告: ポリシーファイルが見つかりません ($POLICY_FILE)"
            echo "基本的なCloudWatch Logsポリシーのみ適用します"
            cat > policy.json << 'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],"Resource":"arn:aws:logs:*:*:*"}]}
EOF
            aws iam put-role-policy \
                --role-name "$ROLE_NAME" \
                --policy-name "${FUNCTION_NAME}-policy" \
                --policy-document file://policy.json > /dev/null
            rm -f policy.json
        fi
        
        rm -f trust-policy.json
        
        echo "IAMロール作成完了。AWS内での伝播を待機中（15秒）..."
        sleep 15
        
        # ダミーのzipファイル作成
        echo "import json" > lambda_function.py
        echo "def lambda_handler(event, context):" >> lambda_function.py
        echo "    return {'statusCode': 200, 'body': json.dumps('Hello')}" >> lambda_function.py
        zip function.zip lambda_function.py > /dev/null
        
        echo ""
        echo "[$FUNCTION_NAME] Lambda関数を作成中..."
        aws lambda create-function \
            --function-name "$FUNCTION_NAME" \
            --runtime python3.12 \
            --role "$ROLE_ARN" \
            --handler lambda_function.lambda_handler \
            --zip-file fileb://function.zip \
            --timeout 30 \
            --memory-size 128 \
            --region $REGION > /dev/null
        
        if [ $? -eq 0 ]; then
            echo "✓ Lambda関数を作成しました"
            echo "Lambda関数の初期化を待機中（10秒）..."
            sleep 10
        else
            echo "✗ Lambda関数の作成に失敗しました"
            rm -f lambda_function.py function.zip
            exit 1
        fi
        
        rm -f lambda_function.py function.zip
    else
        echo "処理を中止しました"
        exit 0
    fi
else
    echo "✓ Lambda関数が存在します"
fi

echo ""
echo "[$FUNCTION_NAME] 環境変数を設定中..."

aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --environment "Variables={BUCKET_NAME=$BUCKET_NAME,TABLE_NAME=$TABLE_NAME,MODEL_ID=$MODEL_ID}" \
    --region $REGION > /dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ 環境変数の設定が完了しました！"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "✗ 設定失敗（関数が存在しないか、権限がありません）"
    echo "========================================"
    exit 1
fi
