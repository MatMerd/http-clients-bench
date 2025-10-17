import asyncio

from impit import AsyncClient

from bench_req.benchmark import run_benchmark


async def fetch(s: AsyncClient, url: str, requests: int) -> list:
    responses = []

    for _ in range(requests):
        responses.append(await s.get(url))

    return responses


async def main(
    iterations: int = 60,
    requests: int = 100,
    connections: int = 10,
    concurrency: int = 10,
) -> None:
    async def benchmark_iteration() -> list:
        async with AsyncClient(
            http3=True,
            verify=False,
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
