import json
import boto3
import os
import base64
from datetime import datetime, timedelta

CLOTHING_TABLE = os.environ.get('CLOTHING_TABLE', 'ClothingItems')
HISTORY_TABLE = os.environ.get('HISTORY_TABLE', 'WearHistory')
CLOTHING_BUCKET = os.environ.get('CLOTHING_BUCKET', 'fureai-clothing-images')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20240620-v1:0')
BEDROCK_REGION = os.environ.get('BEDROCK_REGION', 'us-east-1')

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime', region_name=BEDROCK_REGION)

def lambda_handler(event, context):
    """コーディネート提案（メイン機能）"""
    
    body = json.loads(event.get('body', '{}'))
    schedule = body.get('schedule', '通常の日')
    weather = body.get('weather', {})
    
    # 衣類データ取得
    clothing_table = dynamodb.Table(CLOTHING_TABLE)
    items = clothing_table.scan()['Items']
    
    # 着用履歴取得（7日間）
    history_table = dynamodb.Table(HISTORY_TABLE)
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    recent_worn = []
    
    for item in items:
        response = history_table.query(
            KeyConditionExpression='itemId = :id AND wornDate >= :date',
            ExpressionAttributeValues={':id': item['itemId'], ':date': seven_days_ago}
        )
        if response['Items']:
            recent_worn.append(item['itemId'])
    
    # 利用可能な衣類
    available = [i for i in items if i['itemId'] not in recent_worn]
    
    # 画像付き衣類データを取得
    items_with_images = []
    for item in available:
        if 'imageKey' in item:
            try:
                # S3から画像取得
                image_obj = s3.get_object(Bucket=CLOTHING_BUCKET, Key=item['imageKey'])
                image_bytes = image_obj['Body'].read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                items_with_images.append({
                    'item': item,
                    'image': image_base64
                })
            except Exception as e:
                # 画像取得失敗時はスキップ（画像なしでも動作）
                print(f"画像取得失敗: {item['itemId']} - {str(e)}")
                pass
    
    # Bedrockでコーディネート提案（画像を見ながら）
    prompt = f"""あなたはファッションコーディネーターです。

【ユーザー情報】
年齢: 30代、職業: 会社員、好み: シンプル

【今日の予定】
{schedule}

【天気情報】
気温: {weather.get('temp', 20)}℃、天候: {weather.get('condition', '曇り')}

【利用可能な衣類】
{json.dumps(available, ensure_ascii=False)}

※画像を確認して、実際の色味・デザイン・素材感を考慮してください

【最近着用した服（提案しないでください）】
{recent_worn}

以下のJSON形式で提案してください：
{{
  "tops": {{"itemId": "...", "reason": "..."}},
  "pants": {{"itemId": "...", "reason": "..."}},
  "outer": {{"itemId": "...", "reason": "..."}},
  "overall_comment": "..."
}}"""

    # プロンプトに画像を追加
    content = [{"type": "text", "text": prompt}]
    
    # 画像がある場合のみ追加
    if items_with_images:
        for item_with_image in items_with_images[:10]:  # 最大10枚まで
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": item_with_image['image']
                }
            })
            content.append({
                "type": "text",
                "text": f"画像: {item_with_image['item']['itemId']} - {item_with_image['item']['itemName']}"
            })
    else:
        # 画像がない場合はテキスト情報のみで提案
        content.append({
            "type": "text",
            "text": "※画像情報はありません。テキスト情報のみで提案してください。"
        })
    
    response = bedrock.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": content}]
        })
    )
    
    result = json.loads(response['body'].read())
    coordinate = json.loads(result['content'][0]['text'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(coordinate, ensure_ascii=False)
    }
