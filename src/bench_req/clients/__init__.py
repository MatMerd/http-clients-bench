from bench_req.clients.base import AsyncClient, SyncClient

ASYNC_HTTP1_CLIENTS: list[type[AsyncClient]] = []
ASYNC_HTTP2_CLIENTS: list[type[AsyncClient]] = []
SYNC_CLIENTS: list[type[SyncClient]] = []


def _register() -> None:
    from bench_req.clients import (_aiohttp, _curl_cffi, _httpcore, _httpx,
                                   _httpx_aiohttp, _impit, _niquests, _primp,
                                   _requests, _rnet, _urllib3f)

    for mod in (_aiohttp, _curl_cffi, _httpx, _httpx_aiohttp, _httpcore, _niquests, _urllib3f, _impit, _primp, _rnet):
        if hasattr(mod, "Client"):
            cls = mod.Client
            if "1.1" in cls.http_versions:
                ASYNC_HTTP1_CLIENTS.append(cls)
            if "2" in cls.http_versions:
                ASYNC_HTTP2_CLIENTS.append(cls)

    for mod in (_httpx, _curl_cffi, _requests, _primp, ):
        if hasattr(mod, "SyncHTTPClient"):
            SYNC_CLIENTS.append(mod.SyncHTTPClient)

    if hasattr(_rnet, "SyncHTTPClient"):
        SYNC_CLIENTS.append(_rnet.SyncHTTPClient)


_register()
