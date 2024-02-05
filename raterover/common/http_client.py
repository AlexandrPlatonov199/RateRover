from typing import Any

import httpx
from facet import ServiceMixin


class HTTPClient(httpx.AsyncClient, ServiceMixin):
    def __init__(
            self,
            base_url_binance: str = "",
            base_url_coingecko: str = "",
            verify: bool = True,
    ):
        super().__init__(
                         verify=verify,)

    async def start(self):
        await self.__aenter__()

    async def stop(self):
        await self.__aexit__()