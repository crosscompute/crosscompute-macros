import socket
from os.path import dirname
from random import randint

from aiofiles import open
from aiohttp.client_exceptions import ClientError

from .disk import (
    make_folder)
from .error import (
    WebConnectionError,
    WebRequestError)


async def upload(
        target_uri, source_path, client_session, chunk_size=1024 * 1024,
        method='PUT'):
    f = getattr(client_session, method.lower())
    try:
        async with f(
            target_uri, data=yield_chunk(source_path, chunk_size),
        ) as response:
            response_status = response.status
            response_text = await response.text()
            if response_status != 200:
                raise WebRequestError(
                    response_text, uri=target_uri, code=response_status)
    except ClientError as e:
        raise WebConnectionError(e, uri=target_uri)
    return response_text


async def download(
        target_path, source_uri, client_session, chunk_size=1024 * 1024):
    try:
        async with client_session.get(source_uri) as response:
            response_status = response.status
            if response_status != 200:
                raise WebRequestError(
                    await response.text(), uri=source_uri,
                    code=response_status)
            await make_folder(dirname(target_path))
            async with open(target_path, mode='wb') as f:
                async for chunk in response.content.iter_chunked(chunk_size):
                    await f.write(chunk)
    except ClientError as e:
        raise WebConnectionError(e, uri=source_uri)


async def make_error(Error, message_text, response=None, error=None):
    error_texts = [message_text]
    kwargs = {}
    if response:
        response_text = (await response.text()).strip()
        if response_text:
            error_texts.append(response_text)
        kwargs['uri'] = response.url
        kwargs['code'] = response.status
    elif error:
        error_text = str(error).strip()
        if error_text:
            error_texts.append(error_text)
        kwargs['uri'] = error.uri
        if hasattr(error, 'code'):
            kwargs['code'] = error.code
    return Error('; '.join(error_texts), **kwargs)


async def yield_chunk(source_path, chunk_size):
    async with open(source_path, mode='rb') as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def escape_quotes_html(x):
    try:
        x = x.replace('"', '&#34;').replace("'", '&#39;')
    except AttributeError:
        pass
    return x


def find_open_port(
        default_port=None,
        minimum_port=1024,
        maximum_port=65535):

    def get_new_port():
        return randint(minimum_port, maximum_port)

    port = default_port or get_new_port()
    port_count = maximum_port - minimum_port + 1
    closed_ports = set()
    while True:
        if not is_port_in_use(port):
            break
        closed_ports.add(port)
        if len(closed_ports) == port_count:
            raise OSError(
                'could not find an open port in '
                f'[{minimum_port}, {maximum_port}]')
        port = get_new_port()
    return port


def is_port_in_use(port):
    # https://stackoverflow.com/a/52872579
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        is_in_use = s.connect_ex(('127.0.0.1', int(port))) == 0
    return is_in_use
