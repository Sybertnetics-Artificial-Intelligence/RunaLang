# Messaging Core Module

## Overview

The Messaging Core module (`messaging.runa`) is the foundational layer of the AI Communication System, providing comprehensive message creation, queuing, delivery, and lifecycle management capabilities. This module handles all aspects of message processing from creation to final delivery.

## Key Features

- **Message Lifecycle Management**: Complete tracking from creation to delivery
- **Priority-Based Queuing**: Support for critical, high, normal, low, and background priorities
- **Delivery Guarantees**: Best-effort, at-least-once, exactly-once, ordered, and reliable delivery
- **Message Compression**: Automatic compression for large payloads
- **Retry Logic**: Configurable exponential backoff with jitter
- **Network Transport**: TCP, UDP, and WebSocket delivery mechanisms
- **Error Handling**: Comprehensive error tracking and recovery

## Core Types

### Message Structure

```runa
Type called "AgentMessage":
    message_id as String
    conversation_id as Optional[String]
    parent_message_id as Optional[String]
    sender_id as String
    receiver_id as String
    message_type as MessageType
    priority as MessagePriority
    delivery_guarantee as DeliveryGuarantee
    payload as Any
    headers as Dictionary[String, String]
    metadata as MessageMetadata
    signature as Optional[String]
    encryption_info as Optional[Dictionary]
    status as MessageStatus
    error_info as Optional[Dictionary]
```

### Message Types

```runa
Type MessageType is Enum with values:
    "request"        - Request for action or information
    "response"       - Response to a request
    "notification"   - One-way information broadcast
    "broadcast"      - Message to multiple recipients
    "multicast"      - Message to specific group
    "heartbeat"      - Keep-alive signal
    "discovery"      - Agent discovery message
    "coordination"   - Multi-agent coordination
    "data_transfer"  - Large data payload
    "error"          - Error notification
    "acknowledgment" - Delivery confirmation
    "shutdown"       - Graceful shutdown signal
```

### Priority Levels

```runa
Type MessagePriority is Enum with values:
    "critical"    - Highest priority, immediate processing
    "high"        - High priority, fast processing
    "normal"      - Standard priority
    "low"         - Lower priority, batch processing
    "background"  - Lowest priority, process when idle
```

### Delivery Guarantees

```runa
Type DeliveryGuarantee is Enum with values:
    "best_effort"   - No delivery guarantee, fastest
    "at_least_once" - Message delivered at least once
    "exactly_once"  - Message delivered exactly once
    "ordered"       - Messages delivered in order
    "reliable"      - Combination of exactly-once and ordered
```

## Usage Examples

### Basic Message Creation

```runa
Import "ai/comms/messaging" as Messaging

Process called "create_simple_message" returns AgentMessage:
    Let message be Messaging.create_message with
        sender_id as "agent_sender" and
        receiver_id as "agent_receiver" and
        message_type as "request" and
        payload as "Process this data please"
    
    Return message
```

### Request-Response Pattern

```runa
Process called "send_request_and_wait" returns AgentMessage:
    Note: Create a request message with high priority
    Let request be Messaging.create_request_message with
        sender_id as "requesting_agent" and
        receiver_id as "processing_agent" and
        request_data as Dictionary with:
            "task" as "analyze_data"
            "parameters" as Dictionary with "dataset" as "user_behavior_2024"
    
    Note: Send the request
    Let delivery_result be Messaging.route_message_to_destination with message as request
    
    If delivery_result["success"]:
        Print "Request sent successfully"
        Note: Response handling would be implemented in a separate process
        Return request
    Else:
        Print "Request delivery failed: " + delivery_result["error"]
        Return create_error_message with error as delivery_result["error"]
```

### Creating Response Messages

```runa
Process called "respond_to_request" that takes original_request as AgentMessage and result_data as Any returns AgentMessage:
    Let response be Messaging.create_response_message with
        original_message as original_request and
        response_data as result_data
    
    Note: Response automatically inherits conversation context
    Print "Response created for conversation: " + response["conversation_id"]
    
    Return response
```

### Broadcast Messages

```runa
Process called "broadcast_announcement" that takes announcement as String returns Boolean:
    Let broadcast_message be Messaging.create_broadcast_message with
        sender_id as "system_coordinator" and
        payload as Dictionary with:
            "type" as "system_announcement"
            "message" as announcement
            "timestamp" as get_current_timestamp()
    
    Let broadcast_result be Messaging.handle_broadcast_message with message as broadcast_message
    
    Return broadcast_result["success"]
```

## Message Queuing

### Creating Message Queues

```runa
Process called "setup_agent_queue" that takes agent_id as String returns MessageQueue:
    Let queue be Messaging.create_message_queue with
        agent_id as agent_id and
        max_size as 1000
    
    Note: Configure overflow policy
    Let configured_queue be Messaging.configure_queue_overflow with
        queue as queue and
        policy as "drop_oldest"
    
    Return configured_queue
```

### Queue Operations

```runa
Process called "process_message_queue" that takes queue as MessageQueue returns ProcessingResult:
    Let results be list containing
    
    Note: Process high-priority messages first
    Let high_priority_messages be Messaging.get_priority_messages with
        queue as queue and
        priority as "critical"
    
    For each message in high_priority_messages:
        Let dequeue_result be Messaging.dequeue_message with queue as queue
        If dequeue_result["success"]:
            Let processed_message be process_single_message with message as dequeue_result["message"]
            Add processed_message to results
    
    Note: Process normal priority messages
    Let normal_messages be Messaging.get_priority_messages with
        queue as queue and
        priority as "normal"
    
    For each message in normal_messages:
        Let dequeue_result be Messaging.dequeue_message with queue as queue
        If dequeue_result["success"]:
            Let processed_message be process_single_message with message as dequeue_result["message"]
            Add processed_message to results
    
    Return ProcessingResult with:
        processed_count as length of results
        results as results
```

## Message Delivery

### TCP Delivery

```runa
Process called "deliver_via_tcp_with_retry" that takes message as AgentMessage and endpoint as String returns DeliveryResult:
    Let max_retries be 3
    Let retry_count be 0
    
    While retry_count < max_retries:
        Let delivery_result be Messaging.deliver_via_tcp with
            message as message and
            endpoint as endpoint
        
        If delivery_result["success"]:
            Return DeliveryResult with:
                success as true
                delivery_time as delivery_result["delivery_time"]
                bytes_sent as delivery_result["bytes_sent"]
                retry_count as retry_count
        
        Set retry_count to retry_count plus 1
        Let delay be Messaging.calculate_retry_delay with retry_count as retry_count
        Let sleep_result be system_sleep with seconds as delay
    
    Return DeliveryResult with:
        success as false
        error as "Max retries exceeded"
        retry_count as retry_count
```

### UDP Delivery

```runa
Process called "deliver_low_latency" that takes message as AgentMessage and endpoint as String returns Boolean:
    Note: UDP is best for low-latency, fire-and-forget messages
    Let udp_result be Messaging.deliver_via_udp with
        message as message and
        endpoint as endpoint
    
    If udp_result["success"]:
        Print "Low-latency delivery successful in " + udp_result["delivery_time"] + "ms"
        Return true
    Else:
        Print "UDP delivery failed: " + udp_result["error"]
        Return false
```

## Message Compression

### Automatic Compression

```runa
Process called "send_large_data" that takes large_dataset as Dictionary returns Boolean:
    Note: Large payloads are automatically compressed
    Let message be Messaging.create_message with
        sender_id as "data_producer" and
        receiver_id as "data_consumer" and
        message_type as "data_transfer" and
        payload as large_dataset
    
    Note: Enable compression for efficiency
    Let compressed_message be Messaging.enable_message_compression with
        message as message and
        compression_type as "gzip"
    
    Let delivery_result be Messaging.route_message_to_destination with message as compressed_message
    
    If delivery_result["success"]:
        Print "Large dataset delivered with compression"
        Print "Original size: " + calculate_size(large_dataset) + " bytes"
        Print "Compressed size: " + delivery_result["compressed_size"] + " bytes"
    
    Return delivery_result["success"]
```

### Manual Compression Control

```runa
Process called "compress_sensitive_data" that takes sensitive_data as Dictionary returns Dictionary:
    Note: Compress data before encryption for better performance
    Let compressed_data be Messaging.compress_data with data as sensitive_data
    
    Note: Verify compression was effective
    Let original_size be calculate_payload_size(sensitive_data)
    Let compressed_size be calculate_payload_size(compressed_data)
    Let compression_ratio be original_size / compressed_size
    
    If compression_ratio > 1.2:
        Print "Effective compression achieved: " + compression_ratio + "x reduction"
        Return compressed_data
    Else:
        Print "Compression not effective, using original data"
        Return sensitive_data
```

## Error Handling and Retry Logic

### Configurable Retry Policies

```runa
Process called "setup_custom_retry_policy" that takes message as AgentMessage returns AgentMessage:
    Let retry_policy be Dictionary with:
        "max_retries" as 5
        "base_delay_seconds" as 1.0
        "max_delay_seconds" as 120.0
        "backoff_strategy" as "exponential"
        "jitter_enabled" as true
    
    Let configured_message be Messaging.configure_message_retry with
        message as message and
        retry_policy as retry_policy
    
    Return configured_message
```

### Error Recovery

```runa
Process called "handle_delivery_failures" that takes failed_messages as List[AgentMessage] returns RecoveryResult:
    Let recovered_messages be list containing
    Let permanent_failures be list containing
    
    For each message in failed_messages:
        Let error_info be message["error_info"]
        
        If error_info["error_type"] is equal to "network_timeout":
            Note: Retry network timeouts
            Let retry_result be retry_message_delivery with message as message
            If retry_result["success"]:
                Add message to recovered_messages
            Else:
                Add message to permanent_failures
        
        Otherwise if error_info["error_type"] is equal to "agent_not_found":
            Note: Route to dead letter queue
            Let dlq_result be Messaging.send_to_dead_letter_queue with message as message
            Add message to permanent_failures
        
        Otherwise:
            Note: Log and investigate unknown errors
            Log error with message_id as message["message_id"] and error as error_info
            Add message to permanent_failures
    
    Return RecoveryResult with:
        recovered_count as length of recovered_messages
        permanent_failure_count as length of permanent_failures
        recovered_messages as recovered_messages
        permanent_failures as permanent_failures
```

## Performance Monitoring

### Message Metrics

```runa
Process called "collect_messaging_metrics" returns MessageMetrics:
    Let metrics be Messaging.get_current_metrics()
    
    Print "=== Messaging Performance Metrics ==="
    Print "Total messages sent: " + metrics["total_sent"]
    Print "Total messages received: " + metrics["total_received"]
    Print "Total failed messages: " + metrics["total_failed"]
    Print "Average latency: " + metrics["average_latency"] + "ms"
    Print "Current queue size: " + metrics["current_queue_size"]
    Print "Peak queue size: " + metrics["peak_queue_size"]
    Print "Error rate: " + (metrics["error_rate"] * 100.0) + "%"
    Print "Throughput: " + metrics["throughput"] + " messages/second"
    
    Return metrics
```

### Performance Optimization

```runa
Process called "optimize_messaging_performance" returns OptimizationResult:
    Let current_metrics be collect_messaging_metrics()
    Let optimizations be list containing
    
    Note: Check for queue depth issues
    If current_metrics["current_queue_size"] > 800:
        Add "Increase queue processing threads" to optimizations
        Add "Consider message batching" to optimizations
    
    Note: Check for high error rates
    If current_metrics["error_rate"] > 0.05:
        Add "Review network stability" to optimizations
        Add "Increase retry timeouts" to optimizations
    
    Note: Check for high latency
    If current_metrics["average_latency"] > 100.0:
        Add "Optimize network routing" to optimizations
        Add "Consider message compression" to optimizations
    
    Return OptimizationResult with:
        current_performance as current_metrics
        recommendations as optimizations
```

## Configuration

### Message Configuration

```runa
Let messaging_config be Dictionary with:
    "default_timeout_seconds" as 30.0
    "max_retries" as 3
    "retry_base_delay_seconds" as 1.0
    "retry_max_delay_seconds" as 300.0
    "compression_threshold_bytes" as 1024
    "queue_max_size" as 10000
    "enable_message_signing" as true
    "enable_encryption" as true
```

### Advanced Configuration

```runa
Process called "configure_advanced_messaging" returns MessagingConfiguration:
    Let config be get_messaging_configuration()
    
    Note: Configure delivery guarantees
    Set config["delivery_guarantees"] to Dictionary with:
        "exactly_once_enabled" as true
        "ordered_delivery_enabled" as true
        "deduplication_window_seconds" as 300
    
    Note: Configure priority handling
    Set config["priority_handling"] to Dictionary with:
        "critical_queue_size" as 100
        "high_queue_size" as 500
        "normal_queue_size" as 5000
        "low_queue_size" as 2000
        "background_queue_size" as 1000
    
    Note: Configure compression
    Set config["compression"] to Dictionary with:
        "enabled" as true
        "algorithm" as "gzip"
        "threshold_bytes" as 1024
        "level" as 6
    
    Return config
```

## Integration Examples

### With Encryption Module

```runa
Process called "send_encrypted_message" that takes recipient as String and sensitive_data as Dictionary returns Boolean:
    Import "ai/comms/encryption" as Encryption
    
    Note: Create and encrypt message
    Let message be Messaging.create_message with
        sender_id as "secure_sender" and
        receiver_id as recipient and
        message_type as "data_transfer" and
        payload as sensitive_data
    
    Note: Apply encryption
    Let encryption_key be Encryption.get_agent_key with agent_id as recipient
    Let encrypted_payload be Encryption.encrypt_data with
        data as message["payload"] and
        key as encryption_key and
        algorithm as "aes_256_gcm"
    
    Set message["payload"] to encrypted_payload["encrypted_data"]
    Set message["encryption_info"] to Dictionary with:
        "algorithm" as "aes_256_gcm"
        "key_id" as encryption_key["key_id"]
    
    Let delivery_result be Messaging.route_message_to_destination with message as message
    Return delivery_result["success"]
```

### With Agent Framework

```runa
Process called "integrate_with_agent" that takes agent as AgentCore returns MessagingEnabledAgent:
    Import "ai/agent/core" as Agent
    
    Let agent_queue be Messaging.create_message_queue with
        agent_id as agent["agent_id"] and
        max_size as 1000
    
    Note: Set up message processing
    Let message_processor be Process that takes message as AgentMessage returns ProcessingResult:
        Match message["message_type"]:
            When "request":
                Return Agent.handle_request with agent as agent and request as message
            When "notification":
                Return Agent.handle_notification with agent as agent and notification as message
            When "heartbeat":
                Return Agent.handle_heartbeat with agent as agent
            Otherwise:
                Return ProcessingResult with success as false and error as "Unknown message type"
    
    Let messaging_enabled_agent be Agent.add_capability with
        agent as agent and
        capability as "messaging" and
        handler as message_processor
    
    Return messaging_enabled_agent
```

## Best Practices

### 1. **Message Design**
- Keep message payloads focused and atomic
- Use appropriate message types for different communication patterns
- Include sufficient context in message headers for debugging

### 2. **Queue Management**
- Monitor queue depths and adjust processing capacity accordingly
- Use priority levels appropriately to ensure critical messages are processed first
- Implement proper overflow handling to prevent message loss

### 3. **Error Handling**
- Always implement retry logic with exponential backoff
- Use dead letter queues for messages that cannot be delivered
- Log detailed error information for troubleshooting

### 4. **Performance**
- Enable compression for large payloads
- Use UDP for low-latency, fire-and-forget messages
- Use TCP for reliable delivery requirements
- Monitor and tune configuration based on actual traffic patterns

### 5. **Security**
- Always encrypt sensitive message payloads
- Use digital signatures for message authentication
- Implement proper access controls for message queues

The Messaging Core module provides the solid foundation needed for building sophisticated AI agent communication systems with enterprise-grade reliability, security, and performance.