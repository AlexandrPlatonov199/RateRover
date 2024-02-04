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


    async def get_price_feed(self, base_symbol):
        ws_uri = self.uri + f"{base_symbol}@trade"
        async with websockets.connect(ws_uri) as websocket:
            response = await websocket.recv()
            data = json.loads(response)

            result = {
                    "exchanger": "binance",
                    "direction": data["s"],
                    "value": float(data['p'])
            }
            print(result)
            return result


def get_binance_course(settings: BaseBinanceSettings) -> BinanceService:
    return BinanceService(uri=settings.uri)
