import asyncio

from raterover.common.broker.service import BaseBrokerConsumerService
from raterover.currency_course.database.service import CourseDatabaseService
from .handler import CourseConsumerBrokerHandler
from ..settings import CourseSettings


class CourseConsumerBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: CourseDatabaseService,
            amqp_url: str,
            queues: str,
    ):
        handlers = [
            CourseConsumerBrokerHandler(
                database=database,
                queues=queues,
            ),
        ]

        super().__init__(loop=loop, connection_string=amqp_url, queue_name=queues, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: CourseDatabaseService,
        settings: CourseSettings,
) -> CourseConsumerBrokerService:
    return CourseConsumerBrokerService(
        loop=loop,
        database=database,
        amqp_url=settings.consumer_servers,
        queues=settings.queues
    )


