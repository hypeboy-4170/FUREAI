import boto3
import json
import os
from datetime import datetime

# 環境変数から取得（Lambda設定画面で設定）
TABLE_NAME = os.environ['TABLE_NAME']
MODEL_ID = os.environ['MODEL_ID']

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """DBデータでコーディネート提案"""
    try:
        # DBから全アイテム取得
        response = table.scan()
        items = response.get('Items', [])
        
        # clothing_dataキーで取得した場合の対応
        if isinstance(items, dict) and 'clothing_data' in items:
            items = items['clothing_data']
        
        if not items:
            # テストデータ作成
            test_items = [
                {'itemId': 'tops_001', 'category': 'tops', 'color': '白', 'season': 'all', 'formality': 'business'},
                {'itemId': 'pants_001', 'category': 'pants', 'color': '黒', 'season': 'all', 'formality': 'business'},
                {'itemId': 'outer_001', 'category': 'outer', 'color': 'ネイビー', 'season': 'winter', 'formality': 'casual'}
            ]
            for item in test_items:
                item['timestamp'] = datetime.now().isoformat()
                table.put_item(Item=item)
            items = test_items
        
        # DBデータでコーデ提案
        recommendation = get_coordinate_from_db(items)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'dbItems': items,
                'clothing_data': items,
                'count': len(items),
                'recommendation': recommendation
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False)
        }

def get_coordinate_from_db(items):
    """DBデータからコーデ提案"""
    try:
        items_text = '\n'.join([
            f"- {item.get('itemId', item.get('itemName', 'unknown'))}: "
            f"{item.get('category', 'unknown')}, "
            f"{item.get('color', 'unknown')}, "
            f"{item.get('season', item.get('warmth', 'all'))}, "
            f"{item.get('formality', item.get('style', 'casual'))}"
            for item in items
        ])
        
        prompt = f"""以下の服アイテムから、今日のおすすめコーディネートを提案してください:

利用可能なアイテム:
{items_text}

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
