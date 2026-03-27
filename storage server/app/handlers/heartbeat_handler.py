import socket
from app.core.config import settings
from shared.protocol import CommandType, Field, pack, send_packet, receive_decrypted_packet, unpack

class HeartbeatHandler:
    @staticmethod
    def send_heartbeat(capacity: int):
        """Sends a heartbeat packet to the Tracker with the provided capacity."""
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
