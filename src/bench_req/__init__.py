import asyncio
from .aio_aiohttp import main as aio_aiohttp
from .aio_httpx import main as aio_httpx
from .aio_impit import main as aio_impit
from .aio_niquests import main as aio_niquests
from .aio_niquests_core import main as aio_niquests_core
from .aio_rnet import main as aio_rnet


async def run():
    params = (50, 100, 20, 20)  # iterations, requests, connections, concurrency

    benchmarks = [
        ("aio_impit", aio_impit),
        ("aio_rnet", aio_rnet),
        ("aio_niquests", aio_niquests),
        ("aio_aiohttp", aio_aiohttp),
        ("aio_httpx", aio_httpx),
        ("aio_niquests_core", aio_niquests_core),
    ]

    for name, func in benchmarks:
        print(name)
        await func(*params)
        print("-" * 80)


def main() -> None:
    asyncio.run(run())
