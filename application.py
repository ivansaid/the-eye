from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPResponse
from os import curdir, sep


# Create a index.html aside the code
# Run: python server.py
# After run, try http://localhost:8080/

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/the-eye':
            request_handler(self)

        else:
            self.send_error(404, 'File not found!')
            self.end_headers()


def request_handler(self):
    self.send_response(200)
    self.end_headers()


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
    run()
