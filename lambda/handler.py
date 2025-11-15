"""
FUREAI メインLambda関数
"""
import json
import os
import boto3
import requests
from datetime import datetime

def lambda_handler(event, context):
    """
    Alexaからのリクエストを処理してコーディネートを提案
    """
    user_id = event.get('userId', 'user_test_001')
    
    # 1. 天気情報取得
    weather = get_weather()
    
    # 2. 予定情報取得
    schedule = get_schedule(user_id)
    
    # 3. 服データ取得
    clothes = get_clothes(user_id)
    
    # 4. Bedrock AIで提案生成
    outfit = generate_outfit(weather, schedule, clothes)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'weather': weather,
            'schedule': schedule,
            'outfit': outfit
        }, ensure_ascii=False)
    }

def get_weather():
    """天気情報取得"""
    api_key = os.getenv('WEATHER_API_KEY')
    city = os.getenv('CITY', 'Tokyo')
    
    if not api_key:
        return {"condition": "晴れ", "temp": 26}
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"
        response = requests.get(url, timeout=5)
        data = response.json()
        return {
            "condition": data['weather'][0]['description'],
            "temp": data['main']['temp']
        }
    except:
        return {"condition": "晴れ", "temp": 26}

def get_schedule(user_id):
    """予定情報取得"""
    # Googleカレンダーから今日の予定を取得
    calendar_token = os.getenv('GOOGLE_CALENDAR_TOKEN')
    
    if calendar_token:
        try:
            return get_google_calendar(calendar_token)
        except:
            pass
    
    # フォールバック: 曜日ベース
    from datetime import datetime
    today = datetime.now().weekday()
    
    if today < 5:
        return {"meeting": True, "time": "14:00", "type": "business"}
    else:
        return {"meeting": False, "type": "casual"}

def get_clothes(user_id):
    """服データ取得（モック）"""
    return [
        {"id": 1, "s3_key": "user001/shirt_white.jpg", "category": "tops", "color": "white", "tags": "formal"},
        {"id": 2, "s3_key": "user001/pants_gray.jpg", "category": "bottoms", "color": "gray", "tags": "formal"},
        {"id": 3, "s3_key": "user001/tshirt_blue.jpg", "category": "tops", "color": "blue", "tags": "casual"},
        {"id": 4, "s3_key": "user001/jeans_black.jpg", "category": "bottoms", "color": "black", "tags": "casual"}
    ]

def get_google_calendar(token):
    """Googleカレンダーから今日の予定取得"""
    from datetime import datetime, timedelta
    
    # 今日の開始・終了時刻
    now = datetime.utcnow()
    time_min = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    time_max = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    
    url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    params = {
        'timeMin': time_min,
        'timeMax': time_max,
        'singleEvents': True,
        'orderBy': 'startTime'
    }
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, params=params, headers=headers, timeout=5)
    data = response.json()
    
    events = data.get('items', [])
    
    if not events:
        return {"meeting": False, "type": "free"}
    
    # 最初の予定を取得
    first_event = events[0]
    summary = first_event.get('summary', '')
    start_time = first_event['start'].get('dateTime', first_event['start'].get('date'))
    
    # 予定の種類を推測
    event_type = "business"
    if any(word in summary.lower() for word in ['会議', 'meeting', '打ち合わせ']):
        event_type = "business"
    elif any(word in summary.lower() for word in ['食事', 'ランチ', 'lunch', 'dinner']):
        event_type = "casual"
    
    return {
        "meeting": True,
        "time": start_time,
        "type": event_type,
        "summary": summary
    }

def generate_outfit(weather, schedule, clothes):
    """Bedrock AIでコーディネート生成"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        schedule_text = "会議あり" if schedule.get('meeting') else "予定なし"
        if schedule.get('type'):
            schedule_text += f" ({schedule['type']})"
        
        prompt = f"""あなたはスタイリストAIです。以下の情報から最適なコーディネートを提案してください。

天気: {weather['condition']} {weather['temp']}度
予定: {schedule_text}
利用可能な服: {json.dumps(clothes, ensure_ascii=False)}

JSON形式で回答してください:
{{"item_ids": [1, 2], "explanation": "理由"}}"""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        answer = result['content'][0]['text']
        return json.loads(answer)
    except:
        return {
            "item_ids": [1, 2],
            "explanation": f"{weather['condition']}で{weather['temp']}度、会議があるためフォーマルな白シャツとグレーのパンツを提案します。"
        }
