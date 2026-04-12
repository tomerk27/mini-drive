import asyncio
import os
import sys

# Add project root and libs to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "libs"))

from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport
from handlers.heartbeat_handler import HeartbeatHandler
from services.system_metrics_service import SystemMetricsService
from handlers.command_router import route_command

async def heartbeat_loop():
    """Background task to send heartbeats every 30 seconds."""
    print(f"[*] Starting Heartbeat loop for {settings.NODE_ID}...")
    while True:
        try:
            free_space = SystemMetricsService.get_free_space()
            await HeartbeatHandler.send_heartbeat(free_space)
        except Exception as e:
            print(f"[!] Heartbeat Error: {e}")
        await asyncio.sleep(30)

async def connect_to_main_server():
    """
    Acts as a Worker: Connects to the Main Server and waits for commands.
    """
    key = settings.STORAGE_ENCRYPTION_KEY.encode()
    
    while True:
        try:
            print(f"[*] Attempting to connect to Main Server at {settings.TRACKER_HOST}:9000...")
            reader, writer = await asyncio.open_connection(settings.TRACKER_HOST, 9000)
            transport = AsyncSecureTransport(reader, writer, key)
            
            # Registration
            reg_packet = Packet(CommandType.REGISTER, {Field.NODE_ID: settings.NODE_ID})
            await transport.send_packet(reg_packet)
            
            print(f"[+] Successfully connected and registered as {settings.NODE_ID}")
            
            # Stay connected and handle incoming commands from the Main Server
            while True:
                packet = await transport.receive_packet()
                if not packet:
                    print("[!] Connection closed by Main Server.")
                    break
                
                # Process the command
                await route_command(transport, packet)
                
        except Exception as e:
            print(f"[!] Connection failed: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass

async def main():
    # Start the heartbeat in the background
    asyncio.create_task(heartbeat_loop())
    
    # Start the main worker connection
    await connect_to_main_server()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
