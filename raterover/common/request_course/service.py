from loguru import logger

from .settings import BaseRequestSettings
from raterover.common.http_client import HTTPClient


class RequestService(HTTPClient):
    def __init__(self,
                 uri_binance: str,
                 uri_coingecko: str):
        self.uri_binance = uri_binance
        self.uri_coingecko = uri_coingecko
        print(self.uri_binance)
        print(self.uri_coingecko)

        super().__init__(base_url_binance=self.uri_binance,
                         base_url_coingecko=self.uri_coingecko,)

    async def get_price_feed(self, base_symbol, currency_pair):
        try:
            result_binance = await self.binance_api(base_symbol, currency_pair)
            logger.info(result_binance)
            return result_binance
        except Exception as e:
            logger.error(f"Error in Binance API: {e}")
            logger.info("Switching to CoinGecko...")

            result_coingecko = await self.coingecko_api(base_symbol, currency_pair)
            logger.info(result_coingecko)
            return result_coingecko

    async def coingecko_api(self, base_symbol, currency_pair):
        if base_symbol == "BTC" and currency_pair == "USD":
            base_symbol = "bitcoin"
            currency_pair = "usd"
        elif base_symbol == "BTC" and currency_pair == "RUB":
            base_symbol = "bitcoin"
            currency_pair = "rub"
        elif base_symbol == "ETH" and currency_pair == "RUB":
            base_symbol = "ethereum"
            currency_pair = "rub"
        elif base_symbol == "ETH" and currency_pair == "USD":
            base_symbol = "ethereum"
            currency_pair = "usd"

        params = {'ids': base_symbol.lower(), 'vs_currencies': currency_pair.lower()}
        direction = f"{base_symbol.upper()}-{currency_pair.upper()}"
        response = await self.get(url=self.uri_coingecko, params=params)
        data = response.json()
        price = data[base_symbol.lower()][currency_pair.lower()]

        result = {
            "exchanger": "coingecko",
            "direction": direction,
            "value": float(price)
        }

        return result

    async def binance_api(self, base_symbol, currency_pair):
        if currency_pair == "USD":
            currency_pair = "USDT"
        symbol = f"{base_symbol}{currency_pair}"
        params = {"symbol": symbol}
        currency_pair = f"{base_symbol.upper()}-{currency_pair.upper()}"

        response = await self.get(url=self.uri_binance, params=params)
        data = response.json()

        result = {
            "exchanger": "binance",
            "direction": currency_pair,
            "value": float(data["price"])
        }

        return result










        # ws_uri = self.uri + f"{base_symbol}@trade"
        # async with websockets.connect(ws_uri) as websocket:
        #     response = await websocket.recv()
        #     data = json.loads(response)
        #
        #     result = {
        #             "exchanger": "request_course",
        #             "direction": data["s"],
        #             "value": float(data['p'])
        #     }
        #     print(result)
        #     return result


def get_request_service(settings: BaseRequestSettings) -> RequestService:
    return RequestService(uri_coingecko=settings.uri_coingecko,
                          uri_binance=settings.uri_binance
                          )
