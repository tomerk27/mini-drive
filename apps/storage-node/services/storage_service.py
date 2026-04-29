"""
Handles UPLOAD, DOWNLOAD, and DELETE commands received from the API server.

All methods read the file fields from the TLV packet, operate on the local
data/ directory, and send back a STATUS response packet when done.
"""

import os
from core.config import settings
from shared.protocol import CommandType, Field, Packet, SecureTransport


class StorageService:
    """Handles the three file operations a storage node can perform."""

    @staticmethod
    def handle_upload(transport: SecureTransport, fields: dict):
        """
        Receives a file in Fernet-encrypted chunks and writes it to disk.

        Strips path separators from the filename to prevent path traversal
        attacks (e.g. an attacker sending filename='../../etc/passwd').
        Sends STATUS=0 on success or STATUS=1 on any error.

        Args:
            transport: Encrypted transport for reading chunks and sending ACK.
            fields: TLV fields from the UPLOAD command header (FILENAME, FILE_SIZE).
        """
        filename = fields.get(Field.FILENAME)
        file_size = fields.get(Field.FILE_SIZE)

        # os.path.basename strips any directory component from the filename,
        # preventing path traversal attacks.
        safe_filename = os.path.basename(filename)
        save_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        os.makedirs(settings.STORAGE_DIR, exist_ok=True)

        bytes_received = 0
        try:
            with open(save_path, 'wb') as f:
                while bytes_received < file_size:
                    chunk = transport.receive_chunk()
                    if not chunk:
                        raise Exception("Stream closed during upload")
                    f.write(chunk)
                    bytes_received += len(chunk)

            res_packet = Packet(CommandType.UPLOAD, {Field.STATUS: 0})
            transport.send_packet(res_packet)
            print(f"[+] Saved: {safe_filename} ({file_size} bytes)")

        except Exception as e:
            print(f"[!] Upload Error: {e}")
            res_packet = Packet(CommandType.UPLOAD, {Field.STATUS: 1})
            transport.send_packet(res_packet)

    @staticmethod
    def handle_download(transport: SecureTransport, fields: dict):
        """
        Reads a file from disk and streams it back in Fernet-encrypted 4 KB chunks.

        Sends a response header first (STATUS + FILE_SIZE), then the data chunks,
        then waits for a final confirmation packet from the client.

        Args:
            transport: Encrypted transport for sending the file and receiving ACK.
            fields: TLV fields from the DOWNLOAD command (FILENAME).
        """
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        if not os.path.exists(file_path):
            print(f"[!] Download Failed: {safe_filename} not found.")
            res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: 1, Field.FILE_SIZE: 0})
            transport.send_packet(res_packet)
            return

        file_size = os.path.getsize(file_path)

        # Send the header so the client knows how many bytes to expect.
        res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: 0, Field.FILE_SIZE: file_size})
        transport.send_packet(res_packet)

        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    transport.send_chunk(chunk)

            # Wait for the client's ACK confirming it received all bytes.
            res = transport.receive_packet()
            if res:
                status_code = res.fields.get(Field.STATUS)
                if status_code == 0:
                    print(f"[+] Downloaded: {safe_filename} ({file_size} bytes)")
                else:
                    print(f"[!] Client reported error for {safe_filename}")
            else:
                print(f"[!] Client disconnected without confirmation.")

        except Exception as e:
            print(f"[!] Download Error: {e}")

    @staticmethod
    def handle_delete(transport: SecureTransport, fields: dict):
        """
        Removes a file from local storage and sends a STATUS response.

        Sends STATUS=0 if the file was deleted, STATUS=1 if not found or on error.

        Args:
            transport: Encrypted transport for sending the result.
            fields: TLV fields from the DELETE command (FILENAME).
        """
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                res_packet = Packet(CommandType.DELETE, {Field.STATUS: 0})
                transport.send_packet(res_packet)
                print(f"[+] Deleted: {safe_filename}")
            else:
                print(f"[!] Delete Failed: {safe_filename} not found.")
                res_packet = Packet(CommandType.DELETE, {Field.STATUS: 1})
                transport.send_packet(res_packet)
        except Exception as e:
            print(f"[!] Delete Error: {e}")
            res_packet = Packet(CommandType.DELETE, {Field.STATUS: 1})
            transport.send_packet(res_packet)
