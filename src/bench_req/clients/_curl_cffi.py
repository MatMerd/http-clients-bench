import curl_cffi

from bench_req.clients.base import AsyncClient, SyncClient
from bench_req.config import BenchmarkConfig


class Client(AsyncClient):
    name = "curl_cffi"
    http_versions = ["1.1", "2"]

    async def setup(self, config: BenchmarkConfig, http_version: str = "1.1") -> None:
        pool_size = max(config.pool_size, config.concurrency)
        http_version = "v1" if http_version == "1.1" else "v2"
        self._client = curl_cffi.AsyncSession(
            http_version=http_version,
            verify=False,
            max_clients=pool_size,
            timeout=60.0,
        )

    async def teardown(self) -> None:
        await self._client.close()

    async def get(self, url: str) -> int:
        resp = await self._client.get(url)
        return resp.status_code


class SyncHTTPClient(SyncClient):
    name = "curl_cffi"
    http_versions = ["1.1"]

    def setup(self, config: BenchmarkConfig, http_version: str = "1.1"):
        http_version = "v1" if http_version == "1.1" else "v2"
        self._client = curl_cffi.Session(
            http_version=http_version,
            verify=False,
            timeout=60.0,
        )

    def teardown(self):
        self._client.close()

    def get(self, url: str):
        resp = self._client.get(url)
        return resp.status_code
