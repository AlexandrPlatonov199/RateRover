from typing import Iterable
import aio_pika

class BaseBrokerHandler:
    def __init__(self, queues: Iterable[str] | None = None):
        self._queues = queues

    async def check(self, message: aio_pika.IncomingMessage) -> bool:
        if self._queues is not None and message.routing_key not in self._queues:
            return False

        return await self.custom_check(message=message)

    async def custom_check(self, message: aio_pika.IncomingMessage) -> bool:
        return True

    async def handle(self, message: aio_pika.IncomingMessage):
        pass