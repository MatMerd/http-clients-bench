import asyncio
import statistics
import time

from urllib3_future import AsyncPoolManager, AsyncHTTPResponse
import wassima


async def fetch(pool: AsyncPoolManager, url: str) -> list[AsyncHTTPResponse]:
    promises = []
    responses = []

    for _ in range(100):
        promises.append(await pool.urlopen("GET", url, multiplexed=True))

    for promise in promises:
        responses.append(await pool.get_response(promise=promise))

    return responses


async def main() -> None:
    aggregate = []

    for _ in range(60):
        before = time.time()
        async with AsyncPoolManager(
            maxsize=10, ca_cert_data=wassima.generate_ca_bundle()
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
