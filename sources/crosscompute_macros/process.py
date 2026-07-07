import asyncio
import subprocess
from logging import getLogger
from typing import NamedTuple

from .error import ProcessError


class ProcessPack(NamedTuple):
    output_bytes: bytes
    error_bytes: bytes


async def run_process(args, cwd=None, env=None, input_bytes=None):
    kwargs = {}
    if input_bytes:
        kwargs['stdin'] = subprocess.PIPE
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    p = await asyncio.create_subprocess_exec(*args, cwd=cwd, env=env, **kwargs)
    output_bytes, error_bytes = await p.communicate(input_bytes)
    if return_code := p.returncode:
        raise ProcessError(
            return_code=return_code,
            output_bytes=output_bytes,
            error_bytes=error_bytes)
    L.debug(f'run_process {args=} {output_bytes=} {error_bytes=}')
    return ProcessPack(
        output_bytes=output_bytes,
        error_bytes=error_bytes)


L = getLogger(__name__)
