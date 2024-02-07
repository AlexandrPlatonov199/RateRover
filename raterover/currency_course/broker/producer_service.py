import asyncio

from raterover.common.broker.service import BaseBrokerProducerService
from raterover.currency_course.settings import CourseSettings


class CourseProducerBrokerService(BaseBrokerProducerService):

    async def send_message(self,
                           queue,
                           message,
                           ):
        await self.send(queue=queue, message=message)


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: CourseSettings,
) -> CourseProducerBrokerService:
    return CourseProducerBrokerService(
        loop=loop,
        amqp_url=settings.producer_servers,
    )