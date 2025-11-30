import json
import boto3
import base64
import os
from datetime import datetime

# 環境変数から取得（Lambda設定画面で設定）
BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
MODEL_ID = os.environ['MODEL_ID']

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')

def lambda_handler(event, context):
    """S3アップロード→Bedrock分析→DB登録→コーデ提案"""
    try:
        body = json.loads(event.get('body', '{}'))
        image_data = body.get('imageData')
        
        if not image_data:
            raise Exception('画像データが必要です')
        
        item_id = f'item_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        # 1. S3にアップロード
        s3_key = f'uploads/{item_id}.jpg'
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        
        # 2. Bedrockで画像分析
        analysis = analyze_image_with_bedrock(image_bytes)
        
        # 3. DynamoDBに登録
        table = dynamodb.Table(TABLE_NAME)
        db_item = {
            'itemId': item_id,
            'category': analysis['category'],
            'color': analysis['color'],
            'season': analysis['season'],
            'formality': analysis['formality'],
            's3Key': s3_key,
            's3Bucket': BUCKET_NAME,
            'timestamp': datetime.now().isoformat()
        }
        table.put_item(Item=db_item)
        
        # 4. コーデ提案
        recommendation = get_coordinate_recommendation(db_item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                's3Upload': {'bucket': BUCKET_NAME, 'key': s3_key},
                'imageAnalysis': analysis,
                'dbRegistration': db_item,
                'recommendation': recommendation
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False)
        }

def analyze_image_with_bedrock(image_bytes):
    """Bedrockで画像分析"""
    try:
        prompt = """この服の画像を分析して、以下の情報をJSON形式で返してください:
- category: tops/pants/outer のいずれか
- color: 色（日本語）
- season: spring/summer/autumn/winter/all のいずれか
- formality: casual/business/formal のいずれか

JSON形式のみで回答してください。"""
        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode('utf-8')}},
                    {"type": "text", "text": prompt}
                ]
            }]
        }
        
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload)
        )
        
        result = json.loads(response['body'].read())
        text = result['content'][0]['text']
        return json.loads(text.strip('```json').strip('```').strip())
    except:
        return {'category': 'tops', 'color': '不明', 'season': 'all', 'formality': 'casual'}

def get_coordinate_recommendation(item):
    """DBデータからコーデ提案"""
    try:
        prompt = f"""以下の服アイテムを使ったコーディネートを提案してください:

アイテム情報:
- カテゴリ: {item['category']}
- 色: {item['color']}
- 季節: {item['season']}
- フォーマル度: {item['formality']}

簡潔に提案してください。"""
        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload)
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        return f"提案生成エラー: {str(e)}"
