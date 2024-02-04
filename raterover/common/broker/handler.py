import aio_pika
from typing import Iterable

class BaseBrokerHandler:
    def __init__(self, queues_name: str | None = None):
        self._queue_name = queues_name

    async def check(self, message: aio_pika.IncomingMessage) -> bool:
        if self._queue_name is not None and message.routing_key not in self._queue_name:
            return False

        return await self.custom_check(message=message)

    async def custom_check(self, message: aio_pika.IncomingMessage) -> bool:
        return True

    async def handle(self, message: aio_pika.IncomingMessage):
        pass