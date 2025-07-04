import asyncio
import statistics
import time
import wassima
from httpx import AsyncClient, Response, Limits


async def fetch(s: AsyncClient, url: str) -> list[Response]:
    responses = []

    for _ in range(100):
        responses.append(await s.get(url))

    return responses


async def main() -> None:
    aggregate = []

    for _ in range(60):
        before = time.time()

        async with AsyncClient(
            http2=True,
            verify=wassima.create_default_ssl_context(),
            limits=Limits(max_connections=10),
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
