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
    pack_response,
    send_packet,
    receive_decrypted_packet
)

# Load encryption key
STORAGE_KEY = getattr(settings, "STORAGE_ENCRYPTION_KEY", "").encode()

def send_file_to_storage(filename: str, file_size: int, file_stream) -> bool:
    """
    Connects to the storage server and streams a file's content.
    Returns True if the storage server confirms successful saving (status 0).
    """

    sha256 = hashlib.sha256()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((settings.STORAGE_SERVER_HOST, settings.STORAGE_SERVER_PORT))

        # Pack and send the encrypted header packet
        header = pack_header(CommandType.UPLOAD, filename, file_size)
        send_packet(sock, header, STORAGE_KEY)

        # Stream the actual file data in 4KB chunks, each encrypted
        while True:
            chunk = file_stream.read(4096)
            if not chunk:
                break

            sha256.update(chunk)
            send_packet(sock, chunk, STORAGE_KEY)

        file_hash = sha256.hexdigest()

        # Receive encrypted acknowledgement
        res = receive_decrypted_packet(sock, STORAGE_KEY)
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
        send_packet(sock, header, STORAGE_KEY)
        
        # Receive encrypted response header
        res_header = receive_decrypted_packet(sock, STORAGE_KEY)
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
                    # Receive encrypted chunk
                    chunk = receive_decrypted_packet(sock, STORAGE_KEY)
                    if not chunk:
                        break

                    sha256.update(chunk)

                    yield chunk
                    bytes_read += len(chunk)

                if bytes_read == file_size:
                    send_packet(sock, pack_response(0), STORAGE_KEY)
                else:
                    send_packet(sock, pack_response(1), STORAGE_KEY)
                    raise StorageServerError()

                actual_hash = sha256.hexdigest()
                if expected_hash != actual_hash:
                    print(f"[!] INTEGRITY ERROR for {filename}!")
                    raise StorageServerError() 

            except Exception as e:
                print(f"[!] Download Error: {e}")
                send_packet(sock, pack_response(1), STORAGE_KEY)
                raise StorageServerError()

            finally:
                sock.close()
                
        return file_generator()

    except Exception as e:
        print(f"[!] Storage Client Error (Download): {e}")
        sock.close()
        raise StorageServerError()

def delete_file_from_storage(filename: str) -> bool:
    """
    Connects to the storage server and requests a file deletion.
    Returns True if the storage server confirms successful deletion (status 0).
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((settings.STORAGE_SERVER_HOST, settings.STORAGE_SERVER_PORT))
        
        # Send Delete Request Header
        header = pack_header(CommandType.DELETE, filename, 0)
        send_packet(sock, header, STORAGE_KEY)
        
        # Receive encrypted acknowledgement
        res = receive_decrypted_packet(sock, STORAGE_KEY)
        if not res:
            return False
            
        status = unpack_response(res)
        return status == 0
    
    except Exception as e:
        print(f"[!] Storage Client Error (Delete): {e}")
        return False
    finally:
        sock.close()
