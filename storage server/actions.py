import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    pack_response, 
    pack_download_response,
    unpack_response,
    send_packet,
    receive_decrypted_packet
)

STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def handle_upload(sock, filename, file_size, key):
    """Receives a file in encrypted chunks and saves it to the local storage."""
    # Path Traversal prevention
    safe_filename = os.path.basename(filename)
    save_path = os.path.join(STORAGE_DIR, safe_filename)
    
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    bytes_received = 0
    try:
        with open(save_path, 'wb') as f:
            while bytes_received < file_size:
                # Receive encrypted chunk
                chunk = receive_decrypted_packet(sock, key)
                
                if not chunk:
                    raise Exception("Socket closed during upload")
                    
                f.write(chunk)
                bytes_received += len(chunk)
        
        # After successful writing, send an encrypted SUCCESS status code (0)
        send_packet(sock, pack_response(0), key)
        print(f"[+] Saved: {safe_filename} ({file_size} bytes)")
        
    except Exception as e:
        print(f"[!] Upload Error: {e}")
        send_packet(sock, pack_response(1), key) # Error status

def handle_download(sock, filename, key):
    """Sends a file from local storage to the client in encrypted chunks."""
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(STORAGE_DIR, safe_filename)

    if not os.path.exists(file_path):
        print(f"[!] Download Failed: {safe_filename} not found.")
        send_packet(sock, pack_download_response(1, 0), key) # Error status
        return

    file_size = os.path.getsize(file_path)
    
    # Send Encrypted Success Header (Status 0 + File Size)
    send_packet(sock, pack_download_response(0, file_size), key)

    # Stream directly from disk to socket, encrypting each chunk
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                send_packet(sock, chunk, key)
        
        # Receive encrypted confirmation
        res = receive_decrypted_packet(sock, key)
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