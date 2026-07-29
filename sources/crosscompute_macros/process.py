import asyncio
import subprocess
from logging import getLogger
from typing import NamedTuple

from .error import ProcessError


class ProcessPack(NamedTuple):
    output_text: str


async def run_process(args, cwd=None, env=None, input_text=None):
    L.info('run_process {args=}')
    kwargs = {}
    if input_text:
        kwargs['stdin'] = subprocess.PIPE
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.STDOUT
    p = await asyncio.create_subprocess_exec(*args, cwd=cwd, env=env, **kwargs)
    if input_text:
        input_bytes = input_text.encode() if input_text else None
        p.stdin.write(input_bytes)
        await p.stdin.drain()
        p.stdin.close()
    x_texts = []
    async for x_bytes in p.stdout:
        x_text = x_bytes.decode()
        print(x_text, end='')  # noqa: T201
        x_texts.append(x_text)
    output_text = ''.join(x_texts)
    if return_code := await p.wait():
        raise ProcessError(return_code=return_code, output_text=output_text)
    return ProcessPack(output_text=output_text)


L = getLogger(__name__)
