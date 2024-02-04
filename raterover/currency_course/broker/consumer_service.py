import asyncio
from typing import Iterable

from raterover.common.broker.service import BaseBrokerConsumerService
from raterover.currency_course.broker.handler import CourseBrokerConsumerHandler
from raterover.currency_course.database.service import CurrencyCourseDatabaseService
from raterover.currency_course.settings import CurrencyCourseSettings


class CourseBrokerConsumerService(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: CurrencyCourseDatabaseService,
            amqp_url: str,
            queues_name: str,
    ):
        handlers = [
            CourseBrokerConsumerHandler(
                database=database,
                queues_name=queues_name,
            ),
        ]

        super().__init__(loop=loop, amqp_url=amqp_url, queues_name=queues_name, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: CurrencyCourseDatabaseService,
        settings: CurrencyCourseSettings,
) -> CourseBrokerConsumerService:
    return CourseBrokerConsumerService(
        loop=loop,
        database=database,
        amqp_url=settings.consumer_servers,
        queues_name=settings.queues_name,
    )
