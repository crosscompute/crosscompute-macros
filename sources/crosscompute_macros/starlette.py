import asyncio
import json
from logging import getLogger

from starlette.templating import Jinja2Templates


class TemplateResponseFactory(Jinja2Templates):

    def __init__(self, environment, context_processors=None):
        'Assume nothing about the template environment'
        self.env = environment
        self.context_processors = context_processors or []


async def yield_dictionary_while_connected(websocket, timeout_in_seconds=1):
    async for x in yield_packet_while_connected(websocket, timeout_in_seconds):
        if x and 'text' in x:
            x = json.loads(x['text'])
        else:
            x = {}
        yield x


async def yield_packet_while_connected(websocket, timeout_in_seconds=1):
    while True:
        try:
            packet = await asyncio.wait_for(
                websocket.receive(), timeout=timeout_in_seconds)
            if packet['type'] == 'websocket.disconnect':
                break
        except TimeoutError:
            yield
        except RuntimeError:
            break
        else:
            yield packet


L = getLogger(__name__)
