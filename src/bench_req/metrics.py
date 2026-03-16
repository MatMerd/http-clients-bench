import resource
import statistics
from dataclasses import dataclass, field


@dataclass
class IterationResult:
    latencies: list[float]
    duration: float
    rss_bytes: int
    cpu_user_delta: float
    cpu_system_delta: float

    @property
    def requests_count(self) -> int:
        return len(self.latencies)

    @property
    def rps(self) -> float:
        return self.requests_count / self.duration if self.duration > 0 else 0


@dataclass
class BenchmarkResult:
    name: str
    category: str
    iterations: list[IterationResult] = field(default_factory=list)

    @property
    def total_requests(self) -> int:
        return sum(it.requests_count for it in self.iterations)

    @property
    def total_duration(self) -> float:
        return sum(it.duration for it in self.iterations)

    @property
    def rps(self) -> float:
        return self.total_requests / self.total_duration if self.total_duration > 0 else 0

    @property
    def all_latencies(self) -> list[float]:
        out: list[float] = []
        for it in self.iterations:
            out.extend(it.latencies)
        return out

    @property
    def latency_p50(self) -> float:
        lats = sorted(self.all_latencies)
        return _percentile(lats, 50) * 1000
    @property
    def latency_p95(self) -> float:
        lats = sorted(self.all_latencies)
        return _percentile(lats, 95) * 1000

    @property
    def latency_p99(self) -> float:
        lats = sorted(self.all_latencies)
        return _percentile(lats, 99) * 1000

    @property
    def avg_cpu_total(self) -> float:
        if not self.iterations:
            return 0
        return statistics.mean(
            it.cpu_user_delta + it.cpu_system_delta for it in self.iterations
        )

    @property
    def peak_rss_mb(self) -> float:
        if not self.iterations:
            return 0
        return max(it.rss_bytes for it in self.iterations) / (1024 * 1024)

    @property
    def avg_rss_mb(self) -> float:
        if not self.iterations:
            return 0
        return statistics.mean(it.rss_bytes for it in self.iterations) / (1024 * 1024)


def get_rss_bytes() -> int:
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 0


def get_cpu_times() -> tuple[float, float]:
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime, r.ru_stime


def _percentile(sorted_data: list[float], pct: float) -> float:
    if not sorted_data:
        return 0.0
    k = (len(sorted_data) - 1) * (pct / 100)
    f = int(k)
    c = f + 1
    if c >= len(sorted_data):
        return sorted_data[f]
    return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])
