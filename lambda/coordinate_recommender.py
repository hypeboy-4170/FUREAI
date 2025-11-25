import json
import boto3
import os

CLOTHING_TABLE = os.environ.get('CLOTHING_TABLE', 'ClothingItems')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
BEDROCK_REGION = os.environ.get('BEDROCK_REGION', 'us-east-1')

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)

def lambda_handler(event, context):
    """コーディネート提案"""
    
    body = json.loads(event.get('body', '{}'))
    schedule = body.get('schedule', '通常の日')
    weather = body.get('weather', '20度 晴れ')
    
    # 衣類データ取得
    clothing_table = dynamodb.Table(CLOTHING_TABLE)
    items = clothing_table.scan()['Items']
    
    # Bedrockでコーディネート提案
    prompt = f"""あなたはファッションコーディネーターです。

【今日の予定】
{schedule}

【天気情報】
{weather}

【利用可能な衣類】
{json.dumps(items, ensure_ascii=False)}

以下のJSON形式で提案してください：
{{
  "tops": {{"itemId": "...", "reason": "..."}},
  "pants": {{"itemId": "...", "reason": "..."}},
  "outer": {{"itemId": "...", "reason": "..."}},
  "overall_comment": "..."
}}"""
    
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    
    result = json.loads(response['body'].read())
    coordinate = json.loads(result['content'][0]['text'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(coordinate, ensure_ascii=False)
    }
