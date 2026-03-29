import ssl

import httpx
import httpx_aiohttp

from bench_req.clients.base import AsyncClient
from bench_req.config import BenchmarkConfig


class Client(AsyncClient):
    name = "httpx_aiohttp"
    http_versions = ["1.1"]

    async def setup(self, config: BenchmarkConfig, http_version: str = "1.1") -> None:
        ssl_context = ssl.create_default_context(cafile=config.ca_cert)
        use_http2 = http_version == "2"
        pool_size = max(config.pool_size, config.concurrency)
        self._client = httpx_aiohttp.HttpxAiohttpClient(
            timeout=httpx.Timeout(60.0, pool=120.0),
            transport=httpx_aiohttp.AiohttpTransport(
                limits=httpx.Limits(
                    max_connections=pool_size,
                    max_keepalive_connections=pool_size,
                    keepalive_expiry=30.0,
                ),
                verify=ssl_context,
                ttl_dns_cache=None,
                http2=use_http2,
                http1=not use_http2,
            ),
        )

    async def teardown(self) -> None:
        await self._client.aclose()

    async def get(self, url: str) -> int:
        resp = await self._client.get(url)
        return resp.status_code
