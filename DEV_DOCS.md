# Developer Documentation & Review

Welcome to the RPC Framework developer documentation! This document provides a comprehensive overview of how the custom Remote Procedure Call framework is structured, where to find specific functionality, and a technical review of the architecture.

---

## 🏗️ 1. Architecture Overview (What does what)

The framework is divided into three main layers:
1. **Application Layer (Services & UI)**: The business logic (e.g., Calculator) and the user interfaces.
2. **Stub/Skeleton Layer**: Auto-generated boilerplate code that maps local method calls to network requests.
3. **RPC Core Engine**: The internal machinery that handles serialization, protocol errors, exact-once semantics, and raw TCP networking.

---

## 📂 2. Module Breakdown (Where to go)

### `rpc_core/` (The Engine)
This folder contains the core logic of the framework. You rarely need to touch this unless you are upgrading the protocol itself.
- **`transport.py`**: Handles the raw TCP Socket connections. Implements "Length-Prefixed Message Framing" to ensure JSON strings aren't fragmented or merged during network transit. 
- **`serializer.py`**: Contains `JSONSerializer`. Validates that only allowed types (`int`, `str`, `list`) are processed, and converts Python objects to byte-strings for the transport layer.
- **`protocol.py`**: Defines standardized RPC integer error codes (`METHOD_NOT_FOUND`, `INVALID_PARAMS`, etc.) and the `RPCError` exception.
- **`semantics.py`**: Contains `ResponseCache`. Essential for network reliability; it caches the results of executed requests by their UUID to prevent running the same request twice if the client retries.
- **`rpc_server.py`**: The **Request Dispatcher**. It listens for incoming transport messages, unmarshals them, looks up the requested method in its registry, executes the actual python function, catches any execution errors, and sends the formatted response back.
- **`rpc_client.py`**: The client-side engine. Generates unique UUIDs for requests, marshals them, and contains a retry-loop that automatically reconnects and retransmits requests if a `socket.timeout` occurs.

### `generator/` (Automation)
- **`code_generator.py`**: A custom IDL parser using regex. Developers write simple definitions in `idl/calculator.idl`, run this script, and it automatically writes the complex boilerplate for `client/generated_stub.py` and `server/generated_skeleton.py`.

### Entry Points (How to start)
- **`server/calculator_server.py`**: The main entry point to start the server. It instantiates the `RPCServer`, binds the `CalculatorService` logic to it via the generated skeleton, and starts listening.
- **`client/calculator_client.py`**: A terminal-based testing script that invokes RPC methods and handles exceptions.
- **`client/calculator_gui.py`**: The Tkinter graphical interface for interacting with the RPC framework visually.

---

## 🔍 3. Developer Review

### ✅ Strengths & Achievements
1. **Zero External Dependencies**: The entire architecture relies solely on Python's standard library (`socket`, `json`, `threading`, `tkinter`). It is highly portable.
2. **At-Most-Once / Exactly-Once Semantics**: By combining Client-side retries with Server-side duplicate UUID detection (`ResponseCache`), the framework guarantees that a remote method is executed exactly once even if network connections drop abruptly.
3. **Clean Code Separation**: The business logic (`CalculatorService`) is completely isolated from the networking logic. Developers can add new services without knowing how sockets work.
4. **Resilient Error Handling**: Stack traces and execution crashes on the server are securely caught and forwarded to the client as clean `RPCError` objects.

### ⚠️ Limitations & Areas for Improvement
1. **Scalability**: The `RPCServerTransport` uses a "Thread-per-client" model (`threading.Thread`). While perfect for lightweight tasks, it will struggle with thousands of concurrent connections due to Python's GIL and OS thread overhead. *Improvement: Migrate to `asyncio` for non-blocking IO.*
2. **Security**: Data is transmitted via raw TCP sockets in plain text. There is no encryption (TLS/SSL), making it vulnerable to packet sniffing. Furthermore, there is no authentication layer to verify who is calling the server.
3. **Serialization Efficiency**: We use JSON for message passing. While easy to debug and read, it is slow to parse and takes up more bandwidth compared to binary protocols like Protocol Buffers (Protobuf) or MessagePack.
4. **Cache Memory Leak**: The `ResponseCache` in `semantics.py` currently stores every processed request indefinitely. *Improvement: Implement a TTL (Time-To-Live) eviction policy or an LRU (Least Recently Used) cache to clean up old request IDs and prevent memory exhaustion over time.*
