# Net Module

The Net module provides comprehensive network operations including socket programming, HTTP client/server capabilities, network protocols, and advanced networking utilities.

## Overview

The Net module is designed to handle all network-related operations in Runa, from basic socket programming to advanced network infrastructure management. It supports both low-level network operations and high-level HTTP/WebSocket protocols.

## Core Features

- **Socket Programming**: TCP, UDP, Unix domain sockets
- **HTTP Client/Server**: Full HTTP protocol support
- **WebSocket Support**: Real-time bidirectional communication
- **SSL/TLS**: Secure communication with certificate management
- **Network Discovery**: Hostname resolution, interface enumeration
- **Network Monitoring**: Traffic analysis, packet capture
- **Advanced Protocols**: Multicast, broadcast, raw sockets
- **Network Infrastructure**: Load balancers, proxies, firewalls, VPNs

## Basic Usage

### Socket Operations

```runa
Note: Create a basic TCP socket and connect to a server
:End Note

Let socket be create tcp socket
Let connected be connect socket to "localhost" on port 8080

If connected is true:
    Let message be "Hello, Server!"
    Let sent be send data through socket with message
    Let response be receive data from socket with buffer size 1024
    Close socket
End If
```

### HTTP Client

```runa
Note: Make HTTP requests to web services
:End Note

Let client be create http client
Let response be http get "https://api.example.com/data"
Let status be get http response status from response
Let body be get http response body from response
```

### HTTP Server

```runa
Note: Create a simple HTTP server
:End Note

Let server be create http server on "localhost" port 3000
Let started be start http server server

If started is true:
    Note: Server is running and ready to accept connections
    Note: Add routes and handlers as needed
End If
```

## API Reference

### Socket Operations

#### `create_socket(socket_type: String) -> Dictionary[String, Any]`
Creates a new socket with the specified type.

**Parameters:**
- `socket_type`: Type of socket ("tcp", "udp", "unix")

**Returns:** Socket object

**Example:**
```runa
Let tcp_socket be create socket with type as "tcp"
Let udp_socket be create socket with type as "udp"
```

#### `create_tcp_socket() -> Dictionary[String, Any]`
Creates a new TCP socket.

**Returns:** TCP socket object

#### `create_udp_socket() -> Dictionary[String, Any]`
Creates a new UDP socket.

**Returns:** UDP socket object

#### `bind_socket(socket: Dictionary[String, Any], host: String, port: Integer) -> Boolean`
Binds a socket to a specific address and port.

**Parameters:**
- `socket`: Socket object to bind
- `host`: Host address to bind to
- `port`: Port number to bind to

**Returns:** True if binding successful, false otherwise

#### `listen_socket(socket: Dictionary[String, Any], backlog: Integer) -> Boolean`
Starts listening for incoming connections.

**Parameters:**
- `socket`: Socket to start listening on
- `backlog`: Maximum number of pending connections

**Returns:** True if listening started successfully

#### `accept_connection(socket: Dictionary[String, Any]) -> Dictionary[String, Any]`
Accepts an incoming connection.

**Parameters:**
- `socket`: Listening socket

**Returns:** New connection socket

#### `connect_socket(socket: Dictionary[String, Any], host: String, port: Integer) -> Boolean`
Connects a socket to a remote address.

**Parameters:**
- `socket`: Socket to connect
- `host`: Remote host address
- `port`: Remote port number

**Returns:** True if connection successful

#### `send_data(socket: Dictionary[String, Any], data: String) -> Integer`
Sends string data through a socket.

**Parameters:**
- `socket`: Socket to send through
- `data`: String data to send

**Returns:** Number of bytes sent

#### `send_bytes(socket: Dictionary[String, Any], data: List[Integer]) -> Integer`
Sends binary data through a socket.

**Parameters:**
- `socket`: Socket to send through
- `data`: Binary data as list of integers

**Returns:** Number of bytes sent

#### `receive_data(socket: Dictionary[String, Any], buffer_size: Integer) -> String`
Receives string data from a socket.

**Parameters:**
- `socket`: Socket to receive from
- `buffer_size`: Maximum number of bytes to receive

**Returns:** Received string data

#### `receive_bytes(socket: Dictionary[String, Any], buffer_size: Integer) -> List[Integer]`
Receives binary data from a socket.

**Parameters:**
- `socket`: Socket to receive from
- `buffer_size`: Maximum number of bytes to receive

**Returns:** Received binary data

#### `close_socket(socket: Dictionary[String, Any]) -> None`
Closes a socket connection.

**Parameters:**
- `socket`: Socket to close

#### `shutdown_socket(socket: Dictionary[String, Any], how: String) -> None`
Shuts down a socket connection.

**Parameters:**
- `socket`: Socket to shutdown
- `how`: Shutdown mode ("read", "write", "both")

### Socket Configuration

#### `set_socket_timeout(socket: Dictionary[String, Any], timeout: Number) -> Boolean`
Sets socket timeout in seconds.

#### `set_socket_reuse_address(socket: Dictionary[String, Any], reuse: Boolean) -> Boolean`
Enables/disables address reuse.

#### `set_socket_keepalive(socket: Dictionary[String, Any], keepalive: Boolean) -> Boolean`
Enables/disables keep-alive.

#### `set_socket_nodelay(socket: Dictionary[String, Any], nodelay: Boolean) -> Boolean`
Enables/disables Nagle's algorithm.

### Network Discovery

#### `resolve_hostname(hostname: String) -> List[String]`
Resolves a hostname to IP addresses.

#### `resolve_ip(ip: String) -> String`
Resolves an IP address to hostname.

#### `get_network_interfaces() -> List[Dictionary[String, Any]]`
Gets list of network interfaces.

#### `get_interface_addresses(interface: String) -> List[Dictionary[String, Any]]`
Gets addresses for a specific interface.

#### `ping_host(host: String) -> Dictionary[String, Any]`
Pings a host and returns statistics.

#### `traceroute_host(host: String) -> List[Dictionary[String, Any]]`
Performs traceroute to a host.

### HTTP Client Operations

#### `create_http_client() -> Dictionary[String, Any]`
Creates a new HTTP client.

#### `http_get(url: String) -> Dictionary[String, Any]`
Performs HTTP GET request.

#### `http_post(url: String, data: String) -> Dictionary[String, Any]`
Performs HTTP POST request.

#### `http_put(url: String, data: String) -> Dictionary[String, Any]`
Performs HTTP PUT request.

#### `http_delete(url: String) -> Dictionary[String, Any]`
Performs HTTP DELETE request.

#### `http_request(method: String, url: String, headers: Dictionary[String, String], data: String) -> Dictionary[String, Any]`
Performs custom HTTP request.

#### `set_http_headers(client: Dictionary[String, Any], headers: Dictionary[String, String]) -> None`
Sets default headers for HTTP client.

#### `set_http_timeout(client: Dictionary[String, Any], timeout: Number) -> None`
Sets timeout for HTTP client.

#### `set_http_proxy(client: Dictionary[String, Any], proxy: String) -> None`
Sets proxy for HTTP client.

#### `set_http_ssl_verify(client: Dictionary[String, Any], verify: Boolean) -> None`
Enables/disables SSL verification.

### HTTP Response Handling

#### `get_http_response_status(response: Dictionary[String, Any]) -> Integer`
Gets HTTP response status code.

#### `get_http_response_headers(response: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP response headers.

#### `get_http_response_body(response: Dictionary[String, Any]) -> String`
Gets HTTP response body.

#### `get_http_response_json(response: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets HTTP response as JSON.

### HTTP Server Operations

#### `create_http_server(host: String, port: Integer) -> Dictionary[String, Any]`
Creates a new HTTP server.

#### `start_http_server(server: Dictionary[String, Any]) -> Boolean`
Starts HTTP server.

#### `stop_http_server(server: Dictionary[String, Any]) -> None`
Stops HTTP server.

#### `add_http_route(server: Dictionary[String, Any], method: String, path: String, handler: String) -> Boolean`
Adds route handler to HTTP server.

#### `set_http_middleware(server: Dictionary[String, Any], middleware: String) -> Boolean`
Sets middleware for HTTP server.

### WebSocket Operations

#### `create_websocket_server(host: String, port: Integer) -> Dictionary[String, Any]`
Creates a new WebSocket server.

#### `start_websocket_server(server: Dictionary[String, Any]) -> Boolean`
Starts WebSocket server.

#### `stop_websocket_server(server: Dictionary[String, Any]) -> None`
Stops WebSocket server.

#### `add_websocket_handler(server: Dictionary[String, Any], path: String, handler: String) -> Boolean`
Adds WebSocket handler.

#### `websocket_send(connection: Dictionary[String, Any], message: String) -> Boolean`
Sends message through WebSocket.

#### `websocket_receive(connection: Dictionary[String, Any]) -> String`
Receives message from WebSocket.

### SSL/TLS Operations

#### `create_ssl_context(cert_file: String, key_file: String) -> Dictionary[String, Any]`
Creates SSL context with certificate and key.

#### `wrap_socket_ssl(socket: Dictionary[String, Any], ssl_context: Dictionary[String, Any]) -> Dictionary[String, Any]`
Wraps socket with SSL.

#### `create_ssl_client(host: String, port: Integer) -> Dictionary[String, Any]`
Creates SSL client.

#### `create_ssl_server(host: String, port: Integer, cert_file: String, key_file: String) -> Dictionary[String, Any]`
Creates SSL server.

#### `generate_self_signed_cert(common_name: String, output_dir: String) -> Dictionary[String, String]`
Generates self-signed certificate.

#### `validate_certificate(cert_file: String) -> Dictionary[String, Any]`
Validates certificate.

### Advanced Network Operations

#### `create_udp_multicast(group: String, port: Integer) -> Dictionary[String, Any]`
Creates UDP multicast socket.

#### `join_multicast_group(socket: Dictionary[String, Any], group: String) -> Boolean`
Joins multicast group.

#### `leave_multicast_group(socket: Dictionary[String, Any], group: String) -> Boolean`
Leaves multicast group.

#### `send_multicast(socket: Dictionary[String, Any], group: String, port: Integer, data: String) -> Integer`
Sends multicast message.

#### `receive_multicast(socket: Dictionary[String, Any], buffer_size: Integer) -> Dictionary[String, Any]`
Receives multicast message.

#### `create_broadcast_socket() -> Dictionary[String, Any]`
Creates broadcast socket.

#### `send_broadcast(socket: Dictionary[String, Any], port: Integer, data: String) -> Integer`
Sends broadcast message.

#### `receive_broadcast(socket: Dictionary[String, Any], buffer_size: Integer) -> Dictionary[String, Any]`
Receives broadcast message.

### Raw Socket Operations

#### `create_raw_socket(protocol: Integer) -> Dictionary[String, Any]`
Creates raw socket.

#### `send_raw_packet(socket: Dictionary[String, Any], packet: List[Integer]) -> Integer`
Sends raw packet.

#### `receive_raw_packet(socket: Dictionary[String, Any], buffer_size: Integer) -> List[Integer]`
Receives raw packet.

### Packet Capture and Analysis

#### `create_packet_sniffer(interface: String) -> Dictionary[String, Any]`
Creates packet sniffer.

#### `start_sniffing(sniffer: Dictionary[String, Any]) -> Boolean`
Starts packet sniffing.

#### `stop_sniffing(sniffer: Dictionary[String, Any]) -> None`
Stops packet sniffing.

#### `get_captured_packets(sniffer: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets captured packets.

#### `analyze_packet(packet: List[Integer]) -> Dictionary[String, Any]`
Analyzes network packet.

#### `create_packet_filter(filter_string: String) -> Dictionary[String, Any]`
Creates packet filter.

#### `apply_packet_filter(sniffer: Dictionary[String, Any], filter: Dictionary[String, Any]) -> Boolean`
Applies packet filter.

### Network Monitoring

#### `get_network_statistics() -> Dictionary[String, Any]`
Gets overall network statistics.

#### `get_interface_statistics(interface: String) -> Dictionary[String, Any]`
Gets interface statistics.

#### `get_connection_statistics() -> List[Dictionary[String, Any]]`
Gets connection statistics.

#### `get_protocol_statistics() -> Dictionary[String, Any]`
Gets protocol statistics.

#### `monitor_network_traffic(interface: String, duration: Number) -> Dictionary[String, Any]`
Monitors network traffic.

#### `detect_network_anomalies(traffic_data: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Detects network anomalies.

#### `create_network_monitor(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network monitor.

#### `start_network_monitoring(monitor: Dictionary[String, Any]) -> Boolean`
Starts network monitoring.

#### `stop_network_monitoring(monitor: Dictionary[String, Any]) -> None`
Stops network monitoring.

#### `get_monitoring_alerts(monitor: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets monitoring alerts.

#### `set_monitoring_threshold(monitor: Dictionary[String, Any], metric: String, threshold: Number) -> Boolean`
Sets monitoring threshold.

### Network Infrastructure

#### `create_network_load_balancer(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network load balancer.

#### `add_backend_server(balancer: Dictionary[String, Any], server: String, port: Integer) -> Boolean`
Adds backend server to load balancer.

#### `remove_backend_server(balancer: Dictionary[String, Any], server: String, port: Integer) -> Boolean`
Removes backend server from load balancer.

#### `set_load_balancing_algorithm(balancer: Dictionary[String, Any], algorithm: String) -> Boolean`
Sets load balancing algorithm.

#### `get_load_balancer_stats(balancer: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets load balancer statistics.

#### `create_network_proxy(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network proxy.

#### `start_proxy(proxy: Dictionary[String, Any]) -> Boolean`
Starts network proxy.

#### `stop_proxy(proxy: Dictionary[String, Any]) -> None`
Stops network proxy.

#### `add_proxy_rule(proxy: Dictionary[String, Any], rule: Dictionary[String, Any]) -> Boolean`
Adds proxy rule.

#### `get_proxy_statistics(proxy: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets proxy statistics.

#### `create_network_firewall(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network firewall.

#### `add_firewall_rule(firewall: Dictionary[String, Any], rule: Dictionary[String, Any]) -> Boolean`
Adds firewall rule.

#### `remove_firewall_rule(firewall: Dictionary[String, Any], rule_id: String) -> Boolean`
Removes firewall rule.

#### `get_firewall_rules(firewall: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets firewall rules.

#### `get_firewall_statistics(firewall: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets firewall statistics.

#### `create_network_vpn(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network VPN.

#### `connect_vpn(vpn: Dictionary[String, Any]) -> Boolean`
Connects to VPN.

#### `disconnect_vpn(vpn: Dictionary[String, Any]) -> Boolean`
Disconnects from VPN.

#### `get_vpn_status(vpn: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets VPN status.

#### `get_vpn_statistics(vpn: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets VPN statistics.

#### `create_network_tunnel(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network tunnel.

#### `establish_tunnel(tunnel: Dictionary[String, Any]) -> Boolean`
Establishes network tunnel.

#### `close_tunnel(tunnel: Dictionary[String, Any]) -> Boolean`
Closes network tunnel.

#### `get_tunnel_status(tunnel: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets tunnel status.

#### `create_network_bridge(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates network bridge.

#### `add_bridge_interface(bridge: Dictionary[String, Any], interface: String) -> Boolean`
Adds interface to bridge.

#### `remove_bridge_interface(bridge: Dictionary[String, Any], interface: String) -> Boolean`
Removes interface from bridge.

#### `get_bridge_interfaces(bridge: Dictionary[String, Any]) -> List[String]`
Gets bridge interfaces.

#### `get_bridge_statistics(bridge: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets bridge statistics.

## Advanced Examples

### Echo Server

```runa
Note: Create a simple echo server that responds to client messages
:End Note

Let server_socket be create tcp socket
Let bound be bind socket to "localhost" on port 8080
Let listening be listen socket with backlog 5

If listening is true:
    Note: Server is ready to accept connections
    Let client_socket be accept connection from server_socket
    
    While true:
        Let message be receive data from client_socket with buffer size 1024
        If message is empty:
            Break
        End If
        
        Let sent be send data through client_socket with message
    End While
    
    Close client_socket
End If

Close server_socket
```

### HTTP API Client

```runa
Note: Create an HTTP client for API interactions
:End Note

Let client be create http client
Set http headers for client to {"Authorization": "Bearer token123", "Content-Type": "application/json"}
Set http timeout for client to 30.0

Let response be http post "https://api.example.com/users" with data as '{"name": "John", "email": "john@example.com"}'

If get http response status from response is 201:
    Let user_data be get http response json from response
    Note: User created successfully
Else:
    Note: Failed to create user
End If
```

### WebSocket Chat Server

```runa
Note: Create a WebSocket chat server
:End Note

Let ws_server be create websocket server on "localhost" port 8080
Let started be start websocket server ws_server

If started is true:
    Note: WebSocket server is running
    Note: Add handlers for different message types
End If
```

### Network Monitoring

```runa
Note: Monitor network traffic and detect anomalies
:End Note

Let monitor be create network monitor with config as {"interface": "eth0", "threshold": 1000}
Let monitoring be start network monitoring monitor

If monitoring is true:
    Let alerts be get monitoring alerts monitor
    
    For each alert in alerts:
        Note: Network anomaly detected: alert
    End For
End If
```

## Error Handling

The Net module provides comprehensive error handling for network operations:

```runa
Note: Handle network errors gracefully
:End Note

Let socket be create tcp socket

Try:
    Let connected be connect socket to "invalid-host" on port 8080
    If connected is false:
        Note: Connection failed
    End If
Catch error:
    Note: Network error occurred: error
Finally:
    Close socket
End Try
```

## Performance Considerations

- Use connection pooling for HTTP clients
- Implement proper timeout handling
- Use non-blocking sockets for high-performance applications
- Consider using UDP for real-time applications
- Implement proper error handling and retry logic

## Security Considerations

- Always validate input data
- Use SSL/TLS for sensitive communications
- Implement proper authentication and authorization
- Validate certificates and hostnames
- Use firewalls and network segmentation
- Monitor for suspicious network activity

## Testing

The Net module includes comprehensive tests covering:

- Socket operations (TCP, UDP, Unix)
- HTTP client/server functionality
- WebSocket operations
- SSL/TLS security
- Network discovery and monitoring
- Error handling and edge cases
- Performance and load testing
- Security testing

Run tests with:
```bash
runa test_net.runa
```

## Dependencies

The Net module depends on:
- Operating system socket APIs
- SSL/TLS libraries
- Network interface management
- System monitoring capabilities

## Future Enhancements

Planned features include:
- IPv6 support
- Advanced routing protocols
- Network virtualization
- Cloud networking integration
- Advanced security features
- Performance optimization
- Real-time analytics 