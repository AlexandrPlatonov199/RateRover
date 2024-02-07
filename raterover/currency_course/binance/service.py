import asyncio
import json

import httpx
import websockets
from facet import ServiceMixin
from loguru import logger

from raterover.currency_course.broker.producer_service import CourseProducerBrokerService
from raterover.currency_course.database.service import CourseDatabaseService
from raterover.currency_course.settings import CourseSettings


class BinanceCourseService(httpx.AsyncClient, ServiceMixin):
    def __init__(self,
                 btc_uri: str,
                 eth_uri: str,
                 api_key_exchange: str,
                 url_exchange: str,
                 database: CourseDatabaseService,
                 broker_producer: CourseProducerBrokerService,
                 verify: bool = True):
        self._btc_uri = btc_uri
        self._eth_uri = eth_uri
        self._database = database
        self._broker_producer = broker_producer
        self._api_key_exchange = api_key_exchange
        self._url_exchange = url_exchange


        super().__init__(verify=verify)


    async def coingecko_api(self):
        coins = ['bitcoin', 'ethereum']
        currencies = 'usd,rub'

        while True:
            for coin_id in coins:
                crypto_data = await self.get_crypto_data(coin_id, currencies)

                if crypto_data and coin_id in crypto_data:
                    usd_price = crypto_data[coin_id].get('usd')
                    rub_price = crypto_data[coin_id].get('rub')

                    if coin_id == "bitcoin":
                        coin_id = "btc"

                    if usd_price is not None:
                        # Сохранение курса BTC/USD в базе данных
                        async with self._database.transaction() as session:
                            await self._database.create_course(
                                session=session,
                                exchanger='coingecko',
                                direction=f"{coin_id.upper()[:3]}-USD",
                                value=usd_price
                            )

                    if rub_price is not None:
                        # Сохранение курса BTC/RUB в базе данных
                        async with self._database.transaction() as session:
                            await self._database.create_course(
                                session=session,
                                exchanger='coingecko',
                                direction=f"{coin_id.upper()[:3]}-RUB",
                                value=rub_price
                            )
                else:
                    logger.error("Failed to fetch {} data", coin_id.capitalize())
                    logger.info("Switching to Binance...")
                    await self.binance_websocket()

            await asyncio.sleep(5)

    async def get_crypto_data(self, coin_id, vs_currencies):
        try:
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currencies}'
            response = await self.get(url=url)
            data = response.json()

            # Возвращаем данные в нужном формате
            return data
        except Exception as e:
            logger.exception("An unexpected error occurred: {}", e)
            logger.info("Switching to Binance...")
            await self.binance_websocket()

    async def binance_websocket(self):
        try:
            async with (websockets.connect(self._btc_uri) as btc_websocket,
                        websockets.connect(self._eth_uri) as eth_websocket):
                while True:
                    btc_response = await btc_websocket.recv()
                    btc_data = json.loads(btc_response)

                    eth_response = await eth_websocket.recv()
                    eth_data = json.loads(eth_response)

                    btc_usdt_price = float(btc_data['p'])
                    eth_usdt_price = float(eth_data['p'])

                    # Запрос актуального курса обмена USDT/RUB от ExchangeRate-API
                    usdt_rub_exchange_rate = await self.get_usdt_rub_exchange_rate()

                    if usdt_rub_exchange_rate is not None:
                        # Конвертация цены из BTC/USDT и ETH/USDT в BTC/RUB и ETH/RUB
                        btc_rub_price = btc_usdt_price * usdt_rub_exchange_rate
                        eth_rub_price = eth_usdt_price * usdt_rub_exchange_rate
                    else:
                        logger.error("Failed to fetch USDT/RUB exchange rate.")

                    data = {
                        "exchanger": "binance",
                        "direction": "BTC-USD",
                        "value": btc_usdt_price,
                    }

                    await self._broker_producer.send_message(queue="course_binance", message=data)

                    # async with self._database.transaction() as session:
                    #     await self._database.create_course(
                    #         session=session,
                    #         exchanger='binance',
                    #         direction='BTC-USD',
                    #         value=btc_usdt_price
                    #     )
                    #
                    # async with self._database.transaction() as session:
                    #     await self._database.create_course(
                    #         session=session,
                    #         exchanger='binance',
                    #         direction='BTC-RUB',
                    #         value=btc_rub_price
                    #     )
                    #
                    # async with self._database.transaction() as session:
                    #     await self._database.create_course(
                    #         session=session,
                    #         exchanger='binance',
                    #         direction='ETH-USD',
                    #         value=eth_usdt_price
                    #     )
                    #
                    # async with self._database.transaction() as session:
                    #     await self._database.create_course(
                    #         session=session,
                    #         exchanger='binance',
                    #         direction='ETH-RUB',
                    #         value=eth_rub_price
                    #     )

                    await asyncio.sleep(5)

        except Exception as e:
            logger.exception("An unexpected error occurred: {}", e)
            logger.info("Switching to Coingecko...")
            await self.coingecko_api()

    async def get_usdt_rub_exchange_rate(self):
        params = {'symbols': 'RUB', 'base': 'USD', 'apikey': self._api_key_exchange}

        response = await self.get(url=self._url_exchange, params=params)

        data = response.json()

        usdt_rub_exchange_rate = data['rates']['RUB']

        return usdt_rub_exchange_rate

    async def start(self):
        logger.info("Starting Binance service")
        await self.binance_websocket()


def get_binan(
        settings: CourseSettings,
        database: CourseDatabaseService,
        broker_producer: CourseProducerBrokerService,
              ) -> BinanceCourseService:
    return BinanceCourseService(btc_uri=settings.btc_uri,
                                eth_uri=settings.eth_uri,
                                url_exchange=settings.url_exchange,
                                api_key_exchange=settings.api_key_exchange,
                                database=database,
                                broker_producer=broker_producer,
                                )
