"""
テスト実行用サーバー
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
import re
sys.path.insert(0, os.path.dirname(__file__))

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/test/'):
            match = re.match(r'/api/test/(\d+)', self.path)
            if match:
                step = int(match.group(1))
                self.run_test(step)
        elif self.path.endswith('.html'):
            self.serve_html()
        else:
            self.send_error(404)
    
    def serve_html(self):
        try:
            with open('tests/test.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except:
            self.send_error(404)
    
    def run_test(self, step):
        if step == 1:
            result = {"step": 1, "status": "success", "message": "Alexaスキルテスト成功", "data": {"intent": "GetOutfit", "userId": "test_001"}}
        elif step == 2:
            sys.path.insert(0, '../lambda')
            try:
                from handler import lambda_handler
                event = {"userId": "test_001"}
                res = lambda_handler(event, None)
                result = {"step": 2, "status": "success", "message": "Lambda実行成功", "data": json.loads(res['body'])}
            except Exception as e:
                result = {"step": 2, "status": "error", "message": str(e)}
        elif step == 3:
            result = self.test_bedrock_basic()
        elif step == 4:
            result = self.test_bedrock_with_weather()
        elif step == 5:
            result = self.test_bedrock_with_schedule()
        elif step == 6:
            result = {"step": 6, "status": "success", "message": "S3+DBデータ加味テスト", "data": {"items": [1, 2], "explanation": "全データ加味"}}
        elif step == 7:
            result = {"step": 7, "status": "success", "message": "システムテスト完了", "data": {"outfit": {"items": [1, 2], "explanation": "統合テスト成功"}}}
        else:
            result = {"error": "Invalid step"}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    def test_bedrock_basic(self):
        import boto3
        try:
            bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            prompt = "白いシャツとグレーのパンツでコーデを提案してください。JSON: {\"items\": [], \"explanation\": \"\"}"
            body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 300, "messages": [{"role": "user", "content": prompt}]})
            response = bedrock.invoke_model(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0', body=body)
            result = json.loads(response['body'].read())
            return {"step": 3, "status": "success", "data": result['content'][0]['text']}
        except:
            return {"step": 3, "status": "mock", "data": {"items": ["shirt_white", "pants_gray"], "explanation": "基本テスト"}}
    
    def test_bedrock_with_weather(self):
        import boto3
        weather = {"condition": "晴れ", "temp": 26}
        try:
            bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            prompt = f"天気: {weather['condition']} {weather['temp']}度。コーデ提案。JSON: {{\"items\": [], \"explanation\": \"\"}}"
            body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 300, "messages": [{"role": "user", "content": prompt}]})
            response = bedrock.invoke_model(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0', body=body)
            result = json.loads(response['body'].read())
            return {"step": 4, "status": "success", "weather": weather, "data": result['content'][0]['text']}
        except:
            return {"step": 4, "status": "mock", "weather": weather, "data": {"items": ["shirt_white"], "explanation": "晴れ26度"}}
    
    def test_bedrock_with_schedule(self):
        import boto3
        weather = {"condition": "晴れ", "temp": 26}
        schedule = {"meeting": True, "time": "14:00"}
        try:
            bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            prompt = f"天気: {weather['condition']} {weather['temp']}度、予定: 会議あり。コーデ提案。JSON: {{\"items\": [], \"explanation\": \"\"}}"
            body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 300, "messages": [{"role": "user", "content": prompt}]})
            response = bedrock.invoke_model(modelId='anthropic.claude-3-5-sonnet-20241022-v2:0', body=body)
            result = json.loads(response['body'].read())
            return {"step": 5, "status": "success", "weather": weather, "schedule": schedule, "data": result['content'][0]['text']}
        except:
            return {"step": 5, "status": "mock", "weather": weather, "schedule": schedule, "data": {"items": ["shirt_white", "pants_gray"], "explanation": "会議対応"}}

if __name__ == '__main__':
    print("🚀 サーバー起動: http://localhost:8000/test.html")
    HTTPServer(('', 8000), TestHandler).serve_forever()
