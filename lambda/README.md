# Lambda関数

## ファイル

### hello_world.py
Alexa疎通確認用のシンプルなLambda関数。

**機能**:
- Alexa形式イベントを受け取る
- "Hello World"メッセージを返す
- Lambda動作確認用

**デプロイ** (Windows PowerShell):
```powershell
cd lambda
Compress-Archive -Path hello_world.py -DestinationPath function.zip -Force
aws lambda update-function-code --function-name FureaiAlexaSkill --zip-file fileb://function.zip
```

**テスト**:
```bash
cd tests
python test_01_voice_interface.py
```

---

## 今後追加予定

- `handler.py` - メインハンドラー
- `bedrock_client.py` - Bedrock連携
- `dynamodb_client.py` - DynamoDB連携
- `external_api.py` - 外部API連携
