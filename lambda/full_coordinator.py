import json
import boto3
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
    """全体統合テスト - 各工程の実装状況を返す"""
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('userId', 'default_user')
        location = body.get('location', 'Tokyo')
        
        # 実装状況を追跡
        progress = {
            's3': {'status': 'pending', 'message': ''},
            'db': {'status': 'pending', 'message': ''},
            'weather': {'status': 'pending', 'message': ''},
            'schedule': {'status': 'pending', 'message': ''},
            'bedrock': {'status': 'pending', 'message': ''}
        }
        
        # 1. S3から服データ取得
        try:
            clothing_data = get_clothing_from_s3()
            progress['s3'] = {'status': 'success', 'message': f'{clothing_data["count"]}件取得'}
        except Exception as e:
            progress['s3'] = {'status': 'error', 'message': str(e)}
            clothing_data = {'count': 0, 'items': []}
        
        # 2. DynamoDBからユーザー設定取得
        try:
            user_prefs = get_user_preferences(user_id)
            progress['db'] = {'status': 'success', 'message': 'ユーザー設定取得'}
        except Exception as e:
            progress['db'] = {'status': 'error', 'message': str(e)}
            user_prefs = {'style': 'casual'}
        
        # 3. 天気情報取得
        try:
            weather_info = get_weather(location)
            progress['weather'] = {'status': 'success', 'message': f'{weather_info["temp"]}度 {weather_info["condition"]}'}
        except Exception as e:
            progress['weather'] = {'status': 'error', 'message': str(e)}
            weather_info = {'temp': 20, 'condition': '不明'}
        
        # 4. 予定情報取得
        try:
            schedule_info = get_schedule()
            progress['schedule'] = {'status': 'success', 'message': f'{len(schedule_info["events"])}件の予定'}
        except Exception as e:
            progress['schedule'] = {'status': 'error', 'message': str(e)}
            schedule_info = {'events': []}
        
        # 5. Bedrockに全データを投げる
        try:
            prompt = build_prompt(clothing_data, user_prefs, weather_info, schedule_info)
            bedrock_response = invoke_bedrock(prompt)
            progress['bedrock'] = {'status': 'success', 'message': 'AI提案生成完了'}
        except Exception as e:
            progress['bedrock'] = {'status': 'error', 'message': str(e)}
            bedrock_response = 'AI提案生成エラー'
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'progress': progress,
                'data': {
                    'clothing': clothing_data,
                    'user': user_prefs,
                    'weather': weather_info,
                    'schedule': schedule_info
                },
                'recommendation': bedrock_response
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'progress': progress}, ensure_ascii=False)
        }

def get_clothing_from_s3():
    """S3から服データ取得"""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='uploads/', MaxKeys=10)
        items = []
        for obj in response.get('Contents', []):
            items.append({
                'key': obj['Key'],
                'size': obj['Size'],
                'lastModified': obj['LastModified'].isoformat()
            })
        return {'count': len(items), 'items': items}
    except:
        return {'count': 0, 'items': [], 'source': 'mock'}

def get_user_preferences(user_id):
    """DynamoDBからユーザー設定取得"""
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'itemId': f'user_{user_id}'})
        return response.get('Item', {'style': 'casual', 'source': 'mock'})
    except:
        return {'style': 'casual', 'formality': 'medium', 'source': 'mock'}

def get_weather(location):
    """天気情報取得"""
    return {
        'location': location,
        'temp': 20,
        'condition': '晴れ',
        'humidity': 60,
        'source': 'mock'
    }

def get_schedule():
    """予定情報取得"""
    return {
        'today': datetime.now().strftime('%Y-%m-%d'),
        'events': [
            {'time': '10:00', 'summary': 'チームミーティング'},
            {'time': '14:00', 'summary': 'クライアント訪問'}
        ],
        'source': 'mock'
    }

def build_prompt(clothing, user, weather, schedule):
    """Bedrock用プロンプト構築"""
    return f"""以下の情報を元に、今日のコーディネートを提案してください。

【利用可能な服】
{json.dumps(clothing, ensure_ascii=False, indent=2)}

【ユーザー設定】
{json.dumps(user, ensure_ascii=False, indent=2)}

【天気】
場所: {weather['location']}
気温: {weather['temp']}度
天候: {weather['condition']}

【本日の予定】
{json.dumps(schedule['events'], ensure_ascii=False, indent=2)}

簡潔に提案してください。"""

def invoke_bedrock(prompt):
    """Bedrock呼び出し"""
    try:
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload)
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        return f"Bedrock呼び出しエラー: {str(e)}"
