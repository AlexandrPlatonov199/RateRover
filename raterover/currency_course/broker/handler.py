from typing import Iterable

import aio_pika
from loguru import logger

from raterover.common.broker.handler import BaseBrokerHandler
from raterover.common.broker.models.course import Course
from raterover.currency_course.database.service import CurrencyCourseDatabaseService


class CourseBrokerConsumerHandler(BaseBrokerHandler):
    def __init__(
            self,
            database: CurrencyCourseDatabaseService,
            queues_name: str | None = None,
    ):
        self._database = database

        super().__init__(queues_name=queues_name)

    async def handle(self, message: aio_pika.IncomingMessage):
        course = Course.model_validate_json(json_data=message.body)
        logger.info("course {}", course)

        async with self._database.transaction() as session:
            await self._database.create_course(
                session=session,
                exchanger=course.exchanger,
                direction=course.direction,
                value=course.value,
            )

    @property
    def database(self) -> CurrencyCourseDatabaseService:
        return self._database
