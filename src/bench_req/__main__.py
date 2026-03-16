import argparse
import asyncio

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from bench_req.config import BenchmarkConfig
from bench_req.metrics import BenchmarkResult
from bench_req.reporter import print_all, to_json
from bench_req.runner import run_async_benchmark, run_sync_benchmark

console = Console()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="bench-req",
        description="HTTP client benchmarking suite",
    )
    p.add_argument("--url", default="https://httpbin.local:4443/get", help="Target URL")
    p.add_argument("--ca-cert", default="./certs/ca.crt", help="CA certificate file")
    p.add_argument("--iterations", "-n", type=int, default=30, help="Measurement iterations")
    p.add_argument("--warmup", type=int, default=3, help="Warmup iterations")
    p.add_argument("--total-requests", "-r", type=int, default=10000, help="Total requests per async iteration")
    p.add_argument("--concurrency", "-c", type=int, default=100, help="Max concurrent in-flight requests")
    p.add_argument("--sync-requests", type=int, default=200, help="Requests per sync iteration")
    p.add_argument("--pool-size", type=int, default=100, help="Connection pool size")
    p.add_argument(
        "--categories",
        nargs="+",
        choices=["sync-http1", "async-http1", "async-http2"],
        default=None,
        help="Categories to run (default: all)",
    )
    p.add_argument(
        "--clients",
        nargs="+",
        default=None,
        help="Specific clients to run (e.g. aiohttp httpx rnet)",
    )
    p.add_argument("--iter-timeout", type=float, default=120.0, help="Timeout per iteration in seconds (0=none)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    return p.parse_args()


async def run(config: BenchmarkConfig, categories: list[str] | None, client_filter: list[str] | None, as_json: bool) -> None:
    from bench_req.clients import ASYNC_HTTP1_CLIENTS, ASYNC_HTTP2_CLIENTS, SYNC_CLIENTS

    all_results: dict[str, list[BenchmarkResult]] = {}
    run_all = categories is None

    def filter_clients(clients: list) -> list:
        if client_filter is None:
            return clients
        return [c for c in clients if c.name in client_filter]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:

        if run_all or "sync-http1" in categories:
            clients = filter_clients(SYNC_CLIENTS)
            if clients:
                progress.add_task("[bold]Sync HTTP/1.1[/bold]", total=0)
                results = []
                for cls in clients:
                    r = run_sync_benchmark(cls, config, "Sync HTTP/1.1", progress)
                    results.append(r)
                all_results["Sync HTTP/1.1"] = results

        if run_all or "async-http1" in categories:
            clients = filter_clients(ASYNC_HTTP1_CLIENTS)
            if clients:
                progress.add_task("[bold]Async HTTP/1.1[/bold]", total=0)
                results = []
                for cls in clients:
                    r = await run_async_benchmark(cls, config, "1.1", "Async HTTP/1.1", progress)
                    results.append(r)
                all_results["Async HTTP/1.1"] = results

        if run_all or "async-http2" in categories:
            clients = filter_clients(ASYNC_HTTP2_CLIENTS)
            if clients:
                progress.add_task("[bold]Async HTTP/2[/bold]", total=0)
                results = []
                for cls in clients:
                    r = await run_async_benchmark(cls, config, "2", "Async HTTP/2", progress)
                    results.append(r)
                all_results["Async HTTP/2"] = results

    if as_json:
        console.print(to_json(all_results))
    else:
        print_all(all_results)


def main() -> None:
    args = parse_args()
    config = BenchmarkConfig(
        url=args.url,
        ca_cert=args.ca_cert,
        iterations=args.iterations,
        warmup=args.warmup,
        total_requests=args.total_requests,
        concurrency=args.concurrency,
        sync_requests=args.sync_requests,
        pool_size=args.pool_size,
        iter_timeout=args.iter_timeout,
    )

    console.print("[bold]bench-req[/bold] v0.2.0")
    console.print(f"  URL: {config.url}")
    console.print(f"  Iterations: {config.iterations} (+{config.warmup} warmup)")
    console.print(f"  Async: {config.total_requests} req/iter, concurrency={config.concurrency}")
    console.print(f"  Sync: {config.sync_requests} req/iter (sequential)")
    console.print(f"  Pool: {config.pool_size}, timeout: {config.iter_timeout}s")
    console.print()

    asyncio.run(run(config, args.categories, args.clients, args.json))


if __name__ == "__main__":
    main()
