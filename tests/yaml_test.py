import pytest

from crosscompute_macros.yaml import (
    load_raw_yaml,
    save_raw_yaml,
    sync_load_raw_yaml,
    sync_save_raw_yaml)


def test_sync_save_raw_yaml(tmp_path):
    path = tmp_path / 'x.yaml'
    sync_save_raw_yaml(path, {'a': 1, 'b': 2})
    d = sync_load_raw_yaml(path)
    assert d['a'] == 1
    assert d['b'] == 2


@pytest.mark.asyncio
async def test_save_raw_yaml(tmp_path):
    path = tmp_path / 'x.yaml'
    await save_raw_yaml(path, {'a': 1, 'b': 2})
    d = await load_raw_yaml(path)
    assert d['a'] == 1
    assert d['b'] == 2


# ruff: noqa: S101
