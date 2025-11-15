"""
天気API動作確認テスト
- モック: 固定データでAPI呼び出しをシミュレート
- 本番: 実際のOpenWeatherMap APIを呼び出し
"""
import sys
import requests
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

def test_weather_api_mock():
    """
    モック天気APIテスト - 固定データを使用
    """
    print("=" * 50)
    print("🌤️ 天気APIモックテスト")
    print("=" * 50)
    
    print("\n📊 モックデータで動作確認:")
    mock_data = {
        "condition": "晴れ",
        "temp": 26,
        "temp_max": 28,
        "temp_min": 18,
        "humidity": 65
    }
    print(f"  {mock_data}")
    
    print("\n📤 Bedrock用データ:")
    weather_for_ai = {
        "condition": mock_data["condition"],
        "temp": mock_data["temp"],
        "temp_max": mock_data["temp_max"],
        "temp_min": mock_data["temp_min"]
    }
    print(f"  {weather_for_ai}")
    print("\n✅ モックテスト完了!")

def test_weather_api_production():
    print("=" * 50)
    print("🌤️ 天気API動作確認")
    print("=" * 50)
    
    api_key = os.getenv('WEATHER_API_KEY', 'demo')
    city = 'Tokyo'
    
    print(f"\n📍 都市: {city}")
    print(f"🔑 API Key: {api_key[:10]}...\n")
    
    try:
        # OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"
        
        print("📡 API リクエスト送信中...")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ 天気情報取得成功!\n")
            print(f"  天気: {data['weather'][0]['description']}")
            print(f"  気温: {data['main']['temp']}°C")
            print(f"  最高: {data['main']['temp_max']}°C")
            print(f"  最低: {data['main']['temp_min']}°C")
            print(f"  湿度: {data['main']['humidity']}%")
            
            # Bedrock用のフォーマット
            weather_for_ai = {
                "condition": data['weather'][0]['description'],
                "temp": data['main']['temp'],
                "temp_max": data['main']['temp_max'],
                "temp_min": data['main']['temp_min']
            }
            
            print(f"\n📤 Bedrock用データ:")
            print(f"  {weather_for_ai}")
            
        else:
            print(f"\n❌ エラー: HTTP {response.status_code}")
            print("💡 .env に WEATHER_API_KEY を設定してください")
            
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        print("\n💡 モックデータで動作確認:")
        mock_data = {
            "condition": "晴れ",
            "temp": 26,
            "temp_max": 28,
            "temp_min": 18
        }
        print(f"  {mock_data}")

if __name__ == '__main__':
    print("テストモードを選択してください:")
    print("1. モックテスト (固定データ)")
    print("2. 本番テスト (OpenWeatherMap API)")
    
    choice = input("選択 (1/2): ").strip()
    
    if choice == '1':
        test_weather_api_mock()
    elif choice == '2':
        test_weather_api_production()
    else:
        print("無効な選択です")
