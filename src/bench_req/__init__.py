import asyncio
from .aio_aiohttp import main as aio_aiohttp
from .aio_httpx import main as aio_httpx
from .aio_niquests import main as aio_niquests
from .aio_niquests_core import main as aio_niquests_core


async def run():
    print("aio_aiohttp")
    await aio_aiohttp()
    print("-" * 80)

    print("aio_httpx")
    await aio_httpx()
    print("-" * 80)

    print("aio_niquests")
    await aio_niquests()
    print("-" * 80)

    print("aio_niquests_core")
    await aio_niquests_core()
    print("-" * 80)


def main() -> None:
    asyncio.run(run())
