# FUREAI システムアーキテクチャ

## システム構成

### Lambda関数

| Lambda関数 | 責務 | トリガー | 状態 |
|-----------|------|---------|------|
| **bedrock_tester** | Bedrock疎通確認 | Lambda Function URL | ✅ 実装済み |
| **db_tester** | DB疎通テスト | Lambda Function URL | 📝 設計のみ |
| **s3_tester** | S3疎通テスト | Lambda Function URL | 📝 設計のみ |
| **weather_api_fetcher** | 天気API連携 | Lambda Function URL | 📝 設計のみ |
| **calendar_fetcher** | カレンダー連携 | Lambda Function URL | 📝 設計のみ |
| **coordinate_recommender** | コーディネート提案 | Lambda Function URL | 📝 設計のみ |
| **full_coordinator** | 全体統合 | Lambda Function URL | 📝 設計のみ |

### データフロー

```
Web UI (index.html)
  ↓
  ├→ bedrock_tester (Lambda Function URL) ✅
  │   └→ Bedrock (Claude Sonnet 4.5)
  │
  ├→ db_tester (Lambda Function URL) 📝
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  ├→ s3_tester (Lambda Function URL) 📝
  │   ├→ S3 (画像アップロード)
  │   ├→ Bedrock (画像分析)
  │   ├→ DynamoDB (登録)
  │   └→ Bedrock (コーディネート提案)
  │
  ├→ weather_api_fetcher (Lambda Function URL) 📝
  │   └→ OpenWeatherMap API
  │
  ├→ calendar_fetcher (Lambda Function URL) 📝
  │   └→ Google Calendar API
  │
  ├→ coordinate_recommender (Lambda Function URL) 📝
  │   ├→ DynamoDB (ClothingItems)
  │   └→ Bedrock (コーディネート提案)
  │
  └→ full_coordinator (Lambda Function URL) 📝
      ├→ S3 + DynamoDB + 天気 + 予定
      └→ Bedrock (統合提案)
```



---

## アーキテクチャの特徴

### 1. API Gateway不要
- **Lambda Function URL**を使用
- 各Lambda関数に直接HTTPSアクセス
- CORS設定はLambda Function URLで設定
- コスト削減（API Gateway料金不要）

### 2. 段階的実装
- ✅ **bedrock_tester**: Bedrock疎通確認（実装済み）
- 📝 **その他の関数**: 設計済み、順次実装予定

### 3. シンプルな構成
- Lambda関数は最小限の責務
- 各関数は独立してテスト可能
- Web UIから直接Lambda Function URLを呼び出し



---

## セットアップ手順

### 1. Lambda関数作成

1. AWSコンソール → Lambda → 「関数の作成」
2. 関数名: `fureai-bedrock-tester`
3. ランタイム: Python 3.12
4. コードをデプロイ
5. タイムアウト: 30秒に変更
6. 環境変数設定: `MODEL_ID`
7. IAMポリシーをアタッチ

詳細は `docs/LAMBDA_SETUP.md` を参照

### 2. Lambda Function URL設定

1. 「設定」→「関数URL」→「関数URLを作成」
2. 認証タイプ: NONE
3. CORS: 有効化
   - Allow origin: `*`
   - Allow methods: `POST`
   - Allow headers: `content-type`
   - Max age: `300`

### 3. Web UIにURL設定

`web/config.js`にLambda Function URLを設定:
```javascript
window.LAMBDA_URLS = {
    bedrock: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/'
};
```

### 4. テスト実行

1. `web/index.html`をブラウザで開く
2. 質問を入力
3. 「Bedrockテスト」ボタンをクリック
4. AIの応答を確認

---

## まとめ

### 現在の構成

```
HTML UI → Lambda Function URL → bedrock_tester → Bedrock
```

### 実装状況

- ✅ **bedrock_tester**: 実装済み
- 📝 **その他6関数**: 設計済み、順次実装予定

### コスト見積もり（月間100回実行）

| サービス | 料金 |
|---------|------|
| Lambda | $0.44 |
| Bedrock | $0.45 |
| **合計** | **$0.89** |

※ 無料利用枠内であれば実質無料
