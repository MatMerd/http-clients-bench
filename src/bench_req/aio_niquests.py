import asyncio
import statistics
import time

import niquests
from niquests import AsyncSession, Response


async def fetch(s: niquests.AsyncSession, url: str) -> list[Response]:
    responses = []

    for _ in range(100):
        responses.append(await s.get(url))

    for response in responses:
        await s.gather(response)

    return responses


async def main() -> None:
    aggregate = []

    for _ in range(60):
        before = time.time()

        async with AsyncSession(multiplexed=True, pool_maxsize=10) as session:
            responses_responses = await asyncio.gather(
                *[fetch(session, "https://httpbin.local:4443/get") for _ in range(10)]
            )
            _ = [item for sublist in responses_responses for item in sublist]

        delay = time.time() - before
        aggregate.append(delay)

    print("median", statistics.median(aggregate))
    print("average", sum(aggregate) / len(aggregate))
    print("total", sum(aggregate))


if __name__ == "__main__":
    asyncio.run(main())
