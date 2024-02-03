import asyncio

from raterover.common.broker.service import BaseBrokerProducerService
from raterover.currency_course.settings import CurrencyCourseSettings


class CourseBrokerProducerService(BaseBrokerProducerService):
    pass


def get_service(
    loop: asyncio.AbstractEventLoop,
    settings: CurrencyCourseSettings,
) -> CourseBrokerProducerService:
    return CourseBrokerProducerService(
        loop=loop,
        amqp_url=settings.producer_servers,
    )