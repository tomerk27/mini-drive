import os
from app.core.config import settings
from shared.protocol import (
    CommandType,
    Field,
    pack,
    unpack,
    send_packet,
    receive_decrypted_packet
)

class StorageService:
    @staticmethod
    def handle_upload(sock, fields: dict):
        """Receives a file in encrypted chunks and saves it to the local storage."""
        filename = fields.get(Field.FILENAME)
        file_size = fields.get(Field.FILE_SIZE)

        # Path Traversal prevention
        safe_filename = os.path.basename(filename)
        save_path = os.path.join(settings.STORAGE_DIR, safe_filename)
        
        os.makedirs(settings.STORAGE_DIR, exist_ok=True)
        
        bytes_received = 0
        try:
            with open(save_path, 'wb') as f:
                while bytes_received < file_size:
                    # Receive encrypted chunk
                    chunk = receive_decrypted_packet(sock, settings.STORAGE_ENCRYPTION_KEY)
                    
                    if not chunk:
                        raise Exception("Socket closed during upload")
                        
                    f.write(chunk)
                    bytes_received += len(chunk)
            
            # After successful writing, send an encrypted SUCCESS status code (0)
            res_packet = pack(CommandType.UPLOAD, {Field.STATUS: 0})
            send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY)
            print(f"[+] Saved: {safe_filename} ({file_size} bytes)")
            
        except Exception as e:
            print(f"[!] Upload Error: {e}")
            res_packet = pack(CommandType.UPLOAD, {Field.STATUS: 1})
            send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY) # Error status

    @staticmethod
    def handle_download(sock, fields: dict):
        """Sends a file from local storage to the client in encrypted chunks."""
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        if not os.path.exists(file_path):
            print(f"[!] Download Failed: {safe_filename} not found.")
            res_packet = pack(CommandType.DOWNLOAD, {Field.STATUS: 1, Field.FILE_SIZE: 0})
            send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY) # Error status
            return

        file_size = os.path.getsize(file_path)
        
        # Send Encrypted Success Header (Status 0 + File Size)
        res_packet = pack(CommandType.DOWNLOAD, {Field.STATUS: 0, Field.FILE_SIZE: file_size})
        send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY)

        # Stream directly from disk to socket, encrypting each chunk
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    send_packet(sock, chunk, settings.STORAGE_ENCRYPTION_KEY)
            
            # Receive encrypted confirmation
            res = receive_decrypted_packet(sock, settings.STORAGE_ENCRYPTION_KEY)
            if res:
                _, res_fields = unpack(res)
                status_code = res_fields.get(Field.STATUS)
                if status_code == 0:
                    print(f"[+] Downloaded: {safe_filename} ({file_size} bytes)")
                else:
                    print(f"[!] Client reported error for {safe_filename}")
            else:
                print(f"[!] Client disconnected without confirmation.")
                
        except Exception as e:
            print(f"[!] Download Error: {e}")

    @staticmethod
    def handle_delete(sock, fields: dict):
        """Deletes a file from local storage."""
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                res_packet = pack(CommandType.DELETE, {Field.STATUS: 0})
                send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY) # Success
                print(f"[+] Deleted: {safe_filename}")
            else:
                print(f"[!] Delete Failed: {safe_filename} not found.")
                res_packet = pack(CommandType.DELETE, {Field.STATUS: 1})
                send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY) # Error: Not found
        except Exception as e:
            print(f"[!] Delete Error: {e}")
            res_packet = pack(CommandType.DELETE, {Field.STATUS: 1})
            send_packet(sock, res_packet, settings.STORAGE_ENCRYPTION_KEY)