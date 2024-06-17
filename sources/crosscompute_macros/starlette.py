import asyncio
from logging import getLogger

from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect


class TemplateResponseFactory(Jinja2Templates):

    def __init__(self, environment, context_processors=None):
        'Assume nothing about the template environment'
        self.env = environment
        self.context_processors = context_processors or []


async def yield_bytes_while_connected(websocket, timeout_in_seconds):
    while True:
        try:
            received_bytes = await asyncio.wait_for(
                websocket.receive_bytes(), timeout=timeout_in_seconds)
        except KeyError:
            L.warning('server received and discarded non byte data')
        except TimeoutError:
            yield
        except RuntimeError:
            break
        except WebSocketDisconnect:
            break
        else:
            yield received_bytes


L = getLogger(__name__)
