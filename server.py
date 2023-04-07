from http.server import BaseHTTPRequestHandler, HTTPServer
from config import download_serv
import json
import youtube_dl
import uuid

class DownloadServ(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == download_serv['path']:
            if self.headers.get('content-type') != 'application/json':
                self.respond(400, 'error', 'Content type must be application/json')

            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except ValueError:
                self.respond(400, 'error', 'Invalid JSON data')

            if set(data.keys()) == {'url', 'options'}:
                self.handleOptions(data)
            else:
                self.respond(400, 'error', 'Request body does not include expected values')
        else:
            self.respond(404, 'error', f'Unknown path: {self.path}')

    def handleOptions(self, data):
        url = data['url']
        options = data['options']
        format = options['convertFormat']

        file_uuid = str(uuid.uuid4())
        path = f'{download_serv["download_path"]}{file_uuid}.{format}'

        ydl_opts = {
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format
            }],
            'outtmpl': path,
            'noplaylist': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return_value = {
            'path': path,
            'format': format,
            'media': 'audio' if format == 'mp3' else 'video'
        }
        self.respond(200, 'success', return_value)

    def respond(self, status_code, status, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        response = {'status': status, 'message': message}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', download_serv['access_control_allow_origin'])
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        super().end_headers()


def run(server_class=HTTPServer, handler_class=DownloadServ, port=download_serv['port']):
    server_address = (download_serv['host'], download_serv['port'])
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    print('Started server on port %d' % port)

if __name__ == '__main__':
    run()
