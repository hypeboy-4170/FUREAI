import json
import boto3
import os
from datetime import datetime, timedelta

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')

CLOTHING_TABLE = os.environ.get('CLOTHING_TABLE', 'ClothingItems')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

def lambda_handler(event, context):
    """
    Googleカレンダーから本日の予定を取得してコーディネート提案
    ※ 天気APIは現在の天気のみ対応（未来予測は有料プラン）
    """
    try:
        body = json.loads(event.get('body', '{}'))
        
        # 常に本日の日付を使用
        today = datetime.now().strftime('%Y-%m-%d')
        location = body.get('location', 'Tokyo')
        
        # カレンダー予定取得（本日のみ）
        schedule_data = fetch_calendar_events(today)
        
        # 天気情報取得（現在の天気）
        weather_data = get_current_weather(location)
        
        # DynamoDBから衣類データ取得
        table = dynamodb.Table(CLOTHING_TABLE)
        response = table.scan()
        items = response.get('Items', [])
        
        # Bedrockでコーディネート提案
        prompt = f"""
以下の条件で最適なコーディネートを提案してください。

予定情報:
{json.dumps(schedule_data, ensure_ascii=False, indent=2)}

天気情報:
- 日付: {date}
- 場所: {location}
- 気温: {weather_data['temp']}度
- 天候: {weather_data['condition']}

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
        
        coordinate = json.loads(ai_response.strip())
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'schedule': schedule_data,
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

def fetch_calendar_events(today):
    """
    Googleカレンダーから本日の予定を取得（モック実装）
    """
    if not GOOGLE_API_KEY:
        # モックデータ（本日の予定）
        return {
            'date': today,
            'events': [
                {'time': '10:00-12:00', 'summary': '会議', 'location': 'オフィス'},
                {'time': '14:00-15:00', 'summary': 'クライアント訪問', 'location': '外出'}
            ],
            'source': 'mock'
        }
    
    # TODO: Google Calendar API実装（本日の予定のみ取得）
    return {
        'date': today,
        'events': [],
        'source': 'api'
    }

def get_current_weather(location):
    """
    現在の天気を取得（OpenWeatherMap無料版は現在のみ対応）
    """
    return {
        'temp': 20,
        'condition': '晴れ',
        'source': 'mock',
        'note': '現在の天気（無料APIは予報非対応）'
    }
