import json
import boto3
import os
import requests
from datetime import datetime

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')

CLOTHING_TABLE = os.environ.get('CLOTHING_TABLE', 'ClothingItems')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')

def lambda_handler(event, context):
    """
    OpenWeatherMap APIから天気情報を取得してコーディネート提案
    """
    try:
        body = json.loads(event.get('body', '{}'))
        
        location = body.get('location', 'Tokyo')
        
        # 天気API呼び出し（OpenWeatherMap）
        weather_data = fetch_weather(location)
        
        # DynamoDBから衣類データ取得
        table = dynamodb.Table(CLOTHING_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # Bedrockでコーディネート提案
        prompt = f"""
以下の条件で最適なコーディネートを提案してください。

天気情報:
- 場所: {location}
- 気温: {weather_data['temp']}度
- 天候: {weather_data['condition']}
- 湿度: {weather_data['humidity']}%

利用可能な衣類:
{json.dumps(items, ensure_ascii=False, indent=2)}

JSON形式で回答してください:
{{
  "tops": {{"itemId": "...", "reason": "..."}},
  "pants": {{"itemId": "...", "reason": "..."}},
  "outer": {{"itemId": "..." or null, "reason": "..."}},
  "overall_comment": "..."
}}
"""
        
        bedrock_response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        response_body = json.loads(bedrock_response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        # JSON部分を抽出
        coordinate = json.loads(ai_response.strip())
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'weather': weather_data,
                'coordinate': coordinate
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def fetch_weather(location):
    """
    OpenWeatherMap APIから天気情報を取得
    """
    if not WEATHER_API_KEY:
        # モックデータ
        return {
            'temp': 20,
            'condition': '曇り',
            'humidity': 60,
            'source': 'mock'
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        return {
            'temp': int(data['main']['temp']),
            'condition': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'source': 'api'
        }
    except Exception as e:
        print(f"Weather API Error: {str(e)}")
        # エラー時はモックデータ
        return {
            'temp': 20,
            'condition': '曇り',
            'humidity': 60,
            'source': 'mock'
        }
