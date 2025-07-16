import unittest
import socket
from runa.stdlib.net import (
    create_tcp_server, create_tcp_client, create_udp_server, create_udp_client,
    resolve_hostname, get_local_ip, is_port_open, NetError
)

class TestNetModule(unittest.TestCase):
    def test_resolve_hostname(self):
        ip = resolve_hostname('localhost')
        self.assertTrue(isinstance(ip, str))
        self.assertIn(ip, ['127.0.0.1', '::1'])

    def test_get_local_ip(self):
        ip = get_local_ip()
        self.assertTrue(isinstance(ip, str))
        self.assertRegex(ip, r'^\d+\.\d+\.\d+\.\d+$')

    def test_is_port_open_false(self):
        # Pick a high port unlikely to be open
        self.assertFalse(is_port_open('127.0.0.1', 54321))

    def test_is_port_open_true(self):
        # Open a socket, check port is open, then close
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        s.listen(1)
        port = s.getsockname()[1]
        try:
            self.assertTrue(is_port_open('127.0.0.1', port))
        finally:
            s.close()

    def test_create_tcp_server_and_client(self):
        # Start a server, connect with client, send/receive data
        server = create_tcp_server('127.0.0.1', 0)
        port = server.getsockname()[1]
        client = create_tcp_client('127.0.0.1', port)
        conn, addr = server.accept()
        try:
            client.sendall(b'hello')
            data = conn.recv(1024)
            self.assertEqual(data, b'hello')
            conn.sendall(b'world')
            data2 = client.recv(1024)
            self.assertEqual(data2, b'world')
        finally:
            client.close()
            conn.close()
            server.close()

    def test_create_udp_server_and_client(self):
        server = create_udp_server('127.0.0.1', 0)
        port = server.getsockname()[1]
        client = create_udp_client()
        try:
            client.sendto(b'ping', ('127.0.0.1', port))
            data, addr = server.recvfrom(1024)
            self.assertEqual(data, b'ping')
            server.sendto(b'pong', addr)
            data2, addr2 = client.recvfrom(1024)
            self.assertEqual(data2, b'pong')
        finally:
            client.close()
            server.close()

    def test_resolve_hostname_error(self):
        with self.assertRaises(NetError):
            resolve_hostname('nonexistent.invalid')

    def test_create_tcp_client_error(self):
        # Try to connect to a port that is not open
        with self.assertRaises(NetError):
            create_tcp_client('127.0.0.1', 54321)

if __name__ == '__main__':
    unittest.main() 