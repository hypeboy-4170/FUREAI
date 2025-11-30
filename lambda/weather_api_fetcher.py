import json

def lambda_handler(event, context):
    """天気API疎通テスト（モック）"""
    try:
        body = json.loads(event.get('body', '{}'))
        if isinstance(body, str):
            body = json.loads(body)
        
        location = body.get('location', 'Tokyo')
        
        # モックデータ（実際はOpenWeatherMap APIを呼び出す）
        weather_data = {
            'location': location,
            'temp': 20,
            'condition': '晴れ',
            'humidity': 60,
            'source': 'mock'
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(weather_data, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False)
        }
