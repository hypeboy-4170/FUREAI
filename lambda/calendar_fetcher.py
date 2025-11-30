import json
from datetime import datetime

def lambda_handler(event, context):
    """予定API疎通テスト（モック）"""
    try:
        # モックデータ（実際はGoogleカレンダーAPIを呼び出す）
        schedule_data = {
            'today': datetime.now().strftime('%Y-%m-%d'),
            'events': [
                {'time': '10:00', 'summary': 'チームミーティング'},
                {'time': '14:00', 'summary': 'クライアント訪問'}
            ],
            'source': 'mock',
            'schedule': {
                'events': [
                    {'time': '10:00', 'summary': 'チームミーティング'},
                    {'time': '14:00', 'summary': 'クライアント訪問'}
                ]
            }
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(schedule_data, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False)
        }
