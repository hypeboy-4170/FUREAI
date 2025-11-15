"""
Bedrock AI動作確認テスト
- モック: 固定レスポンスでAI提案をシミュレート
- 本番: 実際のAWS Bedrock Claude 3.5を呼び出し
"""
import sys
import boto3
import json

sys.stdout.reconfigure(encoding='utf-8')

def test_bedrock_mock():
    """
    モックBedrock AIテスト - 固定レスポンスを使用
    """
    print("=" * 50)
    print("🤖 Bedrock AI モックテスト")
    print("=" * 50)
    
    # モックデータ
    facts = {
        "weather": {"condition": "晴れ", "temp": 26, "temp_max": 28, "temp_min": 18},
        "schedule": {"meeting": True, "time": "14:00"},
        "clothes": [
            {"item_id": "shirt_white", "category": "shirt", "color": "white", "tags": "formal"},
            {"item_id": "pants_gray", "category": "pants", "color": "gray", "tags": "formal"}
        ]
    }
    
    print("\n📊 モックデータ:")
    print(json.dumps(facts, ensure_ascii=False, indent=2))
    
    print("\n💭 AIモック提案:")
    mock_response = {
        "items": ["shirt_white", "pants_gray"],
        "explanation": "晴れで26度、会議があるためフォーマルな白シャツとグレーのパンツを提案します。"
    }
    print(json.dumps(mock_response, ensure_ascii=False, indent=2))
    print("\n✅ モックテスト完了!")

def test_bedrock_production():
    # モックデータ
    facts = {
        "weather": {"condition": "晴れ", "temp": 26, "temp_max": 28, "temp_min": 18},
        "schedule": {"meeting": True, "time": "14:00"},
        "clothes": [
            {"item_id": "shirt_white", "category": "shirt", "color": "white", "tags": "formal"},
            {"item_id": "pants_gray", "category": "pants", "color": "gray", "tags": "formal"},
            {"item_id": "jacket_navy", "category": "jacket", "color": "navy", "tags": "formal"}
        ],
        "history": [
            {"item_id": "shirt_white", "worn_date": "2025-11-09"}
        ]
    }
    print("=" * 50)
    print("🤖 Bedrock AI 動作確認")
    print("=" * 50)
    
    # モックデータ
    facts = {
        "weather": {"condition": "晴れ", "temp": 26, "temp_max": 28, "temp_min": 18},
        "schedule": {"meeting": True, "time": "14:00"},
        "clothes": [
            {"item_id": "shirt_white", "category": "shirt", "color": "white", "tags": "formal"},
            {"item_id": "pants_gray", "category": "pants", "color": "gray", "tags": "formal"},
            {"item_id": "jacket_navy", "category": "jacket", "color": "navy", "tags": "formal"}
        ],
        "history": [
            {"item_id": "shirt_white", "worn_date": "2025-11-09"}
        ]
    }
    
    """
    本畫Bedrock APIテスト - 実際のAWS Bedrockを呼び出し
    """
    print("=" * 50)
    print("🤖 Bedrock AI 本畫テスト")
    print("=" * 50)
    
    print("\n📤 Bedrock に送信するデータ:")
    print(json.dumps(facts, ensure_ascii=False, indent=2))
    
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        prompt = f"""あなたはスタイリストAIです。以下の情報から最適なコーディネートを提案してください。

天気: {facts['weather']['condition']} {facts['weather']['temp']}度
予定: {'会議あり' if facts['schedule']['meeting'] else '予定なし'}
利用可能な服: {len(facts['clothes'])}着
昨日着た服: {facts['history'][0]['item_id'] if facts['history'] else 'なし'}

JSON形式で回答してください:
{{"items": ["item_id1", "item_id2"], "explanation": "理由"}}"""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        print("\n📡 Bedrock API 呼び出し中...")
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        answer = result['content'][0]['text']
        
        print("\n✅ Bedrock 応答成功!\n")
        print(f"📥 AI の提案:\n{answer}")
        
    except Exception as e:
        print(f"\n⚠️ Bedrock 接続エラー: {e}")
        print("\n💡 AWS設定を確認してください:")
        print("- AWS CLI設定 (aws configure)")
        print("- Bedrockモデルアクセス申請")
        print("- リージョン設定 (us-east-1)")

if __name__ == '__main__':
    print("テストモードを選択してください:")
    print("1. モックテスト (固定レスポンス)")
    print("2. 本番テスト (AWS Bedrock)")
    
    choice = input("選択 (1/2): ").strip()
    
    if choice == '1':
        test_bedrock_mock()
    elif choice == '2':
        test_bedrock_production()
    else:
        print("無効な選択です")
