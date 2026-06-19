import asyncio
import pytest

from crosscompute_macros.concurrency import (
    lock_by)


@pytest.mark.asyncio
async def test_lock_by_concurrent():
    results = []
    async def task(val):
        async with lock_by('x'):
            results.append(val)
            await asyncio.sleep(0)
            results.append(val)

    await asyncio.gather(task(1), task(2))
    assert results in ([1, 1, 2, 2], [2, 2, 1, 1])


@pytest.mark.asyncio
async def test_lock_by_different_keys():
    order = []
    async def task(key):
        async with lock_by(key):
            order.append(f'start_{key}')
            await asyncio.sleep(0)
            order.append(f'end_{key}')

    await asyncio.gather(task('a'), task('b'))
    assert order.index('start_a') < order.index('end_b')
    assert order.index('start_b') < order.index('end_a')


# ruff: noqa: S101
