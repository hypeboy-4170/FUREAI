# FUREAI デプロイ手順

## Lambda関数デプロイ

### 1. Lambda関数作成 (AWS Console)

**CLIではエラーが出る場合、Consoleから作成:**

1. [Lambda Console](https://console.aws.amazon.com/lambda) を開く
2. 「関数の作成」クリック
3. 設定:
   - 関数名: `FureaiAlexaSkill`
   - ランタイム: Python 3.14
   - アーキテクチャ: x86_64
4. 「関数の作成」クリック
5. 作成後、コードをアップロード（次の手順）

### 2. コードアップロード

**Consoleから直接編集**

1. Lambda Console → `FureaiAlexaSkill` を開く
2. 「コード」タブ
3. `lambda_function.py` を `hello_world.py` の内容に置き換え
4. 「Deploy」クリック

### 3. Alexa権限追加

**Consoleから:**

1. Lambda Console → `FureaiAlexaSkill`
2. 「設定」タブ → 「トリガー」
3. 「トリガーを追加」 → 「Alexa Skills Kit」
4. スキルIDは空欄でOK（全てのAlexaスキルを許可）
5. 「追加」

### 4. Lambda ARN確認

```powershell
aws lambda get-function --function-name FureaiAlexaSkill --query Configuration.FunctionArn
```

このARNをAlexa Developer Consoleに設定。

---

## Alexaスキル設定

### 1. スキル作成

1. [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) を開く
2. 「スキルを作成」
3. スキル名: `FUREAI`
4. モデル: カスタム
5. ホスティング: 自分でプロビジョニング

### 2. インテント設定

**呼び出し名**: `今日のこー`

**インテント**: `FureaiAlexaSkill`

**サンプル発話**:

- えらんで

### 3. エンドポイント設定

「エンドポイント」→ AWS Lambda ARN:

```
arn:aws:lambda:ap-northeast-1:123456789012:function:FureaiAlexaSkill
```

### 4. ビルド

「ビルド」タブ → 「モデルをビルド」

---

## テスト手順

### ローカルテスト

```powershell
cd tests
python test_01_voice_interface.py
# 1 または 2 を選択
```

詳細は [TESTING.md](TESTING.md) を参照。

---

## トラブルシューティング

### Alexa接続エラー

- Lambda ARNが正しいか確認
- Alexa権限が付与されているか確認
- リージョンが一致しているか確認
