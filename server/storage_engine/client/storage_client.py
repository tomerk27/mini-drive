import socket
from shared.protocol import (
    CommandType,
    Field,
    pack,
    unpack,
    send_packet,
    receive_decrypted_packet
)

class StorageClient:
    """
    Low-level driver for communicating with a Storage Node over TCP sockets.
    Handles protocol packing, encryption, and raw byte streaming using generic TLV.
    """
    def __init__(self, host: str, port: int, encryption_key: bytes):
        self.host = host
        self.port = port
        self.key = encryption_key

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def upload(self, filename: str, file_size: int, file_stream) -> bool:
        """Streams a file to the storage node."""
        sock = self._connect()
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
        finally:
            sock.close()

    def download_generator(self, filename: str):
        """Returns a generator that yields binary chunks from the storage node."""
        sock = self._connect()
        try:
            # Send Download Request
            header = pack(CommandType.DOWNLOAD, {Field.FILENAME: filename})
            send_packet(sock, header, self.key)
            
            # Receive response header
            res_header = receive_decrypted_packet(sock, self.key)
            if not res_header:
                sock.close()
                return None, 0
                
            _, fields = unpack(res_header)
            status = fields.get(Field.STATUS)
            file_size = fields.get(Field.FILE_SIZE)

            if status != 0:
                sock.close()
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
                finally:
                    sock.close()

            return chunk_generator(), file_size
        except Exception:
            sock.close()
            raise

    def delete(self, filename: str) -> bool:
        """Requests a file deletion from the storage node."""
        sock = self._connect()
        try:
            header = pack(CommandType.DELETE, {Field.FILENAME: filename})
            send_packet(sock, header, self.key)
            
            res = receive_decrypted_packet(sock, self.key)
            if not res:
                return False
                
            _, fields = unpack(res)
            return fields.get(Field.STATUS) == 0
        finally:
            sock.close()
