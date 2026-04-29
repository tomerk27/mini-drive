"""
Synchronous driver for sending UPLOAD/DOWNLOAD/DELETE commands to a storage node.

Retrieves the node's persistent socket from the ConnectionPool and acquires a
per-node lock before each operation so concurrent requests don't interleave
their bytes on the same socket.
"""

import socket
import threading
from typing import Optional, Tuple
from shared.protocol import CommandType, Field, Packet, SecureTransport, ProtocolError
from gateways.storage.servers.connection_pool import connection_pool

# Errors that mean the TCP connection is dead and must be removed from the pool.
_FATAL_CONNECTION_ERRORS = (OSError, EOFError, ConnectionResetError, BrokenPipeError)


class StorageClient:
    """
    Synchronous driver for communicating with a Storage Node over a persistent TCP socket.

    Acquires a per-node lock before each operation to prevent concurrent stream
    corruption when multiple threads try to use the same socket simultaneously.

    Args:
        node_id: Identifies which node socket to pull from the ConnectionPool.
        encryption_key: Fernet key used to encrypt/decrypt all traffic.
    """

    def __init__(self, node_id: str, encryption_key: bytes):
        self.node_id = node_id
        self.key = encryption_key

    def _get_socket_and_lock(self) -> Tuple[socket.socket, threading.Lock]:
        """
        Retrieves the socket and lock for this node from the ConnectionPool.

        Raises:
            ConnectionError: If the node isn't currently registered (not connected).
        """
        sock = connection_pool.get_node_socket(self.node_id)
        lock = connection_pool.get_node_lock(self.node_id)
        if not sock or not lock:
            raise ConnectionError(f"Node {self.node_id} is not connected to the main server.")
        return sock, lock

    def upload(self, filename: str, file_size: int, file_stream) -> bool:
        """
        Sends an UPLOAD command followed by the file bytes in 4 KB chunks.

        Args:
            filename: Physical name to store the file as on the node.
            file_size: Total byte count (sent in the header so the node knows when to stop).
            file_stream: File-like object to read data from.

        Returns:
            True if the node confirmed a successful write (STATUS == 0).
        """
        sock, lock = self._get_socket_and_lock()
        with lock:
            transport = SecureTransport(sock, self.key)
            try:
                # Send the metadata header first so the node can prepare to receive.
                header = Packet(CommandType.UPLOAD, {
                    Field.FILENAME: filename,
                    Field.FILE_SIZE: file_size
                })
                transport.send_packet(header)

                # Stream the file content in small chunks to keep memory usage low.
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
        """
        Sends a DOWNLOAD command and reads back the file bytes.

        The node first sends a header with status and file size, then streams
        the data. After receiving all chunks, this client sends a confirmation
        packet so the node knows whether the transfer was complete.

        Args:
            filename: Physical name of the file on the node.

        Returns:
            The complete file bytes if successful, or None on failure.
        """
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

                # Read chunks until we've accumulated the expected number of bytes.
                data = b""
                while len(data) < file_size:
                    chunk = transport.receive_chunk()
                    if not chunk:
                        break
                    data += chunk

                # Send STATUS=0 if we received all bytes, 1 if we got a short read.
                status_code = 0 if len(data) == file_size else 1
                transport.send_packet(Packet(CommandType.DOWNLOAD, {Field.STATUS: status_code}))

                return data if len(data) == file_size else None
            except Exception as e:
                print(f"[!] StorageClient Download Error for {self.node_id}: {e}")
                if isinstance(e, _FATAL_CONNECTION_ERRORS):
                    connection_pool.remove_node(self.node_id)
                return None

    def delete(self, filename: str) -> bool:
        """
        Sends a DELETE command and waits for the node's acknowledgment.

        Args:
            filename: Physical name of the file to delete on the node.

        Returns:
            True if the node confirmed deletion (STATUS == 0).
        """
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
                # Any error on DELETE likely means a dead connection — remove it.
                connection_pool.remove_node(self.node_id)
                return False
