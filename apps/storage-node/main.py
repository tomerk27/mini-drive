"""
CyberDrive Storage Node entry point.

This process connects to the API server's DataServer (port 9000) and waits
for UPLOAD / DOWNLOAD / DELETE commands over an encrypted persistent TCP
connection. A separate background task fires heartbeats to the Tracker
(port 9001) every 30 seconds so the API server knows this node is alive.
"""

import asyncio
import os
import sys

# Add project root and libs to sys.path so shared protocol can be imported.
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "libs"))

from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport
from handlers.heartbeat_handler import HeartbeatHandler
from services.system_metrics_service import SystemMetricsService
from handlers.command_router import route_command


async def heartbeat_loop():
    """Background task: reports free disk space to the Tracker every 30 seconds."""
    print(f"[*] Starting Heartbeat loop for {settings.NODE_ID}...")
    while True:
        try:
            free_space = SystemMetricsService.get_free_space()
            await HeartbeatHandler.send_heartbeat(free_space)
        except Exception as e:
            print(f"[!] Heartbeat Error: {e}")
        await asyncio.sleep(30)


def _enable_keepalive(sock):
    """
    Enables TCP keep-alive on the given socket to detect stale connections.

    Without this, a silently dropped connection would appear open indefinitely,
    causing the storage node to block waiting for data that never arrives.
    """
    import socket as _socket
    sock.setsockopt(_socket.SOL_SOCKET, _socket.SO_KEEPALIVE, 1)
    if hasattr(_socket, "TCP_KEEPIDLE"):
        # Start probing after 60 s of silence.
        sock.setsockopt(_socket.IPPROTO_TCP, _socket.TCP_KEEPIDLE, 60)
    if hasattr(_socket, "TCP_KEEPINTVL"):
        # Send a probe every 10 s after the first failure.
        sock.setsockopt(_socket.IPPROTO_TCP, _socket.TCP_KEEPINTVL, 10)
    if hasattr(_socket, "TCP_KEEPCNT"):
        # Declare the connection dead after 5 failed probes.
        sock.setsockopt(_socket.IPPROTO_TCP, _socket.TCP_KEEPCNT, 5)


async def connect_to_main_server():
    """
    Main worker loop: connects to the API server DataServer and processes commands.

    On connection, sends a REGISTER packet so the API server can route future
    UPLOAD/DOWNLOAD/DELETE commands back to this specific node. Reconnects
    automatically after any failure or dropped connection.
    """
    key = settings.STORAGE_ENCRYPTION_KEY.encode()

    while True:
        try:
            print(f"[*] Attempting to connect to Main Server at {settings.TRACKER_HOST}:9000...")
            reader, writer = await asyncio.open_connection(settings.TRACKER_HOST, 9000)
            _enable_keepalive(writer.get_extra_info("socket"))
            transport = AsyncSecureTransport(reader, writer, key)

            # Identify this node to the DataServer immediately after connecting.
            reg_packet = Packet(CommandType.REGISTER, {Field.NODE_ID: settings.NODE_ID})
            await transport.send_packet(reg_packet)

            print(f"[+] Successfully connected and registered as {settings.NODE_ID}")

            # Block here, handling one command at a time until the connection drops.
            while True:
                packet = await transport.receive_packet()
                if not packet:
                    print("[!] Connection closed by Main Server. Retrying in 3 seconds...")
                    await asyncio.sleep(3)
                    break

                await route_command(transport, packet)

        except Exception as e:
            print(f"[!] Connection failed: {e}. Retrying in 3 seconds...")
            await asyncio.sleep(3)
        finally:
            # Always try to close the writer cleanly to free the OS socket.
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass


async def main():
    """Entry point: starts heartbeat loop then enters the command worker loop."""
    # Run heartbeat as a background task alongside the main connection loop.
    asyncio.create_task(heartbeat_loop())
    await connect_to_main_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
