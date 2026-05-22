#!/usr/bin/env python3
"""
淘宝闪购数智经营刷题 — 本地服务器
功能：静态文件服务 + 钉钉 Webhook 代理（解决浏览器 CORS 限制）
"""
import http.server
import json
import urllib.request
import urllib.error
import os
import sys
from io import BytesIO

PORT = 8000

class QuizServer(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ding-proxy':
            try:
                # 读取客户端发来的请求体
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                webhook_url = data.get('webhook', '')
                payload = data.get('payload', {})

                if not webhook_url:
                    self._send_json(400, {'ok': False, 'error': '缺少 webhook 参数'})
                    return

                # 转发到钉钉 Webhook
                req = urllib.request.Request(
                    webhook_url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    resp_body = resp.read().decode('utf-8')
                    self._send_json(200, {
                        'ok': True,
                        'status': resp.status,
                        'ding_response': resp_body
                    })
                    print(f'[OK] 钉钉发送成功 -> {resp_body}')

            except urllib.error.HTTPError as e:
                err_body = e.read().decode('utf-8') if e.fp else ''
                self._send_json(502, {'ok': False, 'error': f'钉钉服务器返回 HTTP {e.code}', 'detail': err_body})
                print(f'[ERR] 钉钉 HTTP {e.code}: {err_body}')
            except Exception as e:
                self._send_json(500, {'ok': False, 'error': str(e)})
                print(f'[ERR] 代理请求失败: {e}')
        else:
            self._send_json(404, {'ok': False, 'error': '未知路径'})

    def do_GET(self):
        # 静态文件服务
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # 简洁日志
        if args[0].startswith('GET'):
            ext = os.path.splitext(args[0].split(' ')[0])[1]
            if ext in ['.js', '.html', '.css', '.txt', '']:
                print(f'  GET {args[0].split(" ")[0]}')
        else:
            print(f'  {args[0]}')


if __name__ == '__main__':
    print(f'''
╔══════════════════════════════════════════════╗
║   淘宝闪购数智经营生态 · 基础知识刷题        ║
║   本地服务器已启动                            ║
╚══════════════════════════════════════════════╝
请在浏览器中打开：http://localhost:{PORT}
按 Ctrl+C 停止服务器
''')
    server = http.server.HTTPServer(('0.0.0.0', PORT), QuizServer)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止。')
        server.server_close()
