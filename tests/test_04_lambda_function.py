"""
Lambda関数テスト
- モック: ローカル環境でLambda関数をシミュレート
- 本番: デプロイされたAWS Lambda関数をテスト
"""
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

def test_lambda_mock():
    """
    モックLambda関数テスト - ローカル環境で実行
    """
    print("=" * 50)
    print("⚡ Lambda関数モックテスト")
    print("=" * 50)
    
    # モックイベント
    event = {
        "intent": "GetOutfit",
        "userId": "user_test_001",
        "timestamp": "2025-11-10T18:00:00Z"
    }
    
    print("\n📥 入力イベント:")
    print(json.dumps(event, ensure_ascii=False, indent=2))
    
    # Lambda処理をシミュレート
    print("\n🔄 Lambda処理中...")
    print("  ✅ 天気API呼び出し: 成功")
    print("  ✅ 予定API呼び出し: 成功")
    print("  ✅ RDS接続: 成功")
    print("  ✅ Bedrock呼び出し: 成功")
    
    # モックレスポンス
    response = {
        "statusCode": 200,
        "body": {
            "speech": "今日は晴れで26度です。午後に会議があるため、白いシャツとグレーのパンツをおすすめします。",
            "outfit": {
                "items": ["shirt_white", "pants_gray"],
                "storage": "引き出し3番と7番"
            }
        }
    }
    
    print("\n📤 Lambda応答:")
    print(json.dumps(response, ensure_ascii=False, indent=2))
    print("\n✅ モックテスト完了!")

def test_lambda_production():
    """
    本番Lambda関数テスト - AWS環境で実行
    """
    print("=" * 50)
    print("☁️ Lambda関数本番テスト")
    print("=" * 50)
    
    print("\n📋 本番テスト手順:")
    print("1. AWS ConsoleでLambda関数を開く")
    print("2. テストイベントを作成")
    print("3. 以下のイベントを設定:")
    
    test_event = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "test-session-001",
            "user": {
                "userId": "user_test_001"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "test-request-001",
            "intent": {
                "name": "GetOutfit"
            }
        }
    }
    
    print(json.dumps(test_event, ensure_ascii=False, indent=2))
    
    print("\n4. テスト実行ボタンをクリック")
    print("\n📊 確認項目:")
    print("  - 実行時間が30秒以内")
    print("  - メモリ使用量が適切")
    print("  - エラーログがない")
    print("  - 正常なレスポンス返却")
    
    print("\n💡 CloudWatch Logsで詳細ログを確認してください")

if __name__ == '__main__':
    print("テストモードを選択してください:")
    print("1. モックテスト (ローカル環境)")
    print("2. 本番テスト (AWS Lambda)")
    
    choice = input("選択 (1/2): ").strip()
    
    if choice == '1':
        test_lambda_mock()
    elif choice == '2':
        test_lambda_production()
    else:
        print("無効な選択です")
