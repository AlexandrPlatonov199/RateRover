import asyncio

from raterover.common.broker.models.course import Course
from raterover.common.broker.service import BaseBrokerProducerService
from raterover.currency_course.settings import CurrencyCourseSettings


class CourseBrokerProducerService(BaseBrokerProducerService):
    async def send_create_course(self, course):
        course_data = Course(exchanger=course["exchanger"],
                             direction=course["direction"],
                             value=course["value"],
                             )
        await self.send(routing_key="", message=course_data)



def get_service(
    loop: asyncio.AbstractEventLoop,
    settings: CurrencyCourseSettings,
) -> CourseBrokerProducerService:
    return CourseBrokerProducerService(
        loop=loop,
        amqp_url=settings.producer_servers,
        exchange_name=settings.exchange_name,
    )