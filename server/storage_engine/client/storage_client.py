import socket
from shared import (
    pack_header, 
    CommandType, 
    unpack_response, 
    unpack_download_response,
    pack_response,
    send_packet,
    receive_decrypted_packet
)

class StorageClient:
    """
    Low-level driver for communicating with a Storage Node over TCP sockets.
    Handles protocol packing, encryption, and raw byte streaming.
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
            header = pack_header(CommandType.UPLOAD, filename, file_size)
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
            
            return unpack_response(res) == 0
        finally:
            sock.close()

    def download_generator(self, filename: str):
        """Returns a generator that yields binary chunks from the storage node."""
        sock = self._connect()
        try:
            # Send Download Request
            header = pack_header(CommandType.DOWNLOAD, filename, 0)
            send_packet(sock, header, self.key)
            
            # Receive response header
            res_header = receive_decrypted_packet(sock, self.key)
            if not res_header:
                sock.close()
                return None, 0
                
            status, file_size = unpack_download_response(res_header)
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
                    if bytes_read == file_size:
                        send_packet(sock, pack_response(0), self.key)
                    else:
                        send_packet(sock, pack_response(1), self.key)
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
            header = pack_header(CommandType.DELETE, filename, 0)
            send_packet(sock, header, self.key)
            
            res = receive_decrypted_packet(sock, self.key)
            if not res:
                return False
                
            return unpack_response(res) == 0
        finally:
            sock.close()
