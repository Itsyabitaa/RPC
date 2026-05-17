import socket
import struct
import threading

def send_message(sock, data: bytes):
    """
    Sends a message over a socket, prefixing it with a 4-byte length header.
    """
    # Pack the length of the data as a 4-byte big-endian integer
    length_prefix = struct.pack('>I', len(data))
    sock.sendall(length_prefix + data)

def receive_message(sock) -> bytes:
    """
    Receives a message from a socket that is prefixed with a 4-byte length header.
    Returns None if the connection is closed.
    """
    # Read the 4-byte length prefix
    length_prefix = _recvall(sock, 4)
    if not length_prefix:
        return None
    
    # Unpack the length
    msg_length = struct.unpack('>I', length_prefix)[0]
    
    # Read the exact message length
    data = _recvall(sock, msg_length)
    return data

def _recvall(sock, n) -> bytes:
    """
    Helper function to receive exactly n bytes or return None if EOF is hit.
    """
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)


class RPCServerTransport:
    """
    Handles accepting incoming client connections and spawning a thread for each.
    """
    def __init__(self, host: str, port: int, handler_func):
        self.host = host
        self.port = port
        self.handler_func = handler_func  # Function to call when a message is received
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing the address to avoid 'Address already in use' errors
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_running = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        print(f"[*] Server listening on {self.host}:{self.port}")

        try:
            while self.is_running:
                client_sock, client_addr = self.server_socket.accept()
                print(f"[+] Accepted connection from {client_addr}")
                # Spawn a new thread to handle the client
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, client_addr),
                    daemon=True
                )
                client_thread.start()
        except Exception as e:
            if self.is_running:
                print(f"[-] Server error: {e}")
        finally:
            self.stop()

    def _handle_client(self, client_sock, client_addr):
        try:
            while True:
                data = receive_message(client_sock)
                if data is None:
                    print(f"[-] Connection closed by {client_addr}")
                    break
                
                # Pass data to the handler function and get the response
                response_data = self.handler_func(data)
                
                if response_data:
                    send_message(client_sock, response_data)
        except ConnectionResetError:
            print(f"[-] Connection reset by {client_addr}")
        except Exception as e:
            print(f"[-] Error handling client {client_addr}: {e}")
        finally:
            client_sock.close()

    def stop(self):
        self.is_running = False
        self.server_socket.close()


class RPCClientTransport:
    """
    Handles connecting to the server, sending, and receiving messages.
    """
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f"[*] Connected to {self.host}:{self.port}")

    def send(self, data: bytes):
        if not self.sock:
            raise Exception("Not connected to server")
        send_message(self.sock, data)

    def receive(self) -> bytes:
        if not self.sock:
            raise Exception("Not connected to server")
        return receive_message(self.sock)

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("[*] Connection closed")
