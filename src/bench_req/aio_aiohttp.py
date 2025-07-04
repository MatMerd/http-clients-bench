import asyncio
import time
import aiohttp
import wassima
import statistics


async def fetch(c: aiohttp.ClientSession, url: str) -> list[aiohttp.ClientResponse]:
    responses = []

    for _ in range(100):
        responses.append(await c.get(url))

    return responses


async def main() -> None:
    aggregate = []

    for _ in range(60):
        before = time.time()

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=10, ssl=wassima.create_default_ssl_context()
            ),
        ) as s:
            responses_responses = await asyncio.gather(
                *[fetch(s, "https://httpbin.local:4443/get") for _ in range(10)]
            )

            _ = [item for sublist in responses_responses for item in sublist]

        delay = time.time() - before
        aggregate.append(delay)

    print("median", statistics.median(aggregate))
    print("average", sum(aggregate) / len(aggregate))
    print("total", sum(aggregate))


if __name__ == "__main__":
    asyncio.run(main())
