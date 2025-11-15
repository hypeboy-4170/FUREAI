"""
Alexa音声インターフェーステスト
- モック: テキスト入力でAlexaスキルをシミュレート
- 本番: 実際のAlexaスキル連携テスト
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_alexa_mock():
    print("=" * 50)
    print("🎤 Alexa モックシミュレーター")
    print("=" * 50)
    print("\n使い方: 「服ちょうだい」と入力してください")
    print("終了: 'exit' と入力\n")
    
    while True:
        user_input = input("あなた: ").strip()
        
        if user_input.lower() == 'exit':
            print("👋 終了します")
            break
        
        # Alexaスキルのインテント判定
        if '服' in user_input or 'コーデ' in user_input or 'outfit' in user_input.lower():
            print("\n🤖 Alexa: 承知しました。最適なコーディネートを提案します...")
            
            # Lambda呼び出しをシミュレート
            event = {
                "intent": "GetOutfit",
                "userId": "user_test_001",
                "timestamp": "2025-11-10T18:00:00Z"
            }
            
            print(f"\n📤 Lambda に送信:")
            print(f"  Intent: {event['intent']}")
            print(f"  User ID: {event['userId']}")
            
            # モック応答
            print(f"\n📥 Lambda からの応答:")
            print(f"  今日は晴れで26度です。")
            print(f"  午後に会議があるため、白いシャツとグレーのパンツをおすすめします。")
            print(f"  引き出し3番と7番から取り出してください。\n")
        else:
            print("\n🤖 Alexa: すみません、理解できませんでした。「服ちょうだい」と言ってください。\n")

def test_alexa_production():
    """
    本番Alexaスキルテスト
    実際のAlexa Developer Consoleでテスト
    """
    print("=" * 50)
    print("🎤 Alexa 本番スキルテスト")
    print("=" * 50)
    print("\n手順:")
    print("1. Alexa Developer Console にアクセス")
    print("2. スキルをテストタブで開く")
    print("3. '服ちょうだい' と音声入力")
    print("4. Lambda関数が正常に呼び出されることを確認")
    print("\n期待される応答:")
    print("- 天気情報の取得")
    print("- 予定情報の確認")
    print("- AI によるコーデ提案")
    print("- 音声での回答")

if __name__ == '__main__':
    print("テストモードを選択してください:")
    print("1. モックテスト (テキスト入力)")
    print("2. 本番テスト (Alexa連携)")
    
    choice = input("選択 (1/2): ").strip()
    
    if choice == '1':
        test_alexa_mock()
    elif choice == '2':
        test_alexa_production()
    else:
        print("無効な選択です")
