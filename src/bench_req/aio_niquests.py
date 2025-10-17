import asyncio

import niquests
from niquests import AsyncSession, Response

from bench_req.benchmark import run_benchmark


async def fetch(s: niquests.AsyncSession, url: str, requests: int) -> list[Response]:
    responses = []

    for _ in range(requests):
        responses.append(await s.get(url, verify="./certs/ca.crt"))

    for response in responses:
        await s.gather(response)

    return responses


async def main(
    iterations: int = 60,
    requests: int = 100,
    connections: int = 10,
    concurrency: int = 10,
) -> None:
    async def benchmark_iteration() -> list:
        async with AsyncSession(multiplexed=True, pool_maxsize=concurrency) as session:
            responses_responses = await asyncio.gather(
                *[
                    fetch(session, "https://httpbin.local:4443/get", requests)
                    for _ in range(connections)
                ]
            )
            return [item for sublist in responses_responses for item in sublist]

    await run_benchmark(benchmark_iteration, iterations, requests, connections)


if __name__ == "__main__":
    asyncio.run(main())
