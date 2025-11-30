import json
import boto3
import os

bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
MODEL_ID = os.environ.get('MODEL_ID', 'jp.anthropic.claude-sonnet-4-5-20250929-v1:0')

def lambda_handler(event, context):
    """
    Bedrock単体の疎通確認用Lambda関数
    DynamoDB不要、Bedrockのみテスト
    """
    try:
        # Lambda関数URLからの呼び出しに対応
        if isinstance(event.get('body'), str):
            body = json.loads(event.get('body', '{}'))
        else:
            body = event
        
        question = body.get('question', '')
        
        if not question:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'question is required'})
            }
        
        # Bedrockに質問を送信（JP Claude Sonnet 4.5 推論プロファイル）
        bedrock_response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": question
                }]
            })
        )
        
        response_body = json.loads(bedrock_response['body'].read())
        answer = response_body['content'][0]['text']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'answer': answer
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'traceback': traceback.format_exc()
            })
        }
