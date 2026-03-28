from shared.protocol import ( CommandType, Field, pack, unpack, send_packet, receive_decrypted_packet )
from storage_engine.tracker.connection_pool import connection_pool

class StorageClient:
    """
    Low-level driver for communicating with a Storage Node over TCP sockets.
    Instead of connecting, it fetches an active socket from the ConnectionPool.
    """
    def __init__(self, node_id: str, encryption_key: bytes):
        self.node_id = node_id
        self.key = encryption_key

    def _get_socket(self):
        sock = connection_pool.get_node_socket(self.node_id)
        if not sock:
            raise ConnectionError(f"Node {self.node_id} is not connected to the Main Server.")
        return sock

    def upload(self, filename: str, file_size: int, file_stream) -> bool:
        """Streams a file through the persistent node socket."""
        sock = self._get_socket()
        try:
            # Send Header
            header = pack(CommandType.UPLOAD, {
                Field.FILENAME: filename,
                Field.FILE_SIZE: file_size
            })
            send_packet(sock, header, self.key)

            # Stream chunks
            while True:
                chunk = file_stream.read(4096)
                if not chunk:
                    break
                send_packet(sock, chunk, self.key)

            # Wait for ACK
            res = receive_decrypted_packet(sock, self.key)
            if not res:
                return False
            
            _, fields = unpack(res)
            return fields.get(Field.STATUS) == 0
        except Exception as e:
            print(f"[!] StorageClient Upload Error for {self.node_id}: {e}")
            connection_pool.remove_node(self.node_id)
            return False

    def download_generator(self, filename: str):
        """Returns a generator that yields binary chunks through the persistent node socket."""
        sock = self._get_socket()
        try:
            # Send Download Request
            header = pack(CommandType.DOWNLOAD, {Field.FILENAME: filename})
            send_packet(sock, header, self.key)
            
            # Receive response header
            res_header = receive_decrypted_packet(sock, self.key)
            if not res_header:
                return None, 0
                
            _, fields = unpack(res_header)
            status = fields.get(Field.STATUS)
            file_size = fields.get(Field.FILE_SIZE)

            if status != 0:
                return None, 0

            def chunk_generator():
                try:
                    bytes_read = 0
                    while bytes_read < file_size:
                        chunk = receive_decrypted_packet(sock, self.key)
                        if not chunk:
                            break
                        yield chunk
                        bytes_read += len(chunk)

                    # Send final ACK/NACK
                    status_code = 0 if bytes_read == file_size else 1
                    res_packet = pack(CommandType.DOWNLOAD, {Field.STATUS: status_code})
                    send_packet(sock, res_packet, self.key)
                except Exception as e:
                    print(f"[!] Download Stream Error for {self.node_id}: {e}")
                    connection_pool.remove_node(self.node_id)
                    raise

            return chunk_generator(), file_size
        except Exception:
            connection_pool.remove_node(self.node_id)
            raise

    def delete(self, filename: str) -> bool:
        """Requests a file deletion through the persistent node socket."""
        sock = self._get_socket()
        try:
            header = pack(CommandType.DELETE, {Field.FILENAME: filename})
            send_packet(sock, header, self.key)
            
            res = receive_decrypted_packet(sock, self.key)
            if not res:
                return False
                
            _, fields = unpack(res)
            return fields.get(Field.STATUS) == 0
        except Exception as e:
            print(f"[!] StorageClient Delete Error for {self.node_id}: {e}")
            connection_pool.remove_node(self.node_id)
            return False