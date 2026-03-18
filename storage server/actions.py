import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    pack_response, 
    pack_download_response,
    unpack_response,
    BYTE_ORDER
)

STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def handle_upload(sock, filename, file_size):
    """Receives a file in chunks and saves it to the local storage."""
    # Path Traversal prevention
    safe_filename = os.path.basename(filename)
    save_path = os.path.join(STORAGE_DIR, safe_filename)
    
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    bytes_received = 0
    try:
        with open(save_path, 'wb') as f:
            while bytes_received < file_size:
                to_read = min(4096, file_size - bytes_received)
                chunk = sock.recv(to_read)
                
                if not chunk:
                    raise Exception("Socket closed during upload")
                    
                f.write(chunk)
                bytes_received += len(chunk)
        
        # After successful writing, send a SUCCESS status code (0)
        sock.sendall(pack_response(0))
        print(f"[+] Saved: {safe_filename} ({file_size} bytes)")
        
    except Exception as e:
        print(f"[!] Upload Error: {e}")
        sock.sendall(pack_response(1)) # Error status

def handle_download(sock, filename):
    """Sends a file from local storage to the client in chunks."""
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(STORAGE_DIR, safe_filename)

    if not os.path.exists(file_path):
        print(f"[!] Download Failed: {safe_filename} not found.")
        sock.sendall(pack_download_response(1, 0)) # Error status
        return

    file_size = os.path.getsize(file_path)
    
    # Send Success Header (Status 0 + File Size)
    sock.sendall(pack_download_response(0, file_size))

    # Stream directly from disk to socket (Memory Efficient)
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
        
        res = sock.recv(1)
        if res:
            status_code = unpack_response(res)
            if status_code == 0:
                print(f"[+] Downloaded: {safe_filename} ({file_size} bytes)")
            else:
                print(f"[!] Client reported error for {safe_filename}")
        else:
            print(f"[!] Client disconnected without confirmation.")
            
    except Exception as e:
        print(f"[!] Download Error: {e}")
