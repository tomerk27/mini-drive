import socket
import os
import sys
import hashlib
from app.core.config import settings
from app.core.exceptions import StorageServerError

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from shared import (
    pack_header, 
    CommandType, 
    unpack_response, 
    unpack_download_response,
    pack_response
)

def send_file_to_storage(filename: str, file_size: int, file_stream) -> bool:
    """
    Connects to the storage server and streams a file's content.
    Returns True if the storage server confirms successful saving (status 0).
    """

    sha256 = hashlib.sha256()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((settings.STORAGE_SERVER_HOST, settings.STORAGE_SERVER_PORT))

        # Pack and send the custom binary header
        header = pack_header(CommandType.UPLOAD, filename, file_size)
        sock.sendall(header)

        # Stream the actual file data in 4KB chunks
        while True:
            chunk = file_stream.read(4096)
            if not chunk:
                break

            sha256.update(chunk)
            sock.sendall(chunk)

        file_hash = sha256.hexdigest()

        # Wait for the server's 1-byte acknowledgment
        res = sock.recv(1)
        if not res:
            return False
            
        status = unpack_response(res)
        return status == 0, file_hash
    
    except Exception as e:
        print(f"[!] Storage Client Error (Upload): {e}")
        return False, None
    finally:
        sock.close()

def get_file_from_storage(filename: str, expected_hash: str):
    """
    Requests a file from the storage server.
    Returns a generator that yields the file's binary chunks.
    """

    sha256 = hashlib.sha256()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((settings.STORAGE_SERVER_HOST, settings.STORAGE_SERVER_PORT))
        
        # Send Download Request Header
        header = pack_header(CommandType.DOWNLOAD, filename, 0)
        sock.sendall(header)
        
        res_header = sock.recv(9)
        if not res_header:
            raise StorageServerError()
            
        status, file_size = unpack_download_response(res_header)
        
        if status != 0:
            print(f"[!] Storage Server returned error status: {status}")
            raise StorageServerError()

        # Stream the file back to the caller
        def file_generator():
            try:
                bytes_read = 0
                while bytes_read < file_size:
                    to_read = min(4096, file_size - bytes_read)
                    chunk = sock.recv(to_read)
                    if not chunk:
                        break

                    sha256.update(chunk)

                    yield chunk
                    bytes_read += len(chunk)

                if bytes_read == file_size:
                    sock.sendall(pack_response(0))
                else:
                    sock.sendall(pack_response(1))
                    raise StorageServerError()

                actual_hash = sha256.hexdigest()
                if expected_hash != actual_hash:
                    print(f"[!] INTEGRITY ERROR for {filename}!")
                    raise StorageServerError() 

            except Exception as e:
                print(f"[!] Download Error: {e}")
                sock.sendall(pack_response(1))
                raise StorageServerError()

            finally:
                sock.close()
                
        return file_generator()

    except Exception as e:
        print(f"[!] Storage Client Error (Download): {e}")
        sock.close()
        raise StorageServerError()
