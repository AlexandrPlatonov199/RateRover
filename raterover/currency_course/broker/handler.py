import aio_pika

from raterover.common.broker.handler import BaseBrokerHandler
from raterover.common.broker.models.models import CourseMessageModel
from raterover.currency_course.database.service import CourseDatabaseService


class CourseConsumerBrokerHandler(BaseBrokerHandler):
    def __init__(
            self,
            database: CourseDatabaseService,
            queues: str | None = None,

    ):
        self._database = database

        super().__init__(queues=queues)

    async def handle(self, message: aio_pika.abc.AbstractIncomingMessage):
        course = CourseMessageModel.model_validate_json(json_data=message.body)

        try:

            async with self._database.transaction() as session:
                await self._database.create_course(
                    session=session,
                    exchanger=course.exchanger,
                    direction=course.direction,
                    value=course.value
                )
        except Exception as e:
            return e

    @property
    def database(self) -> CourseDatabaseService:
        return self._database

