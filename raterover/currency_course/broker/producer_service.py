import asyncio

from raterover.common.broker.models.models import CourseMessageModel
from raterover.common.broker.service import BaseBrokerProducerService
from raterover.currency_course.settings import CourseSettings


class CourseProducerBrokerService(BaseBrokerProducerService):

    async def send_message(self,
                           exchange_name,
                           message,
                           ):
        message_data = CourseMessageModel(**message)
        await self.send(exchange_name=exchange_name, routing_key="", message=message_data)


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: CourseSettings,
) -> CourseProducerBrokerService:
    return CourseProducerBrokerService(
        loop=loop,
        amqp_url=settings.producer_servers,
    )