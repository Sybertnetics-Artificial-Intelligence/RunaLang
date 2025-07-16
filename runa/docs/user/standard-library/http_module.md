# HTTP Module

The HTTP module provides comprehensive HTTP protocol handling including request/response management, middleware support, routing, authentication, and advanced HTTP features.

## Overview

The HTTP module is designed to handle all HTTP-related operations in Runa, from basic request/response handling to advanced features like middleware, authentication, WebSockets, and API management. It supports both client and server operations with full protocol compliance.

## Core Features

- **HTTP Request/Response Management**: Full HTTP protocol support
- **Middleware System**: Extensible middleware architecture
- **Routing**: Advanced routing with pattern matching
- **Authentication**: Multiple authentication methods
- **WebSocket Support**: Real-time bidirectional communication
- **Server-Sent Events**: One-way real-time communication
- **File Upload/Download**: Multipart form handling
- **Caching**: Response caching and cache control
- **Rate Limiting**: Request rate limiting
- **Security**: Security headers and policies
- **API Management**: OpenAPI and GraphQL support
- **Proxy Support**: HTTP proxy handling
- **Health Checks**: Service health monitoring
- **Metrics**: Request/response metrics collection

## Basic Usage

### HTTP Client

```runa
Note: Create an HTTP client and make requests
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

### HTTP Request/Response

```runa
Note: Create and configure HTTP requests
:End Note

Let request be create http request with method as "POST" and url as "https://api.example.com/users"
Set request headers for request to {"Content-Type": "application/json", "Authorization": "Bearer token123"}
Set request json for request to {"name": "John", "email": "john@example.com"}

Let response be send request to server
Let status be get http response status from response
```

## API Reference

### HTTP Request Operations

#### `create_http_request(method: String, url: String) -> Dictionary[String, Any]`
Creates a new HTTP request object.

**Parameters:**
- `method`: HTTP method (GET, POST, PUT, DELETE, etc.)
- `url`: Request URL

**Returns:** HTTP request object

**Example:**
```runa
Let request be create http request with method as "GET" and url as "https://api.example.com/data"
```

#### `set_request_headers(request: Dictionary[String, Any], headers: Dictionary[String, String]) -> None`
Sets HTTP request headers.

**Parameters:**
- `request`: HTTP request object
- `headers`: Headers dictionary

#### `set_request_body(request: Dictionary[String, Any], body: String) -> None`
Sets HTTP request body.

**Parameters:**
- `request`: HTTP request object
- `body`: Request body string

#### `set_request_json(request: Dictionary[String, Any], json_data: Dictionary[String, Any]) -> None`
Sets HTTP request JSON body.

**Parameters:**
- `request`: HTTP request object
- `json_data`: JSON data dictionary

#### `set_request_form_data(request: Dictionary[String, Any], form_data: Dictionary[String, String]) -> None`
Sets HTTP request form data.

**Parameters:**
- `request`: HTTP request object
- `form_data`: Form data dictionary

#### `set_request_cookies(request: Dictionary[String, Any], cookies: Dictionary[String, String]) -> None`
Sets HTTP request cookies.

**Parameters:**
- `request`: HTTP request object
- `cookies`: Cookies dictionary

#### `set_request_auth(request: Dictionary[String, Any], auth_type: String, credentials: Dictionary[String, String]) -> None`
Sets HTTP request authentication.

**Parameters:**
- `request`: HTTP request object
- `auth_type`: Authentication type (basic, bearer, digest, oauth, jwt)
- `credentials`: Authentication credentials

#### `set_request_timeout(request: Dictionary[String, Any], timeout: Number) -> None`
Sets HTTP request timeout.

**Parameters:**
- `request`: HTTP request object
- `timeout`: Timeout in seconds

#### `set_request_proxy(request: Dictionary[String, Any], proxy: String) -> None`
Sets HTTP request proxy.

**Parameters:**
- `request`: HTTP request object
- `proxy`: Proxy URL

#### `set_request_ssl_verify(request: Dictionary[String, Any], verify: Boolean) -> None`
Sets HTTP request SSL verification.

**Parameters:**
- `request`: HTTP request object
- `verify`: Enable/disable SSL verification

#### `set_request_redirects(request: Dictionary[String, Any], allow_redirects: Boolean) -> None`
Sets HTTP request redirect handling.

**Parameters:**
- `request`: HTTP request object
- `allow_redirects`: Allow/deny redirects

#### `set_request_stream(request: Dictionary[String, Any], stream: Boolean) -> None`
Sets HTTP request streaming.

**Parameters:**
- `request`: HTTP request object
- `stream`: Enable/disable streaming

### HTTP Request Information

#### `get_request_method(request: Dictionary[String, Any]) -> String`
Gets HTTP request method.

#### `get_request_url(request: Dictionary[String, Any]) -> String`
Gets HTTP request URL.

#### `get_request_headers(request: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP request headers.

#### `get_request_body(request: Dictionary[String, Any]) -> String`
Gets HTTP request body.

#### `get_request_json(request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets HTTP request JSON body.

#### `get_request_cookies(request: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP request cookies.

#### `get_request_params(request: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP request parameters.

#### `get_request_ip(request: Dictionary[String, Any]) -> String`
Gets HTTP request IP address.

#### `get_request_user_agent(request: Dictionary[String, Any]) -> String`
Gets HTTP request user agent.

#### `get_request_content_type(request: Dictionary[String, Any]) -> String`
Gets HTTP request content type.

#### `get_request_content_length(request: Dictionary[String, Any]) -> Integer`
Gets HTTP request content length.

### HTTP Response Operations

#### `create_http_response(status_code: Integer, body: String) -> Dictionary[String, Any]`
Creates a new HTTP response object.

**Parameters:**
- `status_code`: HTTP status code
- `body`: Response body

**Returns:** HTTP response object

#### `set_response_headers(response: Dictionary[String, Any], headers: Dictionary[String, String]) -> None`
Sets HTTP response headers.

#### `set_response_body(response: Dictionary[String, Any], body: String) -> None`
Sets HTTP response body.

#### `set_response_json(response: Dictionary[String, Any], json_data: Dictionary[String, Any]) -> None`
Sets HTTP response JSON body.

#### `set_response_cookies(response: Dictionary[String, Any], cookies: Dictionary[String, Dictionary[String, Any]]) -> None`
Sets HTTP response cookies.

#### `set_response_status(response: Dictionary[String, Any], status_code: Integer) -> None`
Sets HTTP response status code.

#### `set_response_content_type(response: Dictionary[String, Any], content_type: String) -> None`
Sets HTTP response content type.

#### `set_response_encoding(response: Dictionary[String, Any], encoding: String) -> None`
Sets HTTP response encoding.

#### `set_response_cache_control(response: Dictionary[String, Any], cache_control: String) -> None`
Sets HTTP response cache control.

#### `set_response_etag(response: Dictionary[String, Any], etag: String) -> None`
Sets HTTP response ETag.

#### `set_response_last_modified(response: Dictionary[String, Any], last_modified: String) -> None`
Sets HTTP response last modified.

#### `set_response_location(response: Dictionary[String, Any], location: String) -> None`
Sets HTTP response location.

#### `set_response_redirect(response: Dictionary[String, Any], url: String, status_code: Integer) -> None`
Sets HTTP response redirect.

### HTTP Response Information

#### `get_response_status(response: Dictionary[String, Any]) -> Integer`
Gets HTTP response status code.

#### `get_response_headers(response: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP response headers.

#### `get_response_body(response: Dictionary[String, Any]) -> String`
Gets HTTP response body.

#### `get_response_json(response: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets HTTP response JSON body.

#### `get_response_cookies(response: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets HTTP response cookies.

#### `get_response_content_type(response: Dictionary[String, Any]) -> String`
Gets HTTP response content type.

#### `get_response_content_length(response: Dictionary[String, Any]) -> Integer`
Gets HTTP response content length.

#### `get_response_encoding(response: Dictionary[String, Any]) -> String`
Gets HTTP response encoding.

### HTTP Response Status Checks

#### `is_response_success(response: Dictionary[String, Any]) -> Boolean`
Checks if response is successful (2xx status).

#### `is_response_redirect(response: Dictionary[String, Any]) -> Boolean`
Checks if response is a redirect (3xx status).

#### `is_response_client_error(response: Dictionary[String, Any]) -> Boolean`
Checks if response is a client error (4xx status).

#### `is_response_server_error(response: Dictionary[String, Any]) -> Boolean`
Checks if response is a server error (5xx status).

### HTTP Server Operations

#### `create_http_server(host: String, port: Integer) -> Dictionary[String, Any]`
Creates a new HTTP server.

**Parameters:**
- `host`: Server host address
- `port`: Server port number

**Returns:** HTTP server object

#### `add_server_middleware(server: Dictionary[String, Any], middleware: String) -> Boolean`
Adds middleware to HTTP server.

#### `add_server_route(server: Dictionary[String, Any], method: String, path: String, handler: String) -> Boolean`
Adds route handler to HTTP server.

#### `add_server_static_files(server: Dictionary[String, Any], url_path: String, file_path: String) -> Boolean`
Adds static file serving to HTTP server.

#### `add_server_error_handler(server: Dictionary[String, Any], status_code: Integer, handler: String) -> Boolean`
Adds error handler to HTTP server.

#### `set_server_config(server: Dictionary[String, Any], config: Dictionary[String, Any]) -> Boolean`
Sets HTTP server configuration.

#### `start_http_server(server: Dictionary[String, Any]) -> Boolean`
Starts HTTP server.

#### `stop_http_server(server: Dictionary[String, Any]) -> None`
Stops HTTP server.

#### `get_server_info(server: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets HTTP server information.

#### `get_server_routes(server: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets HTTP server routes.

#### `get_server_middleware(server: Dictionary[String, Any]) -> List[String]`
Gets HTTP server middleware.

#### `get_server_requests(server: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets HTTP server requests.

#### `get_server_statistics(server: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets HTTP server statistics.

### HTTP Middleware

#### `create_http_middleware(name: String, handler: String) -> Dictionary[String, Any]`
Creates HTTP middleware object.

#### `set_middleware_config(middleware: Dictionary[String, Any], config: Dictionary[String, Any]) -> None`
Sets middleware configuration.

#### `get_middleware_info(middleware: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets middleware information.

### HTTP Router

#### `create_http_router() -> Dictionary[String, Any]`
Creates HTTP router object.

#### `add_router_route(router: Dictionary[String, Any], method: String, path: String, handler: String) -> Boolean`
Adds route to HTTP router.

#### `add_router_middleware(router: Dictionary[String, Any], middleware: Dictionary[String, Any]) -> Boolean`
Adds middleware to HTTP router.

#### `set_router_prefix(router: Dictionary[String, Any], prefix: String) -> None`
Sets router prefix.

#### `get_router_routes(router: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets router routes.

#### `match_router_route(router: Dictionary[String, Any], method: String, path: String) -> Dictionary[String, Any]`
Matches route in router.

### HTTP Session Management

#### `create_http_session() -> Dictionary[String, Any]`
Creates HTTP session object.

#### `set_session_data(session: Dictionary[String, Any], key: String, value: Any) -> None`
Sets session data.

#### `get_session_data(session: Dictionary[String, Any], key: String) -> Any`
Gets session data.

#### `remove_session_data(session: Dictionary[String, Any], key: String) -> Boolean`
Removes session data.

#### `clear_session(session: Dictionary[String, Any]) -> None`
Clears session.

#### `get_session_id(session: Dictionary[String, Any]) -> String`
Gets session ID.

#### `is_session_valid(session: Dictionary[String, Any]) -> Boolean`
Checks if session is valid.

### HTTP Authentication

#### `create_http_authentication(auth_type: String, config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates HTTP authentication object.

#### `authenticate_request(auth: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Authenticates HTTP request.

#### `create_basic_auth(username: String, password: String) -> Dictionary[String, Any]`
Creates basic authentication.

#### `create_bearer_auth(token: String) -> Dictionary[String, Any]`
Creates bearer token authentication.

#### `create_digest_auth(username: String, password: String, realm: String) -> Dictionary[String, Any]`
Creates digest authentication.

#### `create_oauth_auth(client_id: String, client_secret: String, redirect_uri: String) -> Dictionary[String, Any]`
Creates OAuth authentication.

#### `create_jwt_auth(secret: String, algorithm: String) -> Dictionary[String, Any]`
Creates JWT authentication.

#### `validate_jwt_token(auth: Dictionary[String, Any], token: String) -> Dictionary[String, Any]`
Validates JWT token.

### HTTP CORS

#### `create_http_cors(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates CORS middleware.

#### `set_cors_origins(cors: Dictionary[String, Any], origins: List[String]) -> None`
Sets CORS origins.

#### `set_cors_methods(cors: Dictionary[String, Any], methods: List[String]) -> None`
Sets CORS methods.

#### `set_cors_headers(cors: Dictionary[String, Any], headers: List[String]) -> None`
Sets CORS headers.

#### `set_cors_credentials(cors: Dictionary[String, Any], credentials: Boolean) -> None`
Sets CORS credentials.

### HTTP Rate Limiting

#### `create_http_rate_limiter(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates rate limiter.

#### `set_rate_limit(limiter: Dictionary[String, Any], requests: Integer, window: Number) -> None`
Sets rate limit.

#### `check_rate_limit(limiter: Dictionary[String, Any], identifier: String) -> Boolean`
Checks rate limit.

#### `get_rate_limit_info(limiter: Dictionary[String, Any], identifier: String) -> Dictionary[String, Any]`
Gets rate limit information.

### HTTP Caching

#### `create_http_cache(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates cache middleware.

#### `set_cache_ttl(cache: Dictionary[String, Any], ttl: Number) -> None`
Sets cache TTL.

#### `get_cached_response(cache: Dictionary[String, Any], key: String) -> Dictionary[String, Any]`
Gets cached response.

#### `set_cached_response(cache: Dictionary[String, Any], key: String, response: Dictionary[String, Any]) -> None`
Sets cached response.

#### `invalidate_cache(cache: Dictionary[String, Any], pattern: String) -> Integer`
Invalidates cache.

### HTTP Logging

#### `create_http_logger(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates logger middleware.

#### `set_log_level(logger: Dictionary[String, Any], level: String) -> None`
Sets log level.

#### `set_log_format(logger: Dictionary[String, Any], format: String) -> None`
Sets log format.

#### `log_request(logger: Dictionary[String, Any], request: Dictionary[String, Any]) -> None`
Logs HTTP request.

#### `log_response(logger: Dictionary[String, Any], response: Dictionary[String, Any]) -> None`
Logs HTTP response.

### HTTP Compression

#### `create_http_compression(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates compression middleware.

#### `set_compression_level(compression: Dictionary[String, Any], level: Integer) -> None`
Sets compression level.

#### `set_compression_types(compression: Dictionary[String, Any], types: List[String]) -> None`
Sets compression types.

#### `compress_response(compression: Dictionary[String, Any], response: Dictionary[String, Any]) -> Dictionary[String, Any]`
Compresses HTTP response.

#### `decompress_request(compression: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Decompresses HTTP request.

### HTTP Security

#### `create_http_security(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates security middleware.

#### `set_security_headers(security: Dictionary[String, Any], headers: Dictionary[String, String]) -> None`
Sets security headers.

#### `set_csp_policy(security: Dictionary[String, Any], policy: String) -> None`
Sets CSP policy.

#### `set_hsts_policy(security: Dictionary[String, Any], max_age: Integer) -> None`
Sets HSTS policy.

#### `apply_security_headers(security: Dictionary[String, Any], response: Dictionary[String, Any]) -> Dictionary[String, Any]`
Applies security headers.

### WebSocket Support

#### `create_http_websocket(path: String) -> Dictionary[String, Any]`
Creates WebSocket handler.

#### `set_websocket_handler(websocket: Dictionary[String, Any], handler: String) -> None`
Sets WebSocket handler.

#### `set_websocket_protocols(websocket: Dictionary[String, Any], protocols: List[String]) -> None`
Sets WebSocket protocols.

#### `handle_websocket_upgrade(websocket: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles WebSocket upgrade.

#### `create_http_websocket_connection(request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates WebSocket connection.

#### `send_websocket_message(connection: Dictionary[String, Any], message: String) -> Boolean`
Sends WebSocket message.

#### `receive_websocket_message(connection: Dictionary[String, Any]) -> String`
Receives WebSocket message.

#### `close_websocket_connection(connection: Dictionary[String, Any]) -> None`
Closes WebSocket connection.

### Server-Sent Events

#### `create_http_sse(path: String) -> Dictionary[String, Any]`
Creates SSE handler.

#### `set_sse_handler(sse: Dictionary[String, Any], handler: String) -> None`
Sets SSE handler.

#### `send_sse_event(sse: Dictionary[String, Any], event: String, data: String) -> Boolean`
Sends SSE event.

### File Upload/Download

#### `create_http_multipart(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates multipart handler.

#### `set_multipart_max_size(multipart: Dictionary[String, Any], max_size: Integer) -> None`
Sets multipart max size.

#### `parse_multipart_request(multipart: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Parses multipart request.

#### `get_multipart_files(parsed: Dictionary[String, Any]) -> List[Dictionary[String, Any]]`
Gets multipart files.

#### `get_multipart_fields(parsed: Dictionary[String, Any]) -> Dictionary[String, String]`
Gets multipart fields.

#### `create_http_upload(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates upload handler.

#### `set_upload_directory(upload: Dictionary[String, Any], directory: String) -> None`
Sets upload directory.

#### `set_upload_max_size(upload: Dictionary[String, Any], max_size: Integer) -> None`
Sets upload max size.

#### `set_upload_allowed_types(upload: Dictionary[String, Any], types: List[String]) -> None`
Sets upload allowed types.

#### `handle_file_upload(upload: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles file upload.

#### `create_http_download(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates download handler.

#### `set_download_directory(download: Dictionary[String, Any], directory: String) -> None`
Sets download directory.

#### `set_download_chunk_size(download: Dictionary[String, Any], chunk_size: Integer) -> None`
Sets download chunk size.

#### `handle_file_download(download: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles file download.

### HTTP Proxy

#### `create_http_proxy(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates proxy handler.

#### `set_proxy_target(proxy: Dictionary[String, Any], target: String) -> None`
Sets proxy target.

#### `set_proxy_rewrite_rules(proxy: Dictionary[String, Any], rules: List[Dictionary[String, String]]) -> None`
Sets proxy rewrite rules.

#### `handle_proxy_request(proxy: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles proxy request.

### Health Checks

#### `create_http_health_check(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates health check handler.

#### `set_health_check_endpoint(health: Dictionary[String, Any], endpoint: String) -> None`
Sets health check endpoint.

#### `set_health_check_checks(health: Dictionary[String, Any], checks: List[String]) -> None`
Sets health check checks.

#### `perform_health_check(health: Dictionary[String, Any]) -> Dictionary[String, Any]`
Performs health check.

### Metrics

#### `create_http_metrics(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates metrics handler.

#### `set_metrics_endpoint(metrics: Dictionary[String, Any], endpoint: String) -> None`
Sets metrics endpoint.

#### `record_request_metric(metrics: Dictionary[String, Any], request: Dictionary[String, Any], response: Dictionary[String, Any]) -> None`
Records request metric.

#### `get_metrics_data(metrics: Dictionary[String, Any]) -> Dictionary[String, Any]`
Gets metrics data.

### API Management

#### `create_http_openapi(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates OpenAPI handler.

#### `set_openapi_spec(openapi: Dictionary[String, Any], spec: Dictionary[String, Any]) -> None`
Sets OpenAPI spec.

#### `set_openapi_endpoint(openapi: Dictionary[String, Any], endpoint: String) -> None`
Sets OpenAPI endpoint.

#### `generate_openapi_spec(openapi: Dictionary[String, Any], routes: List[Dictionary[String, Any]]) -> Dictionary[String, Any]`
Generates OpenAPI spec.

#### `create_http_graphql(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates GraphQL handler.

#### `set_graphql_schema(graphql: Dictionary[String, Any], schema: String) -> None`
Sets GraphQL schema.

#### `set_graphql_resolvers(graphql: Dictionary[String, Any], resolvers: Dictionary[String, String]) -> None`
Sets GraphQL resolvers.

#### `handle_graphql_request(graphql: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles GraphQL request.

#### `create_http_grpc(config: Dictionary[String, Any]) -> Dictionary[String, Any]`
Creates gRPC handler.

#### `set_grpc_proto(grpc: Dictionary[String, Any], proto: String) -> None`
Sets gRPC proto.

#### `set_grpc_services(grpc: Dictionary[String, Any], services: Dictionary[String, String]) -> None`
Sets gRPC services.

#### `handle_grpc_request(grpc: Dictionary[String, Any], request: Dictionary[String, Any]) -> Dictionary[String, Any]`
Handles gRPC request.

## Advanced Examples

### RESTful API Server

```runa
Note: Create a RESTful API server with middleware
:End Note

Let server be create http server on "localhost" port 3000

Note: Add CORS middleware
Let cors be create http cors with config as {"origins": ["*"], "methods": ["GET", "POST", "PUT", "DELETE"]}
Add server middleware server with cors

Note: Add authentication middleware
Let auth be create jwt auth with secret "my-secret" and algorithm "HS256"
Add server middleware server with auth

Note: Add routes
Add server route server with method "GET" and path "/api/users" and handler "get_users_handler"
Add server route server with method "POST" and path "/api/users" and handler "create_user_handler"
Add server route server with method "PUT" and path "/api/users/:id" and handler "update_user_handler"
Add server route server with method "DELETE" and path "/api/users/:id" and handler "delete_user_handler"

Let started be start http server server
```

### WebSocket Chat Server

```runa
Note: Create a WebSocket chat server
:End Note

Let server be create http server on "localhost" port 8080

Let ws_handler be create http websocket with path "/chat"
Set websocket handler ws_handler with "chat_message_handler"

Add server route server with method "GET" and path "/chat" and handler ws_handler

Let started be start http server server
```

### File Upload Server

```runa
Note: Create a file upload server
:End Note

Let server be create http server on "localhost" port 3000

Let upload be create http upload with config as {"max_size": 10485760, "allowed_types": ["jpg", "png", "pdf"]}
Set upload directory upload to "/uploads"

Add server route server with method "POST" and path "/upload" and handler upload

Let started be start http server server
```

### API Gateway

```runa
Note: Create an API gateway with rate limiting and caching
:End Note

Let server be create http server on "localhost" port 3000

Note: Add rate limiting
Let limiter be create http rate limiter with config as {"window": 60, "max_requests": 100}
Add server middleware server with limiter

Note: Add caching
Let cache be create http cache with config as {"ttl": 300}
Add server middleware server with cache

Note: Add proxy routes
Let proxy be create http proxy with config as {"target": "http://backend-service:8080"}
Add server route server with method "*" and path "/api/*" and handler proxy

Let started be start http server server
```

## Error Handling

The HTTP module provides comprehensive error handling:

```runa
Note: Handle HTTP errors gracefully
:End Note

Let client be create http client

Try:
    Let response be http get "https://invalid-url.com"
    Let status be get http response status from response
    
    If is response client error response:
        Note: Handle client error
    Else If is response server error response:
        Note: Handle server error
    End If
Catch error:
    Note: Handle network error: error
End Try
```

## Performance Considerations

- Use connection pooling for HTTP clients
- Implement proper timeout handling
- Use compression for large responses
- Implement caching for frequently accessed resources
- Use rate limiting to prevent abuse
- Monitor request/response metrics
- Use async operations for I/O-bound tasks

## Security Considerations

- Always validate input data
- Use HTTPS for sensitive communications
- Implement proper authentication and authorization
- Set security headers (CSP, HSTS, etc.)
- Validate file uploads
- Implement rate limiting
- Use secure session management
- Monitor for suspicious activity

## Testing

The HTTP module includes comprehensive tests covering:

- Request/response handling
- Middleware functionality
- Authentication systems
- WebSocket operations
- File upload/download
- Error handling
- Performance testing
- Security testing

Run tests with:
```bash
runa test_http.runa
```

## Dependencies

The HTTP module depends on:
- Network socket operations
- SSL/TLS libraries
- Compression libraries
- Authentication libraries
- File system operations

## Future Enhancements

Planned features include:
- HTTP/2 and HTTP/3 support
- Advanced caching strategies
- Load balancing
- Service mesh integration
- Advanced security features
- Performance optimization
- Real-time analytics 