import asyncio
from logging import getLogger

from starlette.websockets import WebSocketDisconnect


async def yield_bytes_while_connected(websocket, timeout_in_seconds):
    while True:
        try:
            received_bytes = await asyncio.wait_for(
                websocket.receive_bytes(), timeout=timeout_in_seconds)
        except KeyError:
            L.warning('server received and discarded non byte data')
        except TimeoutError:
            yield
        except WebSocketDisconnect:
            break
        else:
            yield received_bytes


L = getLogger(__name__)
