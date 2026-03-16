import json

from rich.console import Console
from rich.table import Table

from bench_req.metrics import BenchmarkResult

console = Console()


def print_category(category: str, results: list[BenchmarkResult]) -> None:
    results = [r for r in results if r.iterations]
    if not results:
        console.print(f"\n[yellow]{category}: no successful results[/yellow]")
        return

    results.sort(key=lambda r: r.rps, reverse=True)

    table = Table(
        title=f"\n{category}",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )

    table.add_column("Client", style="bold", min_width=16)
    table.add_column("RPS", justify="right", min_width=10)
    table.add_column("p50 (ms)", justify="right", min_width=10)
    table.add_column("p95 (ms)", justify="right", min_width=10)
    table.add_column("p99 (ms)", justify="right", min_width=10)
    table.add_column("CPU (s/iter)", justify="right", min_width=12)
    table.add_column("RSS avg (MB)", justify="right", min_width=12)
    table.add_column("RSS peak (MB)", justify="right", min_width=13)
    table.add_column("Requests", justify="right", min_width=10)

    best_rps = results[0].rps if results else 0

    for r in results:
        rps_pct = (r.rps / best_rps * 100) if best_rps > 0 else 0
        rps_color = "green" if rps_pct > 90 else "yellow" if rps_pct > 60 else "red"

        table.add_row(
            r.name,
            f"[{rps_color}]{r.rps:,.0f}[/{rps_color}]",
            f"{r.latency_p50:.2f}",
            f"{r.latency_p95:.2f}",
            f"{r.latency_p99:.2f}",
            f"{r.avg_cpu_total:.3f}",
            f"{r.avg_rss_mb:.1f}",
            f"{r.peak_rss_mb:.1f}",
            f"{r.total_requests:,}",
        )

    console.print(table)


def print_all(all_results: dict[str, list[BenchmarkResult]]) -> None:
    for category, results in all_results.items():
        print_category(category, results)


def to_json(all_results: dict[str, list[BenchmarkResult]]) -> str:
    data = {}
    for category, results in all_results.items():
        data[category] = []
        for r in sorted(results, key=lambda r: r.rps, reverse=True):
            if not r.iterations:
                continue
            data[category].append({
                "client": r.name,
                "rps": round(r.rps, 1),
                "latency_p50_ms": round(r.latency_p50, 3),
                "latency_p95_ms": round(r.latency_p95, 3),
                "latency_p99_ms": round(r.latency_p99, 3),
                "cpu_per_iter_s": round(r.avg_cpu_total, 4),
                "rss_avg_mb": round(r.avg_rss_mb, 1),
                "rss_peak_mb": round(r.peak_rss_mb, 1),
                "total_requests": r.total_requests,
                "iterations": len(r.iterations),
            })
    return json.dumps(data, indent=2)
