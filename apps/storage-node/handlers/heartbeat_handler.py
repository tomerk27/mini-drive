import asyncio
from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport

class HeartbeatHandler:
    @staticmethod
    async def send_heartbeat(capacity: int):
        """Sends a heartbeat packet to the Tracker with the provided capacity."""
        key = settings.STORAGE_ENCRYPTION_KEY.encode()
        packet = Packet(CommandType.HEARTBEAT, {
            Field.NODE_ID: settings.NODE_ID,
            Field.NODE_PORT: settings.PORT,
            Field.CAPACITY: capacity
        })

        try:
            reader, writer = await asyncio.open_connection(settings.TRACKER_HOST, settings.TRACKER_PORT)
            transport = AsyncSecureTransport(reader, writer, key)

            await transport.send_packet(packet)

            # Wait for acknowledgment
            res = await transport.receive_packet()
            if res:
                if res.fields.get(Field.STATUS) == 0:
                    print(f"[*] Heartbeat confirmed by Tracker")

            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"[!] Tracker unreachable: {e}")
