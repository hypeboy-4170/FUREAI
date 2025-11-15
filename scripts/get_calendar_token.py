"""
Googleカレンダー アクセストークン取得スクリプト
"""
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_token():
    # credentials.jsonをダウンロードしてこのディレクトリに配置
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    
    creds = flow.run_local_server(port=8080)
    
    print("\n✅ トークン取得成功!")
    print(f"\nアクセストークン:\n{creds.token}")
    print(f"\nリフレッシュトークン:\n{creds.refresh_token}")
    
    # .envに追加
    with open('../.env', 'a') as f:
        f.write(f"\nGOOGLE_CALENDAR_TOKEN={creds.token}\n")
        f.write(f"GOOGLE_CALENDAR_REFRESH_TOKEN={creds.refresh_token}\n")
    
    print("\n.envに保存しました")

if __name__ == '__main__':
    get_token()
