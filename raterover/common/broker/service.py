import asyncio

from typing import Iterable

import aio_pika
import backoff
from facet import ServiceMixin
from loguru import logger
from pydantic import BaseModel

from .handler import BaseBrokerHandler


class BaseBrokerConsumerService(ServiceMixin):
    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 amqp_url: str,
                 queues: Iterable[str],
                 handlers: Iterable[BaseBrokerHandler] = ()):
        self._handlers = handlers
        self._connection = None
        self._loop = loop
        self._amqp_url = amqp_url
        self._queues = queues

    @backoff.on_exception(backoff.expo, Exception)
    async def consume(self):
        async with self._connection.channel() as channel:
            for queue_name in self._queues:
                queue = await channel.declare_queue(queue_name)
                await queue.consume(self.handle)

        logger.info("Started consuming from queues: {}", self._queues)

    async def handle(self, message: aio_pika.IncomingMessage):
        async with message.process():
            for handler in self._handlers:
                if not await handler.check(message=message):
                    logger.debug("Skip message from queue '{}': {}", message.routing_key, message.body)
                    continue

                logger.debug("Handle message from queue '{}': {}", message.routing_key, message.body)
                await handler.handle(message=message)

    async def start(self):
        logger.info("Starting RabbitMQ Consumer service")

        self._connection = await aio_pika.connect_robust(self._amqp_url, loop=self._loop)
        await self.consume()

    async def stop(self):
        logger.info("Stopping RabbitMQ Consumer service")

        await self._connection.close()


class BaseBrokerProducerService(ServiceMixin):
    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 amqp_url: str,
                 ):
        self._connection = None
        self._loop = loop
        self._amqp_url = amqp_url

    async def send(self, exchange_name: str, routing_key: str, message: BaseModel):
        payload = message.json().encode()

        async with self._connection.channel() as channel:
            exchange = await channel.declare_exchange(exchange_name, type=aio_pika.ExchangeType.FANOUT)
            await exchange.publish(
                aio_pika.Message(payload),
                routing_key=routing_key
            )

        logger.debug("Sent message to exchange '{}', routing_key: {}", exchange_name, routing_key)

    async def start(self):
        logger.info("Starting RabbitMQ Producer service")

        self._connection = await aio_pika.connect_robust(self._amqp_url, loop=self._loop)

    async def stop(self):
        logger.info("Stopping RabbitMQ Producer service")

        await self._connection.close()