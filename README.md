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

#### Libraries Tested

- **aiohttp**: >=3.13.1
- **httpcore**: >=1.0.9
- **httpx**: >=0.28.1
- **impit**: >=0.7.3
- **niquests**: >=3.15.2
- **primp**: >=0.15.0
- **rnet**: ==3.0.0rc9

| Client | Median (s) | Average (s) | Estimated Throughput |
|--------|------------|-------------|---------------------|
| rnet | 0.191 | 0.192 | ~10393 req/s |
| impit | 0.216 | 0.220 | ~9077 req/s |
| aiohttp | 0.277 | 0.284 | ~7038 req/s |
| niquests core | 0.572 | 0.596 | ~3356 req/s |
| niquests | 1.013 | 1.010 | ~1981 req/s |
| httpx | 1.220 | 1.255 | ~1594 req/s |
