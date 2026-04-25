import socket
import threading
from typing import Optional, Tuple
from shared.protocol import CommandType, Field, Packet, SecureTransport, ProtocolError
from gateways.storage.servers.connection_pool import connection_pool

_FATAL_CONNECTION_ERRORS = (OSError, EOFError, ConnectionResetError, BrokenPipeError)


class StorageClient:
    """
    Synchronous driver for communicating with a Storage Node over a persistent TCP socket.
    Acquires a per-node lock before each operation to prevent concurrent stream corruption.
    """
    def __init__(self, node_id: str, encryption_key: bytes):
        self.node_id = node_id
        self.key = encryption_key

    def _get_socket_and_lock(self) -> Tuple[socket.socket, threading.Lock]:
        sock = connection_pool.get_node_socket(self.node_id)
        lock = connection_pool.get_node_lock(self.node_id)
        if not sock or not lock:
            raise ConnectionError(f"Node {self.node_id} is not connected to the main server.")
        return sock, lock

    def upload(self, filename: str, file_size: int, file_stream) -> bool:
        sock, lock = self._get_socket_and_lock()
        with lock:
            transport = SecureTransport(sock, self.key)
            try:
                header = Packet(CommandType.UPLOAD, {
                    Field.FILENAME: filename,
                    Field.FILE_SIZE: file_size
                })
                transport.send_packet(header)

                while True:
                    chunk = file_stream.read(4096)
                    if not chunk:
                        break
                    transport.send_chunk(chunk)

                res = transport.receive_packet()
                if not res:
                    return False
                return res.fields.get(Field.STATUS) == 0
            except Exception as e:
                print(f"[!] StorageClient Upload Error for {self.node_id}: {e}")
                if isinstance(e, _FATAL_CONNECTION_ERRORS):
                    connection_pool.remove_node(self.node_id)
                return False

    def download(self, filename: str) -> Optional[bytes]:
        sock, lock = self._get_socket_and_lock()
        with lock:
            transport = SecureTransport(sock, self.key)
            try:
                header = Packet(CommandType.DOWNLOAD, {Field.FILENAME: filename})
                transport.send_packet(header)

                res_header = transport.receive_packet()
                if not res_header:
                    return None

                status = res_header.fields.get(Field.STATUS)
                file_size = res_header.fields.get(Field.FILE_SIZE)

                if status != 0:
                    return None

                data = b""
                while len(data) < file_size:
                    chunk = transport.receive_chunk()
                    if not chunk:
                        break
                    data += chunk

                status_code = 0 if len(data) == file_size else 1
                transport.send_packet(Packet(CommandType.DOWNLOAD, {Field.STATUS: status_code}))

                return data if len(data) == file_size else None
            except Exception as e:
                print(f"[!] StorageClient Download Error for {self.node_id}: {e}")
                if isinstance(e, _FATAL_CONNECTION_ERRORS):
                    connection_pool.remove_node(self.node_id)
                return None

    def delete(self, filename: str) -> bool:
        sock, lock = self._get_socket_and_lock()
        with lock:
            transport = SecureTransport(sock, self.key)
            try:
                header = Packet(CommandType.DELETE, {Field.FILENAME: filename})
                transport.send_packet(header)

                res = transport.receive_packet()
                if not res:
                    return False
                return res.fields.get(Field.STATUS) == 0
            except Exception as e:
                print(f"[!] StorageClient Delete Error for {self.node_id}: {e}")
                connection_pool.remove_node(self.node_id)
                return False
