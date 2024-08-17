import json

import pytest
from aiofiles import open

from crosscompute_macros.disk import update_raw_json


@pytest.mark.asyncio
async def test_update_variable_data(tmp_path):
    path = tmp_path / 'x.json'
    await update_raw_json(path, {'a': 1, 'b': 2})
    async with open(path, mode='rt') as f:
        d = json.loads(await f.read())
        assert d['a'] == 1
        assert d['b'] == 2
    await update_raw_json(path, {'a': 2})
    async with open(path, mode='rt') as f:
        d = json.loads(await f.read())
        assert d['a'] == 2
        assert d['b'] == 2
