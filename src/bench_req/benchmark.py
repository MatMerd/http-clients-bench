import statistics
import time
from typing import Awaitable, Callable


async def run_benchmark(
    benchmark_func: Callable[[], Awaitable[list]],
    iterations: int = 60,
    requests: int = 100,
    connections: int = 10,
) -> None:
    """
    Общая функция для запуска бенчмарков.

    Args:
        benchmark_func: Async функция, которая выполняет одну итерацию бенчмарка
        iterations: Количество итераций
        requests: Количество запросов на соединение
        connections: Количество параллельных соединений
    """
    aggregate = []

    for _ in range(iterations):
        before = time.time()
        await benchmark_func()
        delay = time.time() - before
        aggregate.append(delay)

    print("median", statistics.median(aggregate))
    print("average", sum(aggregate) / len(aggregate))
    print("total", sum(aggregate))
    print("requests per second", requests * iterations * connections / sum(aggregate))
