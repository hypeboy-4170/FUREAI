import json
import boto3
import base64
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'fureai-clothing-images')
TABLE_NAME = os.environ.get('TABLE_NAME', 'ClothingItems')

def lambda_handler(event, context):
    """
    S3にアップロードされた画像を分析してDynamoDBに登録
    """
    try:
        # S3イベントから画像キーを取得
        if 'Records' in event:
            # S3トリガー
            s3_key = event['Records'][0]['s3']['object']['key']
        else:
            # 手動実行
            body = json.loads(event.get('body', '{}'))
            s3_key = body.get('s3Key')
        
        if not s3_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 's3Key is required'})
            }
        
        # itemIdを抽出（uploads/tops_001.jpg → tops_001）
        item_id = s3_key.split('/')[-1].split('.')[0]
        
        # S3から画像取得
        response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        image_data = response['Body'].read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Bedrockで画像分析
        prompt = """
この衣類の画像を分析して、以下のJSON形式で回答してください。

{
  "itemName": "衣類の名前（例: 白シャツ、黒ニット）",
  "category": "tops/pants/outer のいずれか",
  "color": "主な色（例: white, black, brown, beige, gray, navy, blue）",
  "style": "formal/casual/business_casual のいずれか",
  "season": ["spring", "summer", "autumn", "winter"] から適切なものを配列で,
  "warmth": "warm/cool のいずれか"
}

JSONのみを返してください。説明は不要です。
"""
        
        bedrock_response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }]
            })
        )
        
        response_body = json.loads(bedrock_response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        # JSON部分を抽出
        ai_data = json.loads(ai_response.strip())
        
        # DynamoDBに登録
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'itemId': item_id,
                'imageKey': s3_key,
                'itemName': ai_data['itemName'],
                'category': ai_data['category'],
                'color': ai_data['color'],
                'style': ai_data['style'],
                'season': ai_data['season'],
                'warmth': ai_data['warmth']
            }
        )
        
        print(f"✓ DynamoDB登録完了: {item_id}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'itemId': item_id,
                'data': ai_data,
                'message': 'Successfully analyzed and registered'
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
