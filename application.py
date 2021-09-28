from http.server import BaseHTTPRequestHandler, HTTPServer
from database import LogDatabase, EyeDatabase
from threading import Thread
import json

logger = None
eye_database = None
valid_sessions = {'e2085be5-9137-4e4e-80b5-f1ffddc25423': True}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/the-eye-data':
            if self.headers.get('user', False) and self.headers.get('user') == 'admin':
                copy = eye_database.__dict__.copy()
                del copy['logger']
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(copy).encode(encoding='utf_8'))
            else:
                self.send_response(401)
                self.end_headers()


    def do_POST(self):
        if self.path == '/the-eye':
            if self.headers.get('session_id', False) and valid_sessions.get(self.headers.get('session_id')):
                logger.insert(
                    {"process": "processing request", "type": "Process", "message": "request proccess by user: " +
                                                                                    self.headers.get(
                                                                                        'session_id')})

                Thread(target=self.request_handler).start()
                self.send_response(200)
                self.end_headers()
            else:
                logger.insert(
                    {"process": "processing request", "type": "Error", "message": "unauthorized or invalid user"})
                self.send_response(401)
                self.end_headers()

        else:
            self.send_error(404, 'File not found!')
            self.end_headers()

    def request_handler(self):
        body = json.loads(self.rfile.read(int(self.headers.get('content-length', 0))))
        eye_database.insert(body)


def run():
    print('http server is starting...')
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        print('http server is running...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()


if __name__ == '__main__':
    logger = LogDatabase()
    eye_database = EyeDatabase(logger)
    run()
