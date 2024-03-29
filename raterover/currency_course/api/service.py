from typing import Iterable

import fastapi
from facet import ServiceMixin

from raterover.common.api.service import BaseAPIService
from raterover.common.utils.package import get_version
from raterover.currency_course.database.service import CourseDatabaseService
from raterover.currency_course.settings import CourseSettings

from . import health, router
from ..broker.consumer_service import CourseConsumerBrokerService
from ..broker.producer_service import CourseProducerBrokerService


class CourseAPIService(BaseAPIService):
    def __init__(
            self,
            database: CourseDatabaseService,
            broker_producer_service: CourseProducerBrokerService,
            broker_consumer_service: CourseConsumerBrokerService,
            version: str = "0.0.0",
            port: int = 8000,
            root_url: str = "http://localhost",
            root_path: str = "",
            allowed_origins: Iterable[str] = (),

    ):
        self._database = database
        self._broker_producer_service = broker_producer_service
        self._broker_consumer_service = broker_consumer_service
        super().__init__(
            title="Course",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.add_api_route(path="/health", endpoint=health.health)
        app.include_router(router.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
            self._broker_producer_service,
            self._broker_consumer_service
        ]

    @property
    def database(self) -> CourseDatabaseService:
        return self._database


def get_service(
        database: CourseDatabaseService,
        settings: CourseSettings,
        broker_producer_service: CourseProducerBrokerService,
        broker_consumer_service: CourseConsumerBrokerService,
) -> CourseAPIService:
    return CourseAPIService(
        database=database,
        broker_producer_service=broker_producer_service,
        broker_consumer_service=broker_consumer_service,
        version=get_version() or "0.0.0",
        port=settings.port,
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
    )
