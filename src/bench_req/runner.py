import asyncio
import gc
import time

from rich.console import Console
from rich.progress import Progress

from bench_req.clients.base import AsyncClient, SyncClient
from bench_req.config import BenchmarkConfig
from bench_req.metrics import BenchmarkResult, IterationResult, get_cpu_times, get_rss_bytes

console = Console()


async def run_async_benchmark(
    client_cls: type[AsyncClient],
    config: BenchmarkConfig,
    http_version: str,
    category: str,
    progress: Progress,
) -> BenchmarkResult:
    client = client_cls()
    result = BenchmarkResult(name=client_cls.name, category=category)
    total_iters = config.warmup + config.iterations

    task_id = progress.add_task(
        f"  {client_cls.name}", total=total_iters
    )

    try:
        await client.setup(config, http_version)
    except Exception as e:
        progress.update(task_id, description=f"  {client_cls.name} [red]SETUP FAILED: {e}[/red]")
        progress.update(task_id, completed=total_iters)
        return result

    for _ in range(config.warmup):
        try:
            await _run_async_iteration_with_timeout(client, config)
        except Exception:
            pass
        progress.advance(task_id)

    gc.collect()

    for _ in range(config.iterations):
        gc.collect()
        try:
            iteration = await _run_async_iteration_with_timeout(client, config)
            if iteration is not None:
                result.iterations.append(iteration)
            else:
                progress.update(task_id, description=f"  {client_cls.name} [yellow]TIMEOUT[/yellow]")
        except Exception as e:
            progress.update(task_id, description=f"  {client_cls.name} [yellow]ERR: {e!r:.60}[/yellow]")
        progress.advance(task_id)

    try:
        await client.teardown()
    except Exception:
        pass

    progress.update(task_id, description=f"  {client_cls.name} [green]done[/green]")
    return result


async def _run_async_iteration_with_timeout(
    client: AsyncClient, config: BenchmarkConfig
) -> IterationResult | None:
    if config.iter_timeout > 0:
        try:
            return await asyncio.wait_for(
                _run_async_iteration(client, config),
                timeout=config.iter_timeout,
            )
        except asyncio.TimeoutError:
            return None
    return await _run_async_iteration(client, config)


async def _run_async_iteration(
    client: AsyncClient, config: BenchmarkConfig
) -> IterationResult:
    sem = asyncio.Semaphore(config.concurrency)
    latencies: list[float] = []
    lock = asyncio.Lock()

    async def bounded_request() -> None:
        async with sem:
            t0 = time.perf_counter()
            await client.get(config.url)
            lat = time.perf_counter() - t0
        async with lock:
            latencies.append(lat)

    rss_before = get_rss_bytes()
    cpu_before = get_cpu_times()
    t_start = time.perf_counter()

    await asyncio.gather(
        *[bounded_request() for _ in range(config.total_requests)],
        return_exceptions=True,
    )

    duration = time.perf_counter() - t_start
    cpu_after = get_cpu_times()
    rss_after = get_rss_bytes()

    return IterationResult(
        latencies=latencies,
        duration=duration,
        rss_bytes=rss_after,
        cpu_user_delta=cpu_after[0] - cpu_before[0],
        cpu_system_delta=cpu_after[1] - cpu_before[1],
    )


def run_sync_benchmark(
    client_cls: type[SyncClient],
    config: BenchmarkConfig,
    category: str,
    progress: Progress,
) -> BenchmarkResult:
    client = client_cls()
    result = BenchmarkResult(name=client_cls.name, category=category)
    total_iters = config.warmup + config.iterations

    task_id = progress.add_task(
        f"  {client_cls.name}", total=total_iters
    )

    try:
        client.setup(config)
    except Exception as e:
        progress.update(task_id, description=f"  {client_cls.name} [red]SETUP FAILED: {e}[/red]")
        progress.update(task_id, completed=total_iters)
        return result

    for _ in range(config.warmup):
        try:
            _run_sync_iteration(client, config)
        except Exception:
            pass
        progress.advance(task_id)

    gc.collect()

    for _ in range(config.iterations):
        gc.collect()
        try:
            iteration = _run_sync_iteration(client, config)
            result.iterations.append(iteration)
        except Exception as e:
            progress.update(task_id, description=f"  {client_cls.name} [yellow]ERR: {e!r:.60}[/yellow]")
        progress.advance(task_id)

    try:
        client.teardown()
    except Exception:
        pass

    progress.update(task_id, description=f"  {client_cls.name} [green]done[/green]")
    return result


def _run_sync_iteration(
    client: SyncClient, config: BenchmarkConfig
) -> IterationResult:
    latencies: list[float] = []

    rss_before = get_rss_bytes()
    cpu_before = get_cpu_times()
    t_start = time.perf_counter()

    for _ in range(config.sync_requests):
        t0 = time.perf_counter()
        client.get(config.url)
        latencies.append(time.perf_counter() - t0)

    duration = time.perf_counter() - t_start
    cpu_after = get_cpu_times()
    rss_after = get_rss_bytes()

    return IterationResult(
        latencies=latencies,
        duration=duration,
        rss_bytes=rss_after,
        cpu_user_delta=cpu_after[0] - cpu_before[0],
        cpu_system_delta=cpu_after[1] - cpu_before[1],
    )
