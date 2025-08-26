# Runa Agent Networking and Communication Layer Implementation Plan

## 1. Objective

To build a secure, reliable, and scalable communication layer for the Runa AI Agent Framework. This layer is the foundational prerequisite for enabling the advanced multi-agent architectural workflows, including the Nemesis Security Bus, the Odin Strategic Dispatcher, and the seamless fulfillment of external user requests.

## 2. Current State

A foundational `network.runa` module has been created. It defines the core data structures for communication (`AgentMessage`, `NetworkEndpoint`) and the high-level process signatures for sending and receiving messages. However, the underlying network transport is currently implemented with placeholders and does not perform real network operations.

## 3. Phased Implementation Plan

The development will proceed in four distinct, sequential phases to ensure a robust and well-structured implementation.

### Phase 1: Core Transport Layer (TCP Implementation)

This phase focuses on replacing the placeholder network functions with a functional, asynchronous TCP transport layer using the Runa `net/tcp` standard library.

-   **Implement `_start_listening_server`:** Each agent, upon initialization, will call this process to start a non-blocking TCP server on its designated endpoint. This server will run in a separate thread to listen for incoming connections.
-   **Implement `_handle_incoming_connection`:** This process will be responsible for handling new TCP connections. Its duties will include:
    1.  Reading the raw data from the socket.
    2.  Deserializing the JSON data into an `AgentMessage`.
    3.  Performing a cryptographic signature verification on the message using the source agent's public key to ensure authenticity and integrity.
    4.  Placing the verified message into the target agent's inbound message queue.
-   **Implement `_send_tcp_message_async`:** This process will manage the client-side communication. It will:
    1.  Establish a TCP connection to a target agent's endpoint.
    2.  Serialize an `AgentMessage` into JSON.
    3.  Send the data over the established connection.
    4.  This process will be non-blocking to ensure the sending agent remains responsive.

**Success Criterion for Phase 1:** Two agents can be run as separate processes and successfully exchange signed, verified messages over the network.

### Phase 2: Service Discovery Integration

This phase will decouple agents by removing the need for hardcoded endpoints and integrating with the agent registry for dynamic service discovery.

-   **Update `_discover_agent_endpoint`:** The current placeholder logic will be replaced with a live lookup against the persistent `AgentRegistry` (from `registry.runa`). When an agent needs to send a message, it will query the registry for the target agent's last known endpoint.

**Success Criterion for Phase 2:** An agent can send a message to another agent using only its `agent_id`, with the network address being resolved dynamically at runtime.

### Phase 3: Protocol Enhancement for Architectural Patterns

This phase will enhance the `AgentMessage` protocol to support the complex, asynchronous workflows required by the SyberCraft architecture.

-   **Modify `AgentMessage` Payload:** The generic `payload` dictionary will be given a more defined structure by adding two key fields:
    -   `message_type`: A string identifier (e.g., "ComplianceCheckRequest", "TaskDispatch", "QASubmission") to allow receiving agents to quickly route the message to the correct handler.
    -   `correlation_id`: A unique identifier to link requests with their corresponding responses. This is essential for managing asynchronous conversations and callbacks.

**Success Criterion for Phase 3:** The message protocol can unambiguously represent the different types of interactions in the three core workflows and can correlate asynchronous responses with their original requests.

### Phase 4: Implementing Architectural Routing

With a robust networking layer in place, this phase will implement the application-level logic for the high-level architectural patterns.

-   **Implement the Nemesis Security Bus:** This will be an application-level routing rule. All agents will be configured to send their outbound messages to the Nemesis agent's well-known endpoint. Nemesis's core logic will then be implemented to inspect these messages, verify compliance, and securely forward them to the intended recipient (e.g., Odin or another agent).
-   **Implement the Odin Strategic Dispatcher:** This logic will reside within the Odin agent. Odin will be programmed to receive abstract work orders, use the `registry.runa` module to query for specialist agents based on required capabilities, and use the `network.runa` module to dispatch the work order to the selected agent.

**Success Criterion for Phase 4:** The Nemesis and Odin agents correctly route and dispatch messages according to the defined workflows, effectively orchestrating the agent federation.

## 4. Final Success Criteria

The successful completion of this plan will result in a fully functional, secure, and reliable inter-agent communication system that serves as the central nervous system for the SyberCraft agent federation, ready to support all defined operational workflows.
