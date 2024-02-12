import asyncio
import json

from typing import Iterable


import aio_pika

from facet import ServiceMixin
from loguru import logger
from pydantic import BaseModel

from .handler import BaseBrokerHandler
from .models.models import CourseMessageModel


class BaseBrokerConsumerService(ServiceMixin):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        connection_string: str,
        queue_name: str,
        handlers: Iterable[BaseBrokerHandler] = (),
    ):
        self._handlers = handlers
        self._connection_string = connection_string
        self._queue_name = queue_name
        self._loop = loop

    async def consume(self):
        connection = await aio_pika.connect(self._connection_string, loop=self._loop)


        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
                self._queue_name,
                durable=False,

            )

        await queue.consume(self.on_message)

        print(" [*] Waiting for messages. To exit press CTRL+C")

    async def on_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            await self.handle(message)

    async def handle(self, message: aio_pika.abc.AbstractIncomingMessage):
        for handler in self._handlers:
            if not await handler.check(message=message):
                logger.debug("Skip message from '{}': {}", self._queue_name, message.body)
                continue

            logger.debug("Handle message from '{}': {}", self._queue_name, message.body)
            await handler.handle(message=message)

    async def start(self):
        logger.info("Start Broker Consumer service")

        self.add_task(self.consume())

    async def stop(self):
        logger.info("Stop Broker Consumer service")


class BaseBrokerProducerService(ServiceMixin):
    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 amqp_url: str,
                 ):
        self._connection = None
        self._loop = loop
        self._amqp_url = amqp_url

    async def send(self, routing_key: str, message: BaseModel):
        self._connection = await aio_pika.connect(self._amqp_url, loop=self._loop)



        channel = await self._connection.channel()

        payload = message.json().encode()

        message = aio_pika.Message(
            payload, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await channel.default_exchange.publish(
            message, routing_key=routing_key,
            )

        logger.debug("Sent message to routing_key '{}'", routing_key)

    async def start(self):
        logger.info("Starting RabbitMQ Producer service")

    async def stop(self):
        logger.info("Stopping RabbitMQ Producer service")

        await self._connection.close()