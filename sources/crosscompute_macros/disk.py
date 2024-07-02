import json
from os.path import dirname, join

from aiofiles import open, os

from .error import DiskError
from .iterable import LRUDict
from .log import redact_path


class FileCache(LRUDict):

    def __init__(self, *args, load, length: int, **kwargs):
        super().__init__(*args, length=length, **kwargs)
        self._load = load

    async def set(self, path, d):
        t = await get_modification_time(path)
        value = t, d
        super().__setitem__(str(path), value)

    async def get(self, path):
        path = str(path)
        if path in self:
            old_t, d = super().__getitem__(path)
            new_t = await get_modification_time(path)
            if old_t == new_t:
                return d
        x = await self._load(path)
        await self.set(path, x)
        return x


async def make_folder(folder):
    await os.makedirs(folder, exist_ok=True)
    return folder


async def copy_path(target_path, source_path):
    byte_count = await get_byte_count(source_path)
    async with open(
        target_path, mode='wb',
    ) as t, open(
        source_path, mode='rb',
    ) as s:
        await os.sendfile(t.fileno(), s.fileno(), 0, byte_count)
    return target_path


async def get_byte_count(path):
    s = await os.stat(path)
    return s.st_size


async def save_raw_text(path, text):
    async with open(path, mode='wt') as f:
        await f.write(text)
    return path


async def load_raw_text(path):
    async with open(path, mode='rt') as f:
        text = await f.read()
    return text.rstrip()


async def save_raw_json(path, dictionary):
    await make_folder(path.parent)
    async with open(path, mode='wt') as f:
        await f.write(json.dumps(dictionary))
    return path


async def load_raw_json(path):
    async with open(path, mode='rt') as f:
        dictionary = json.loads(await f.read())
    return dictionary


async def update_raw_json(path, dictionary):
    async with open(path, mode='r+t') as f:
        d = json.loads(await f.read())
        d.update(dictionary)
        await f.seek(0)
        await f.write(json.dumps(d))
        await f.truncate()


async def make_link(target_path, source_path):
    await os.symlink(source_path, target_path)


async def get_real_path(path):
    path = await os.path.abspath(path)
    original_path = path
    paths = [path]
    while await is_link_path(path):
        path = await os.path.abspath(join(dirname(path), await os.readlink(
            path)))
        if path in paths:
            raise OSError(
                f'path "{redact_path(original_path)}" is a circular symlink')
        paths.append(path)
    return path


async def assert_path_is_in_folder(path, folder):
    try:
        path = await get_real_path(path)
        folder = await get_real_path(folder)
    except OSError as e:
        raise DiskError(e)
    try:
        assert path.startswith(folder)
    except AssertionError as e:
        raise DiskError(e)


get_modification_time = os.path.getmtime
is_existing_path = os.path.exists
is_file_path = os.path.isfile
is_folder_path = os.path.isdir
is_link_path = os.path.islink
is_same_path = os.path.samefile
list_paths = os.listdir
remove_path = os.unlink
