# DynamoDB設計

## テーブル構成

### ClothingItems（衣類マスタ）

| 属性名 | 型 | キー | 説明 | 例 |
|--------|-----|------|------|-----|
| itemId | String | PK | 衣類ID | "tops_001" |
| imageKey | String | - | S3画像パス | "uploads/tops_001.jpg" |
| itemName | String | - | 衣類名 | "茶シャツ" |
| category | String | - | カテゴリ | "tops" / "pants" / "outer" |
| color | String | - | 色 | "brown" / "black" / "beige" |
| style | String | - | スタイル | "formal" / "casual" / "business_casual" |
| season | List | - | 適した季節 | ["spring", "summer", "autumn"] |
| warmth | String | - | 暖かさ | "warm" / "cool" |

### WearHistory（着用履歴）

| 属性名 | 型 | キー | 説明 | 例 |
|--------|-----|------|------|-----|
| itemId | String | PK | 衣類ID | "tops_001" |
| wornDate | String | SK | 着用日 | "2025-01-20" |

## データ例

### ClothingItems

```json
{
  "itemId": "tops_001",
  "imageKey": "uploads/tops_001.jpg",
  "itemName": "茶シャツ",
  "category": "tops",
  "color": "brown",
  "style": "formal",
  "season": ["spring", "summer", "autumn"],
  "warmth": "cool"
}
```

### WearHistory

```json
{
  "itemId": "tops_001",
  "wornDate": "2025-01-20"
}
```

## アクセスパターン

### 1. 全衣類取得
```python
dynamodb.scan(TableName='ClothingItems')
```

### 2. カテゴリ別取得（GSI必要）
```python
# 将来的にGSI追加を検討
dynamodb.query(
    TableName='ClothingItems',
    IndexName='category-index',
    KeyConditionExpression='category = :cat'
)
```

### 3. 着用履歴取得
```python
dynamodb.query(
    TableName='WearHistory',
    KeyConditionExpression='itemId = :id AND wornDate > :date'
)
```

## 課金モード

**PAY_PER_REQUEST（オンデマンド）**

- 理由: アクセス頻度が低い
- コスト: 読み取り$0.25/100万、書き込み$1.25/100万
