# Web UIテスト手順

## 事前準備

### 1. Lambda関数URLの設定

`web/config.js` を編集してLambda関数URLを設定:

```javascript
window.LAMBDA_URLS = {
    bedrock: 'https://xxxxx.lambda-url.ap-northeast-1.on.aws/',
    // 他の関数も実装後に追加
};
```

### 2. index.htmlを開く

ブラウザで `web/index.html` を直接開く（サーバー不要）

---

## テスト方法

### ✅ 1. Bedrockテスト（実装済み）

**目的**: Bedrock API疎通確認

**手順**:
1. テキストエリアに質問を入力（例: `こんにちは`）
2. 「Bedrockテスト」ボタンをクリック
3. AIの応答が表示されることを確認

**期待結果**:
```
✅ Bedrock疎通成功

質問: こんにちは

回答:
こんにちは！何かお手伝いできることはありますか？
```

**エラー時の確認**:
- F12 → Console タブでエラー内容を確認
- Lambda関数のCloudWatch Logsを確認

---

### 📝 2. DBテスト（未実装）

**目的**: DynamoDBデータでコーディネート提案

**手順**:
1. 「DBテスト」ボタンをクリック
2. DBアイテム一覧とAIコーデ提案が表示される

**期待結果**:
```
✅ DBテスト成功

💾 DBアイテム (7件):
tops_001: tops / 白 / all / business
pants_001: pants / 黒 / all / business
...

🤖 AIコーデ提案:
白シャツと黒パンツの組み合わせがおすすめです
```

---

### 📝 3. S3テスト（未実装）

**目的**: 画像アップロード→Bedrock分析→DB登録→コーデ提案

**手順**:
1. 「ファイルを選択」で画像を選択
2. 「S3テスト（全工程）」ボタンをクリック
3. 4つの工程が順次実行される

**期待結果**:
```
✅ S3テスト成功（全工程完了）

📦 1. S3アップロード
fureai-clothing-images / uploads/item_001.jpg

🔍 2. Bedrock画像分析
カテゴリ: tops
色: 白
季節: all
フォーマル度: business

💾 3. DynamoDB登録
itemId: item_001

🤖 4. AIコーデ提案:
白シャツを使ったコーディネート提案...
```

---

### 📝 4. 天気テスト（未実装）

**目的**: OpenWeatherMap API疎通確認

**手順**:
1. 場所を入力（例: `Tokyo`）
2. 「天気テスト」ボタンをクリック
3. 天気情報が表示される

**期待結果**:
```
✅ 天気API疎通成功

場所: Tokyo
気温: 20度
天候: 曇り
湿度: 60%
```

---

### 📝 5. 予定テスト（未実装）

**目的**: Googleカレンダー疎通確認

**手順**:
1. 「予定テスト」ボタンをクリック
2. 本日の予定が表示される

**期待結果**:
```
✅ 予定API疎通成功

本日の予定:
10:00: 会議
14:00: プレゼン
```

---

### 📝 6. 全体テスト（未実装）

**目的**: S3 + DB + 天気 + 予定 → Bedrock → 統合提案

**手順**:
1. ユーザーIDを入力（例: `user001`）
2. 場所を入力（例: `Tokyo`）
3. 「🚀 全体テスト実行」ボタンをクリック
4. 全データを統合したコーディネート提案が表示される

**期待結果**:
```
🎉 全体統合テスト成功！

📦 S3データ
服アイテム数: 10件

💾 DBデータ
スタイル: シンプル

🌡️ 天気
Tokyo: 20度 晴れ

📅 予定
2件の予定

🤖 AIコーディネート提案
本日のおすすめコーディネート...
```

---

## トラブルシューティング

### CORS エラー

```
Access to fetch at '...' from origin 'null' has been blocked by CORS policy
```

**解決方法**:
1. Lambda関数URL → 設定 → 関数URL → 編集
2. CORS設定を確認:
   - Allow origin: `*`
   - Allow methods: `POST`
   - Allow headers: `content-type`

### 502 Bad Gateway

```
HTTP 502: Internal Server Error
```

**原因**:
- Lambda関数のタイムアウト（3秒デフォルト）
- IAM権限不足
- Bedrockモデルアクセス未有効化

**解決方法**:
1. Lambda → 設定 → 一般設定 → タイムアウト: 30秒
2. CloudWatch Logsでエラー詳細を確認
3. `docs/LAMBDA_SETUP.md` を参照

### JSON Parse エラー

```
Unexpected token 'I', "Internal S"... is not valid JSON
```

**原因**:
Lambda関数がエラーを返しているが、HTMLテキストで返している

**解決方法**:
1. ブラウザのコンソール（F12）でレスポンス内容を確認
2. CloudWatch Logsでエラー詳細を確認

---

## デバッグ方法

### ブラウザのコンソールを開く

1. F12キーを押す
2. 「Console」タブを選択
3. エラーメッセージを確認

### ネットワークタブで確認

1. F12 → 「Network」タブ
2. テストボタンをクリック
3. リクエスト/レスポンスの詳細を確認

### CloudWatch Logsで確認

1. AWSコンソール → CloudWatch
2. ログ → ロググループ
3. `/aws/lambda/fureai-bedrock-tester` を選択
4. 最新のログストリームを確認

---

## 次のステップ

1. ✅ bedrock_tester: テスト成功
2. 📝 db_tester: Lambda関数を実装
3. 📝 s3_tester: Lambda関数を実装
4. 📝 weather_api_fetcher: Lambda関数を実装
5. 📝 calendar_fetcher: Lambda関数を実装
6. 📝 coordinate_recommender: Lambda関数を実装
7. 📝 full_coordinator: Lambda関数を実装
