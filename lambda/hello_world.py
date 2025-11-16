"""
Hello World Lambda関数
Alexa疎通確認用
"""
import json

def lambda_handler(event, context):
    """
    Lambda関数のエントリーポイント
    
    Args:
        event: Alexaまたはテストからのイベント
        context: Lambda実行コンテキスト
    
    Returns:
        Alexa形式のレスポンス
    """
    print(f"Received event: {json.dumps(event)}")
    
    # SessionEndedRequestはレスポンス不要
    if 'request' in event and event['request'].get('type') == 'SessionEndedRequest':
        return {}
    
    # IntentRequest処理
    if 'request' in event and event['request'].get('type') == 'IntentRequest':
        intent_name = event['request']['intent']['name']
        
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': f'こんにちは！{intent_name}を受け取りました。Lambda関数が正常に動作しています。'
                },
                'shouldEndSession': True
            }
        }
    
    # 通常のテストイベント
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello World from Lambda!',
            'input': event
        }, ensure_ascii=False)
    }
