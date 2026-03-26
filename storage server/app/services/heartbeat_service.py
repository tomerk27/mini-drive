import socket
import shutil
import time
from app.core.config import settings
from shared.protocol import CommandType, Field, pack, send_packet, receive_decrypted_packet, unpack

class HeartbeatHandler:     
    @staticmethod     
    def send_pulse():
         """The single action of sending one heartbeat."""
         capacity = shutil.disk_usage(settings.STORAGE_DIR).free
         key = settings.STORAGE_ENCRYPTION_KEY.encode()

         packet = pack(CommandType.HEARTBEAT, {
             Field.NODE_ID: settings.NODE_ID,
             Field.NODE_PORT: settings.PORT,
             Field.CAPACITY: capacity
         })

         try:
             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                 sock.settimeout(5)
                 sock.connect((settings.TRACKER_HOST, settings.TRACKER_PORT))
                 send_packet(sock, packet, key)

                 # Wait for acknowledgment
                 res = receive_decrypted_packet(sock, key)
                 if res:
                     _, fields = unpack(res)
                     if fields.get(Field.STATUS) == 0:
                         print(f"[*] Heartbeat confirmed by Tracker")
         except Exception as e:
             print(f"[!] Tracker unreachable: {e}")

    @classmethod
    def start_pulse_loop(cls):
        """The background loop that keeps the node alive."""
        print(f"[*] Starting Heartbeat loop for {settings.NODE_ID}...")
        while True:
            cls.send_pulse()
            time.sleep(30) # Wait 30 seconds