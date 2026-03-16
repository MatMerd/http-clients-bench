# bench-req

HTTP client benchmarking suite for Python.

## Libraries

| Library | Type | HTTP/2 |
|---------|------|--------|
| [rnet](https://pypi.org/project/rnet/) | Async + Sync | Yes |
| [primp](https://pypi.org/project/primp/) | Async + Sync | Yes |
| [aiohttp](https://pypi.org/project/aiohttp/) | Async | No |
| [httpx](https://pypi.org/project/httpx/) | Async | Yes |
| [httpcore](https://pypi.org/project/httpcore/) | Async | Yes |
| [niquests](https://pypi.org/project/niquests/) | Async | Yes |
| [urllib3-future](https://pypi.org/project/urllib3-future/) | Async | Yes |
| [impit](https://pypi.org/project/impit/) | Async | No |
| [requests](https://pypi.org/project/requests/) | Sync | No |

## Setup

```bash
echo "127.0.0.1   httpbin.local" | sudo tee -a /etc/hosts
docker compose up -d
uv sync
```

## Usage

```bash
uv run bench-req
uv run bench-req -r 100000 -c 100 -n 5
uv run bench-req --categories async-http2 --clients rnet httpx niquests
uv run bench-req --json
```

## Results

Arch Linux, AMD Ryzen 5 3600 6-Core, 39GB RAM, Python 3.14, 10k req/iter, concurrency 100

### Sync HTTP/1.1

| Client | RPS | p50 (ms) | p95 (ms) | p99 (ms) | CPU (s/iter) | RSS avg (MB) | RSS peak (MB) |
|--------|----:|--------:|--------:|--------:|------------:|------------:|-------------:|
| rnet | 3,909 | 0.24 | 0.34 | 0.44 | 0.017 | 100.8 | 100.8 |
| primp | 3,651 | 0.26 | 0.37 | 0.46 | 0.014 | 84.9 | 84.9 |
| requests | 1,179 | 0.78 | 1.05 | 2.09 | 0.120 | 81.5 | 81.5 |

### Async HTTP/1.1

| Client | RPS | p50 (ms) | p95 (ms) | p99 (ms) | CPU (s/iter) | RSS avg (MB) | RSS peak (MB) |
|--------|----:|--------:|--------:|--------:|------------:|------------:|-------------:|
| rnet | 13,649 | 5.22 | 9.42 | 16.49 | 1.349 | 261.0 | 261.1 |
| impit | 12,574 | 6.84 | 10.97 | 18.08 | 2.090 | 213.9 | 214.4 |
| primp | 10,649 | 7.24 | 22.64 | 35.63 | 2.041 | 221.3 | 221.7 |
| aiohttp | 9,654 | 7.82 | 10.37 | 15.06 | 0.949 | 148.9 | 149.2 |
| urllib3-future | 3,074 | 17.21 | 25.58 | 34.33 | 3.161 | 195.3 | 196.1 |
| niquests | 1,995 | 25.69 | 40.04 | 50.04 | 4.900 | 182.3 | 183.2 |
| httpcore | 947 | 70.06 | 314.70 | 494.11 | 10.448 | 154.7 | 154.7 |
| httpx | 608 | 105.23 | 504.03 | 803.55 | 16.299 | 151.8 | 152.0 |

### Async HTTP/2

| Client | RPS | p50 (ms) | p95 (ms) | p99 (ms) | CPU (s/iter) | RSS avg (MB) | RSS peak (MB) |
|--------|----:|--------:|--------:|--------:|------------:|------------:|-------------:|
| rnet | 13,020 | 5.95 | 11.39 | 15.96 | 1.366 | 269.8 | 270.2 |
| primp | 12,063 | 7.05 | 13.08 | 18.56 | 1.699 | 272.4 | 272.6 |
| urllib3-future | 2,940 | 17.71 | 28.82 | 38.82 | 3.307 | 270.9 | 271.4 |
| httpcore | 2,267 | 41.17 | 56.39 | 67.77 | 4.317 | 261.6 | 261.6 |
| niquests | 1,810 | 28.18 | 46.16 | 56.72 | 5.417 | 262.2 | 262.7 |
| httpx | 1,653 | 59.67 | 75.10 | 84.41 | 5.940 | 259.9 | 259.9 |
