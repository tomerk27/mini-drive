import os
import asyncio
from core.config import settings
from shared.protocol import ( CommandType, Field, Packet, AsyncSecureTransport )

class StorageService:
    @staticmethod
    async def handle_upload(transport: AsyncSecureTransport, fields: dict):
        """Receives a file in encrypted chunks and saves it to the local storage."""
        filename = fields.get(Field.FILENAME)
        file_size = fields.get(Field.FILE_SIZE)

        # Path Traversal prevention
        safe_filename = os.path.basename(filename)
        save_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        os.makedirs(settings.STORAGE_DIR, exist_ok=True)

        bytes_received = 0
        try:
            # We use a thread for file writing to not block the event loop
            # or use a library like aiofiles. For now, standard open is used.
            # In a real system, we should use aiofiles.
            with open(save_path, 'wb') as f:
                while bytes_received < file_size:
                    chunk = await transport.receive_chunk()
                    if not chunk:
                        raise Exception("Stream closed during upload")
                    f.write(chunk)
                    bytes_received += len(chunk)

            # Send ACK
            res_packet = Packet(CommandType.UPLOAD, {Field.STATUS: 0})
            await transport.send_packet(res_packet)
            print(f"[+] Saved: {safe_filename} ({file_size} bytes)")

        except Exception as e:
            print(f"[!] Upload Error: {e}")
            res_packet = Packet(CommandType.UPLOAD, {Field.STATUS: 1})
            await transport.send_packet(res_packet)

    @staticmethod
    async def handle_download(transport: AsyncSecureTransport, fields: dict):
        """Sends a file from local storage to the client in encrypted chunks."""
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        if not os.path.exists(file_path):
            print(f"[!] Download Failed: {safe_filename} not found.")
            res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: 1, Field.FILE_SIZE: 0})
            await transport.send_packet(res_packet)
            return

        file_size = os.path.getsize(file_path)

        # Send Header
        res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: 0, Field.FILE_SIZE: file_size})
        await transport.send_packet(res_packet)

        # Stream directly from disk
        try:
            with open(file_path, 'rb') as f:
                while True:
                    # In a real async system, use aiofiles or run_in_executor
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    await transport.send_chunk(chunk)

            # Wait for confirmation
            res = await transport.receive_packet()
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
    async def handle_delete(transport: AsyncSecureTransport, fields: dict):
        """Deletes a file from local storage."""
        filename = fields.get(Field.FILENAME)
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(settings.STORAGE_DIR, safe_filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                res_packet = Packet(CommandType.DELETE, {Field.STATUS: 0})
                await transport.send_packet(res_packet)
                print(f"[+] Deleted: {safe_filename}")
            else:
                print(f"[!] Delete Failed: {safe_filename} not found.")
                res_packet = Packet(CommandType.DELETE, {Field.STATUS: 1})
                await transport.send_packet(res_packet)
        except Exception as e:
            print(f"[!] Delete Error: {e}")
            res_packet = Packet(CommandType.DELETE, {Field.STATUS: 1})
            await transport.send_packet(res_packet)
