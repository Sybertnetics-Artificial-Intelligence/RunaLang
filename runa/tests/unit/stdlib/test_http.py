import unittest
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from runa.stdlib.http import (
    http_get, http_post, parse_url, parse_query_string, build_url, HTTPError
)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'hello world')
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'got: ' + post_data)
    def log_message(self, format, *args):
        pass  # Silence server logs

def run_server(server):
    server.serve_forever()

class TestHttpModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), SimpleHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=run_server, args=(cls.server,), daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def test_http_get(self):
        url = f'http://127.0.0.1:{self.port}/'
        resp = http_get(url)
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.body, b'hello world')
        self.assertIn('Content-type', resp.headers)

    def test_http_post(self):
        url = f'http://127.0.0.1:{self.port}/'
        resp = http_post(url, data=b'foo=bar')
        self.assertEqual(resp.status, 200)
        self.assertTrue(resp.body.startswith(b'got: '))

    def test_parse_url(self):
        url = 'http://user:pass@host:8080/path?x=1&y=2#frag'
        parsed = parse_url(url)
        self.assertEqual(parsed['scheme'], 'http')
        self.assertEqual(parsed['hostname'], 'host')
        self.assertEqual(parsed['port'], 8080)
        self.assertEqual(parsed['username'], 'user')
        self.assertEqual(parsed['password'], 'pass')
        self.assertEqual(parsed['path'], '/path')
        self.assertEqual(parsed['query'], 'x=1&y=2')
        self.assertEqual(parsed['fragment'], 'frag')

    def test_parse_query_string(self):
        qs = 'a=1&b=2&b=3'
        parsed = parse_query_string(qs)
        self.assertEqual(parsed['a'], ['1'])
        self.assertEqual(parsed['b'], ['2', '3'])

    def test_build_url(self):
        url = build_url(scheme='https', hostname='foo.com', path='/bar', query='x=1')
        self.assertTrue(url.startswith('https://foo.com/bar'))
        self.assertIn('x=1', url)

    def test_http_error(self):
        with self.assertRaises(HTTPError):
            http_get('http://127.0.0.1:9999/')

if __name__ == '__main__':
    unittest.main() 