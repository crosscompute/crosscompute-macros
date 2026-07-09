import asyncio
import subprocess
from logging import getLogger
from typing import NamedTuple

from .error import ProcessError


class ProcessPack(NamedTuple):
    output_text: str
    error_text: str


async def run_process(args, cwd=None, env=None, input_text=None):
    kwargs = {}
    if input_text:
        kwargs['stdin'] = subprocess.PIPE
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    p = await asyncio.create_subprocess_exec(*args, cwd=cwd, env=env, **kwargs)
    output_bytes, error_bytes = await p.communicate(
        input_text.encode() if input_text else None)
    output_text = output_bytes.decode()
    error_text = error_bytes.decode()
    return_code = p.returncode
    lines = [f'run_process {args=} {return_code=}']
    if output_text:
        lines.extend(['# stdout', output_text])
    if error_text:
        lines.extend(['# stderr', error_text])
    L.debug('\n'.join(lines))
    if return_code:
        raise ProcessError(
            return_code=return_code,
            output_text=output_text,
            error_text=error_text)
    return ProcessPack(
        output_text=output_text,
        error_text=error_text)


L = getLogger(__name__)
