import aiofiles
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from .error import DiskError, FormattingError, ParsingError


async def load_raw_yaml(path, with_comments=False):
    yaml = YAML(typ='rt' if with_comments else 'safe')
    try:
        async with aiofiles.open(path, mode='rt') as f:
            dictionary = yaml.load(await f.read())
    except OSError as e:
        raise DiskError(f'path is not accessible; {e}', path=path)
    except YAMLError as e:
        raise ParsingError(f'file is not yaml; {e}', path=path)
    return dictionary or {}


async def save_raw_yaml(path, x, with_comments=False):
    yaml = YAML(typ=['rt' if with_comments else 'safe', 'bytes'])
    try:
        async with aiofiles.open(path, mode='wb') as f:
            await f.write(yaml.dump_to_bytes(x))
    except OSError as e:
        raise DiskError(f'path is not accessible; {e}', path=path)
    except YAMLError as e:
        raise FormattingError(f'value cannot be yaml; {e}', path=path)


def sync_load_raw_yaml(path, with_comments=False):
    yaml = YAML(typ='rt' if with_comments else 'safe')
    try:
        with open(path, mode='rt') as f:
            dictionary = yaml.load(f.read())
    except OSError as e:
        raise DiskError(f'path is not accessible; {e}', path=path)
    except YAMLError as e:
        raise ParsingError(f'file is not valid yaml; {e}', path=path)
    return dictionary or {}


def sync_save_raw_yaml(path, x, with_comments=False):
    yaml = YAML(typ=['rt' if with_comments else 'safe', 'bytes'])
    try:
        with open(path, mode='wb') as f:
            f.write(yaml.dump_to_bytes(x))
    except OSError as e:
        raise DiskError(f'path is not accessible; {e}', path=path)
    except YAMLError as e:
        raise FormattingError(f'value cannot be yaml; {e}', path=path)
