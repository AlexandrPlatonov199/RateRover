import asyncio
import json

import backoff
from httpx import HTTPError
import websockets
from facet import ServiceMixin
from loguru import logger

from raterover.common.binance.settings import BaseBinanceSettings
from raterover.common.http_client import HTTPClient


class BinanceService(ServiceMixin):
    def __init__(self,
                 uri: str):
        self.uri = uri
        logger.info(self.uri)

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3, raise_on_giveup=False)
    async def get_price_feed(self, base_symbol):
        while True:
            async with websockets.connect(self.uri) as websocket:
                response = await websocket.recv()
                data = json.loads(response)

                for res in data:
                    if res["s"] == base_symbol:
                        result = {
                            "exchanger": "binance",
                            "direction": res["s"],
                            "value": float(res['c'])

                        }




def get_binance_course(settings: BaseBinanceSettings) -> BinanceService:
    return BinanceService(uri=settings.uri)
