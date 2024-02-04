import asyncio
from typing import Iterable

from aio_pika import connect_robust, Message, ExchangeType, IncomingMessage
from facet import ServiceMixin
from loguru import logger
from pydantic import BaseModel

from .handler import BaseBrokerHandler


class BaseBrokerConsumerService(ServiceMixin):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        amqp_url: str,
        queues_name: str,
        handlers: Iterable[BaseBrokerHandler] = (),
    ):
        self._handlers = handlers
        self._queue_name = queues_name
        self._amqp_url = amqp_url
        self._connection = None

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            logger.debug("Get message from '{}': {}", message.routing_key, message.body)
            await self.handle(message)

    async def consume(self):
        connection = await connect_robust(self._amqp_url)
        channel = await connection.channel()

        queue = await channel.declare_queue(self._queue_name, durable=False)
        await queue.consume(self.on_message)

    async def handle(self, message: IncomingMessage):
        for handler in self._handlers:
            if not await handler.check(message=message):
                logger.debug("Skip message from '{}': {}", message.routing_key, message.body)
                continue

            logger.debug("Handle message from '{}': {}", message.routing_key, message.body)
            await handler.handle(message=message)

    async def start(self):
        logger.info("Start Broker Consumer service")
        await self.consume()

    async def stop(self):
        logger.info("Stop Broker Consumer service")
        if self._connection:
            await self._connection.close()


class BaseBrokerProducerService(ServiceMixin):
    def __init__(self, loop: asyncio.AbstractEventLoop, amqp_url: str, exchange_name: str):
        self._amqp_url = amqp_url
        self._exchange_name = exchange_name
        self._connection = None

    async def send(self, routing_key: str, message: BaseModel):
        connection = await connect_robust(self._amqp_url)
        channel = await connection.channel()

        exchange = await channel.declare_exchange(self._exchange_name, type=ExchangeType.DIRECT, durable=True)
        payload = message.model_dump_json().encode()

        message = Message(payload, content_type="application/json")
        await exchange.publish(message, routing_key=routing_key)

        logger.debug("Send message to '{}': {}", routing_key, payload)

        await connection.close()

    async def start(self):
        logger.info("Start Broker Producer service")

    async def stop(self):
        logger.info("Stop Broker Producer service")