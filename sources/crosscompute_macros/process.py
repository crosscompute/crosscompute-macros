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
    async for x_bytes in p.stdout:
        print(x_bytes.decode(), end='')  # noqa: T201
    output_text = p.stdout.decode()
    if return_code := await p.wait():
        raise ProcessError(return_code=return_code, output_text=output_text)
    return ProcessPack(output_text=output_text)


L = getLogger(__name__)
