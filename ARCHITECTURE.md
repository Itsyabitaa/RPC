# Architecture & Protocol Definition

This document outlines the core architecture and protocol design for our custom Remote Procedure Call (RPC) framework.

## Protocol Structure

We use a custom JSON-based serialization format over TCP sockets to handle request-response communication between the client and server.

### Request Format
When a client makes a remote procedure call, the stub generates a JSON payload representing the request:

```json
{
  "request_id": 1,
  "method": "add",
  "params": [5, 3]
}
```

- **`request_id`**: A unique integer identifying the request. Used by the client to map responses to their corresponding requests.
- **`method`**: A string representing the name of the remote procedure to execute.
- **`params`**: A list of arguments to pass to the method.

### Response Format
When the server finishes processing the request, it returns a JSON payload containing the result or any errors:

```json
{
  "request_id": 1,
  "result": 8,
  "error": null
}
```

- **`request_id`**: Echoed from the request to allow the client to match this response.
- **`result`**: The computed result if the operation was successful.
- **`error`**: A string describing what went wrong, if an exception or error occurred during execution. If successful, this is `null`.

## Supported Data Types

Our custom RPC protocol supports the following basic data types for parameters and return values:

1. **Integer**
2. **String**
3. **Arrays (Lists)**

More complex types will need to be broken down or serialized into these primitive types before transmission.

## RPC Workflow
1. The **Client** calls a local method on the **Stub**.
2. The **Stub** marshals (serializes) the method name and parameters into the JSON **Request Format**.
3. The **Client Transport** layer sends the payload over a TCP socket to the server.
4. The **Server Transport** layer receives the TCP payload and passes it to the **Skeleton**.
5. The **Skeleton** unmarshals (deserializes) the JSON request, identifying the target method and parameters.
6. The **Skeleton** invokes the actual implementation of the method on the **Server**.
7. The method returns a result to the **Skeleton**.
8. The **Skeleton** marshals the result into the JSON **Response Format**.
9. The **Server Transport** sends the response payload back to the client over TCP.
10. The **Client Transport** receives the payload, and the **Stub** unmarshals it.
11. The **Stub** returns the final result to the **Client** application.
