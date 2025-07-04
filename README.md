# HTTP clients benchmarking suite comparing requests, httpx, aiohttp, and niquests performance

## Original repository

https://github.com/Ousret/niquests-stats/

## Setup

```
apt install mkcert # or brew install mkcert | yum install mkcert | pacman -S mkcert
mkcert -cert-file ./certs/httpbin.local.pem -key-file ./certs/httpbin.local.key httpbin.local
mkcert -install
echo "127.0.0.1   httpbin.local" | sudo tee -a /etc/hosts
```

## Run

```
docker compose up -d
uv sync
uv run bench-req
```

## Results

### Published Results (Fedora 38, Intel Core i7 12th Gen, 32GB DDR4, Python 3.11)

#### High-level APIs

| Client | Average Delay | Estimated Throughput |
|--------|---------------|---------------------|
| requests | 987 ms | ~1013 req/s |
| httpx | 720 ms | ~1389 req/s |
| niquests | 340 ms | ~2941 req/s |

#### Simplified APIs

| Client | Average Delay | Estimated Throughput |
|--------|---------------|---------------------|
| requests core | 643 ms | ~1555 req/s |
| httpx core | 490 ms | ~2000 req/s |
| aiohttp | 210 ms | ~4762 req/s |
| niquests core | 160 ms | ~6200 req/s |

### Actual Results (Arch Linux, AMD Ryzen 5 3600 6-Core, 39GB RAM, Python 3.13.3)

| Client | Median (s) | Average (s) | Estimated Throughput |
|--------|------------|-------------|---------------------|
| httpx | 0.714 | 0.736 | ~1359 req/s |
| niquests | 0.535 | 0.579 | ~1727 req/s |
| niquests core | 0.318 | 0.332 | ~3012 req/s |
| aiohttp | 0.166 | 0.167 | ~5988 req/s |
