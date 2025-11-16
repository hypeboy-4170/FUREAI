# FUREAI テスト手順

## ⚠️ 重要: SCP制限について

組織のService Control Policy (SCP)により、CLI/SDKからのLambda実行が制限されています。

**制限される操作**:

- `lambda:CreateFunction` (CLI/SDK)
- `lambda:InvokeFunction` (CLI/SDK)

**利用可能な方法**:

- ✅ AWS Console (ブラウザ)
- ✅ Alexa Developer Console
- ❌ AWS CLI
- ❌ boto3 (Python SDK)

---

## テストダッシュボード起動

```bash
cd tests
python server.py
```

ブラウザで <http://localhost:8000/test.html> を開く

**注意**: ボタン1, 2はSCP制限によりエラーになります。Console経由でテストしてください。

---

## 各テスト詳細

### 1. Lambda関数テスト (AWS Console)

**目的**: Lambda関数が正常に動作するか確認

**手順**:

1. [Lambda Console](https://console.aws.amazon.com/lambda) を開く
2. `FureaiAlexaSkill` を選択
3. 「テスト」タブをクリック
4. 「新しいイベントを作成」:
   - イベント名: `AlexaTest`
   - テンプレート: `alexa-skills-kit-intent-request`
   - または `tests/alexa_test_event.json` の内容をコピー
5. 「テスト」ボタンをクリック
6. 実行結果を確認

**期待結果**:

```json
{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "こんにちは！GetOutfitIntentを受け取りました。Lambda関数が正常に動作しています。"
    },
    "shouldEndSession": true
  }
}
```

---

### 2. Alexa⇒Lambda統合テスト (Alexa Console)

**目的**: AlexaスキルからLambda呼び出しが正常に動作するか確認

**手順**:

1. [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) を開く
2. FUREAIスキルを選択
3. 「Test」タブ → Development環境に切り替え
4. テキスト入力: `今日のこーでえらんで`
5. JSON Outputでレスポンス確認

**期待結果**: Lambda ARNが呼び出され、応答が返る

---

### 3. Bedrock基本テスト

**目的**: Bedrock AIがコーデ提案を生成できるか確認

**手順**: ダッシュボードの「2. Bedrock基本テスト」ボタンをクリック

**注意**: Bedrock権限がない場合はモックデータが返ります

**期待結果**: JSON形式でコーデ提案が返る

```json
{
  "items": [1, 2],
  "explanation": "白シャツとグレーパンツの組み合わせは清潔感があり..."
}
```

---

### 4. 天気API検証

**目的**: OpenWeatherMap APIで天気情報を取得できるか確認

**料金**: 無料プラン (1,000回/日まで)

**手順**:

1. [OpenWeatherMap API](https://openweathermap.org/api) を開く
2. アカウント作成（無料）
3. API Keys → Create Key
4. `.env`に`OPENWEATHER_API_KEY`を設定

**期待結果**: 東京の現在の天気情報が返る

---

### 5. 予定API検証

**目的**: Google Calendar APIで予定情報を取得できるか確認

**料金**: 無料 (クォータ: 1,000,000リクエスト/日)

**手順**:

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成
2. Google Calendar API有効化
3. OAuth 2.0認証情報作成
4. `.env`に`GOOGLE_CALENDAR_CREDENTIALS`を設定

**期待結果**: 今日の予定リストが返る

---

### 6. 統合テスト（全データ）

**目的**: DynamoDB + S3 + 天気 + 予定 → Bedrock提案の全フロー確認

**手順**: ダッシュボードの「5. 統合テスト」ボタンをクリック

**期待結果**: 全データを加味したコーデ提案が返る

```json
{
  "weather": {"condition": "晴れ", "temp": 26},
  "schedule": {"meeting": true, "time": "14:00"},
  "clothes": [...],
  "recommendation": {
    "items": [1, 2],
    "explanation": "晴れで会議があるため..."
  }
}
```

---

## トラブルシューティング

### Lambda実行エラー (Console)

Lambda Console → CloudWatch Logs で確認:

```
/aws/lambda/FureaiAlexaSkill
```

### CLI/SDKでAccessDenied

```
AccessDeniedException: explicit deny in a service control policy
```

**原因**: 組織のSCPでLambda実行が制限

**対処**: AWS ConsoleまたはAlexa Consoleから実行

### Bedrock接続エラー

- リージョン確認: `us-east-1`
- モデルID確認: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- IAMロール権限確認

### 外部API接続エラー

- APIキーの有効期限確認
- レート制限確認
- `.env`ファイルの設定確認
