import asyncio

from urllib3_future import AsyncPoolManager, AsyncHTTPResponse

from bench_req.benchmark import run_benchmark


async def fetch(
    pool: AsyncPoolManager, url: str, requests: int
) -> list[AsyncHTTPResponse]:
    promises = []
    responses = []

    for _ in range(requests):
        promises.append(await pool.urlopen("GET", url, multiplexed=True))

    for promise in promises:
        responses.append(await pool.get_response(promise=promise))

    return responses


async def main(
    iterations: int = 60,
    requests: int = 100,
    connections: int = 10,
    concurrency: int = 10,
) -> None:
    async def benchmark_iteration() -> list:
        async with AsyncPoolManager(
            maxsize=concurrency, ca_certs="./certs/ca.crt"
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
