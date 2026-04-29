"""
Handles outgoing heartbeat packets from the storage node to the API server's Tracker.
"""

import asyncio
from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport


class HeartbeatHandler:
    """Sends a single heartbeat to the Tracker each time it is called."""

    @staticmethod
    async def send_heartbeat(capacity: int):
        """
        Opens a short-lived connection to the Tracker and sends one HEARTBEAT packet.

        The heartbeat carries the node's ID, port, and current free disk space
        so the Tracker can update the node's record and select it for file placement.
        A new connection is opened each time (not reused) because the Tracker
        closes the connection after handling each heartbeat.

        Args:
            capacity: Free disk space in bytes, reported to the API server.
        """
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

            # Wait for the Tracker's ACK before closing.
            res = await transport.receive_packet()
            if res:
                if res.fields.get(Field.STATUS) == 0:
                    print(f"[*] Heartbeat confirmed by Tracker")

            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"[!] Tracker unreachable: {e}")
