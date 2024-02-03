from typing import Any

import httpx
from facet import ServiceMixin


class HTTPClient(httpx.AsyncClient, ServiceMixin):
    def __init__(
            self,
            base_url: str = "",
            verify: bool = True,
    ):
        super().__init__(base_url=base_url, verify=verify)

    async def start(self):
        await self.__aenter__()  # pylint: disable=unnecessary-dunder-call

    async def stop(self):
        await self.__aexit__()  # pylint: disable=unnecessary-dunder-call
