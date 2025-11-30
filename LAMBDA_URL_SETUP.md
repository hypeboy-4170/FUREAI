# Lambda関数URL発行手順

## 関数名

```
fureai-coordinate-recommender
```

## URL発行手順

### 1. Lambda関数作成後
1. Lambda コンソールで関数を選択
2. 「設定」タブ → 「関数URL」
3. 「関数URLを作成」をクリック

### 2. 設定
- **認証タイプ**: NONE（認証なし）
- **CORS設定**: 有効化
  - Allow origin: `*`
  - Allow methods: `POST`
  - Allow headers: `*`

### 3. 保存
- 「保存」をクリック
- 関数URLが発行される（例: `https://xxxxx.lambda-url.ap-northeast-1.on.aws/`）

## 環境変数設定

Lambda関数の「設定」→「環境変数」で以下を設定:

```
CLOTHING_TABLE=ClothingItems
BEDROCK_MODEL_ID=jp.anthropic.claude-sonnet-4-5-20250929-v1:0
BEDROCK_REGION=ap-northeast-1
```

## テスト方法

```bash
curl -X POST https://xxxxx.lambda-url.ap-northeast-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "schedule": "会社でプレゼン",
    "weather": "15度 曇り"
  }'
```
