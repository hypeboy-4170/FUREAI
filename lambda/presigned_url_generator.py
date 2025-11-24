import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'fureai-clothing-images')

def lambda_handler(event, context):
    """
    Presigned URLを生成してHTMLから直接S3にアップロードできるようにする
    """
    try:
        # イベントボディをパース
        body = json.loads(event.get('body', '{}'))
        
        # Presigned URL生成リクエストの場合
        if body.get('action') == 'getPresignedUrl':
            item_id = body.get('itemId')
            file_type = body.get('fileType', 'image/jpeg')
            
            if not item_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'itemId is required'})
                }
            
            # S3キーを生成（拡張子は.jpgに統一）
            s3_key = f"uploads/{item_id}.jpg"
            
            # Presigned URLを生成（15分間有効）
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': s3_key,
                    'ContentType': file_type
                },
                ExpiresIn=900  # 15分
            )
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'uploadUrl': presigned_url,
                    's3Key': s3_key,
                    'bucket': BUCKET_NAME
                })
            }
        
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid action'})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
