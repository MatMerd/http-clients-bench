import asyncio
import statistics
import time
import wassima
from httpcore import AsyncConnectionPool, Response


async def fetch(s: AsyncConnectionPool, url: str) -> list[Response]:
    responses = []

    for _ in range(100):
        responses.append(await s.request("GET", url))

    return responses


async def main() -> None:
    aggregate = []

    for _ in range(60):
        before = time.time()
        async with AsyncConnectionPool(
            http2=True,
            ssl_context=wassima.create_default_ssl_context(),
            max_connections=10,
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
