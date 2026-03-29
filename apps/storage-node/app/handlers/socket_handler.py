import asyncio
from shared.protocol import AsyncSecureTransport, ProtocolError
from app.handlers.command_router import route_command
from app.core.config import settings

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Handles an individual client connection."""
    address = writer.get_extra_info('peername')
    print(f"[*] Connection from {address[0]}:{address[1]}")
    
    try:
        key = settings.STORAGE_ENCRYPTION_KEY.encode()
        transport = AsyncSecureTransport(reader, writer, key)

        # Receive the first command packet
        packet = await transport.receive_packet()
        if not packet:
            return

        # Route the command
        await route_command(transport, packet)
            
    except ProtocolError as e:
        print(f"[!] Protocol Error handling client {address}: {e}")
    except Exception as e:
        print(f"[!] Error handling client {address}: {e}")
    finally:
        print(f"[*] Closing connection with {address[0]}")
        writer.close()
        try:
            await writer.wait_closed()
        except:
            pass
