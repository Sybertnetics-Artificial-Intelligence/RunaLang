"""
Runa Standard Library - Network Module

Provides network operations for Runa programs.
"""

import urllib.request
import urllib.parse
import urllib.error
import json as py_json
import socket
import http.client

def send_http_request(url, method="GET", data=None, headers=None):
    """Send an HTTP request to a URL."""
    try:
        if headers is None:
            headers = {}
        
        # Convert data to bytes if needed
        if data and isinstance(data, str):
            data = data.encode('utf-8')
        
        # Create request
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        # Send request and get response
        with urllib.request.urlopen(request) as response:
            return {
                'status_code': response.getcode(),
                'headers': dict(response.headers),
                'content': response.read().decode('utf-8')
            }
    except urllib.error.HTTPError as e:
        return {
            'status_code': e.code,
            'headers': dict(e.headers),
            'content': e.read().decode('utf-8') if e.fp else None,
            'error': str(e)
        }
    except Exception as e:
        return {
            'status_code': None,
            'headers': {},
            'content': None,
            'error': str(e)
        }

def get_from_url(url, headers=None):
    """Send a GET request to a URL."""
    return send_http_request(url, "GET", headers=headers)

def post_to_url(url, data=None, headers=None):
    """Send a POST request to a URL."""
    return send_http_request(url, "POST", data=data, headers=headers)

def put_to_url(url, data=None, headers=None):
    """Send a PUT request to a URL."""
    return send_http_request(url, "PUT", data=data, headers=headers)

def delete_from_url(url, headers=None):
    """Send a DELETE request to a URL."""
    return send_http_request(url, "DELETE", headers=headers)

def download_file(url, file_path):
    """Download a file from a URL to a local path."""
    try:
        urllib.request.urlretrieve(url, file_path)
        return True
    except Exception as e:
        raise Exception(f"Error downloading file: {e}")

def encode_url_parameters(params):
    """Encode dictionary parameters for URL."""
    return urllib.parse.urlencode(params)

def parse_url(url):
    """Parse a URL into its components."""
    parsed = urllib.parse.urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': parsed.query,
        'fragment': parsed.fragment
    }

def build_url(base_url, path=None, params=None):
    """Build a URL from components."""
    if path:
        if not base_url.endswith('/') and not path.startswith('/'):
            base_url += '/'
        base_url += path
    
    if params:
        query_string = encode_url_parameters(params)
        separator = '&' if '?' in base_url else '?'
        base_url += separator + query_string
    
    return base_url

def send_json_request(url, data=None, method="POST", headers=None):
    """Send a JSON request to a URL."""
    if headers is None:
        headers = {}
    
    headers['Content-Type'] = 'application/json'
    
    json_data = py_json.dumps(data) if data else None
    response = send_http_request(url, method, json_data, headers)
    
    # Try to parse response as JSON
    if response.get('content'):
        try:
            response['json'] = py_json.loads(response['content'])
        except py_json.JSONDecodeError:
            response['json'] = None
    
    return response

def get_local_ip_address():
    """Get the local IP address of the machine."""
    try:
        # Connect to a dummy address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def check_port_open(host, port, timeout=5):
    """Check if a port is open on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def get_hostname():
    """Get the hostname of the current machine."""
    return socket.gethostname()

def resolve_hostname(hostname):
    """Resolve a hostname to an IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        raise Exception(f"Could not resolve hostname: {e}")

def ping_host(host, timeout=5):
    """Simple ping check by attempting to connect."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, 80))
            return result == 0
    except Exception:
        return False

def create_server_socket(host="localhost", port=8080):
    """Create a basic server socket."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return server_socket
    except Exception as e:
        raise Exception(f"Error creating server socket: {e}")

def create_client_socket():
    """Create a basic client socket."""
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as e:
        raise Exception(f"Error creating client socket: {e}")

# Runa-style function names for natural language calling
make_http_request = send_http_request
fetch_from_url = get_from_url
send_data_to_url = post_to_url
update_at_url = put_to_url
remove_from_url = delete_from_url
download_file_from_url = download_file
prepare_url_parameters = encode_url_parameters
break_down_url = parse_url
construct_url = build_url
send_json_to_url = send_json_request
get_my_ip_address = get_local_ip_address
check_if_port_is_open = check_port_open
get_computer_name = get_hostname
find_ip_for_hostname = resolve_hostname
test_connection_to_host = ping_host
start_server_on_port = create_server_socket
connect_to_server = create_client_socket