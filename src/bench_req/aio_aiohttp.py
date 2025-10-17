import asyncio
import ssl
import aiohttp

from bench_req.benchmark import run_benchmark


async def fetch(
    c: aiohttp.ClientSession, url: str, requests: int
) -> list[aiohttp.ClientResponse]:
    responses = []

    for _ in range(requests):
        responses.append(await c.get(url))

    return responses


async def main(
    iterations: int = 60,
    requests: int = 100,
    connections: int = 10,
    concurrency: int = 10,
) -> None:
    async def benchmark_iteration() -> list:
        ssl_context = ssl.create_default_context(cafile="./certs/ca.crt")
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=concurrency, ssl=ssl_context),
        ) as s:
            responses_responses = await asyncio.gather(
                *[
                    fetch(s, "https://httpbin.local:4443/get", requests)
                    for _ in range(connections)
                ]
            )
            return [item for sublist in responses_responses for item in sublist]

    await run_benchmark(benchmark_iteration, iterations, requests, connections)


if __name__ == "__main__":
    asyncio.run(main())
