# Lambda関数実装チェックリスト

各Lambda関数を実装する際に、コードに反映させる必要がある項目をまとめています。

---

## 1. bedrock_tester ✅ 実装済み

### コードに反映済み
- ✅ Bedrock呼び出し（MODEL_ID: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`）
- ✅ 入力: `question`
- ✅ 出力: `answer`
- ✅ エラーハンドリング
- ✅ CORS対応不要（Lambda Function URLで設定）

---

## 2. db_tester 📝 未実装

### コードに反映すべき項目
- [ ] DynamoDB接続（テーブル名: `ClothingItems`）
- [ ] DynamoDB Scan実行
- [ ] Bedrock呼び出し（MODEL_ID: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`）
- [ ] 入力: なし（`{}`）
- [ ] 出力: `dbItems`, `recommendation`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
```

### 処理フロー
1. DynamoDBから全アイテム取得
2. Bedrockでコーディネート提案
3. 結果を返す

---

## 3. s3_tester 📝 未実装

### コードに反映すべき項目
- [ ] S3接続（バケット名: `fureai-clothing-images`）
- [ ] Base64画像データをデコード
- [ ] S3にアップロード（キー: `uploads/item_XXX.jpg`）
- [ ] Bedrockで画像分析
- [ ] DynamoDB登録（テーブル名: `ClothingItems`）
- [ ] Bedrockでコーディネート提案
- [ ] 入力: `imageData`
- [ ] 出力: `s3Upload`, `imageAnalysis`, `dbRegistration`, `recommendation`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
```

### 処理フロー
1. Base64画像をデコード
2. S3にアップロード
3. Bedrockで画像分析
4. DynamoDBに登録
5. Bedrockでコーディネート提案
6. 結果を返す

---

## 4. weather_api_fetcher 📝 未実装

### コードに反映すべき項目
- [ ] OpenWeatherMap API呼び出し（モック可）
- [ ] 入力: `location`
- [ ] 出力: `temp`, `condition`, `humidity`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
```

### 処理フロー（モック版）
1. locationを受け取る
2. 固定値で天気情報を返す（実装簡略化）
3. 結果を返す

### モック実装例
```python
def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    location = body.get('location', 'Tokyo')
    
    # モックデータ
    return {
        'statusCode': 200,
        'body': json.dumps({
            'temp': 20,
            'condition': '曇り',
            'humidity': 60
        }, ensure_ascii=False)
    }
```

---

## 5. calendar_fetcher 📝 未実装

### コードに反映すべき項目
- [ ] Google Calendar API呼び出し（モック可）
- [ ] 入力: なし（`{}`）
- [ ] 出力: `events`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
```

### 処理フロー（モック版）
1. 固定値で予定情報を返す（実装簡略化）
2. 結果を返す

### モック実装例
```python
def lambda_handler(event, context):
    # モックデータ
    return {
        'statusCode': 200,
        'body': json.dumps({
            'events': [
                {'time': '10:00', 'summary': '会議'},
                {'time': '14:00', 'summary': 'プレゼン'}
            ]
        }, ensure_ascii=False)
    }
```

---

## 6. coordinate_recommender 📝 未実装

### コードに反映すべき項目
- [ ] DynamoDB接続（テーブル名: `ClothingItems`）
- [ ] DynamoDB Scan実行
- [ ] Bedrock呼び出し（MODEL_ID: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`）
- [ ] 入力: `schedule`, `weather`
- [ ] 出力: `tops`, `pants`, `outer`, `overall_comment`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
```

### 処理フロー
1. DynamoDBから全アイテム取得
2. schedule, weatherを元にBedrockでコーディネート提案
3. JSON形式で結果を返す

---

## 7. full_coordinator 📝 未実装

### コードに反映すべき項目
- [ ] S3接続（バケット名: `fureai-clothing-images`）
- [ ] DynamoDB接続（テーブル名: `ClothingItems`）
- [ ] Bedrock呼び出し（MODEL_ID: `jp.anthropic.claude-sonnet-4-5-20250929-v1:0`）
- [ ] 天気情報取得（モック可）
- [ ] 予定情報取得（モック可）
- [ ] 入力: `userId`, `location`
- [ ] 出力: `data`, `recommendation`
- [ ] エラーハンドリング

### 必要なimport
```python
import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-1')
```

### 処理フロー
1. S3から画像一覧取得
2. DynamoDBから衣類データ取得
3. 天気情報取得（モック）
4. 予定情報取得（モック）
5. 全データを統合してBedrockで提案
6. 結果を返す

---

## 共通実装パターン

### Lambda Function URL対応
```python
def lambda_handler(event, context):
    # bodyを取得
    if 'body' in event and isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event
    
    # 処理...
    
    return {
        'statusCode': 200,
        'body': json.dumps(result, ensure_ascii=False)
    }
```

### エラーハンドリング
```python
try:
    # 処理...
    return {
        'statusCode': 200,
        'body': json.dumps(result, ensure_ascii=False)
    }
except Exception as e:
    return {
        'statusCode': 500,
        'body': json.dumps({'error': str(e)})
    }
```

### Bedrock呼び出し
```python
response = bedrock.invoke_model(
    modelId='jp.anthropic.claude-sonnet-4-5-20250929-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    })
)

result = json.loads(response['body'].read())
answer = result['content'][0]['text']
```

### DynamoDB Scan
```python
table = dynamodb.Table('ClothingItems')
response = table.scan()
items = response['Items']
```

---

## 実装優先順位

1. ✅ **bedrock_tester** - 実装済み
2. 📝 **db_tester** - DynamoDB + Bedrock（次に実装推奨）
3. 📝 **weather_api_fetcher** - モック実装で簡単
4. 📝 **calendar_fetcher** - モック実装で簡単
5. 📝 **coordinate_recommender** - メイン機能
6. 📝 **s3_tester** - 複雑（画像処理）
7. 📝 **full_coordinator** - 最も複雑（全統合）
