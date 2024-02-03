from typing import Iterable

import fastapi
from facet import ServiceMixin

from raterover.common.api.service import BaseAPIService
# from raterover.common.utils.package import get_version
from raterover.currency_course.database.service import CurrencyCourseDatabaseService
from raterover.currency_course.settings import CurrencyCourseSettings

from . import health, router
from ..broker.producer_service import CourseBrokerProducerService

from ...common.binance import BinanceService


class CurrencyCourseAPIService(BaseAPIService):
    def __init__(
            self,
            database: CurrencyCourseDatabaseService,
            binance_service: BinanceService,
            broker_producer: CourseBrokerProducerService,
            version: str = "0.0.0",
            port: int = 8000,
            root_url: str = "http://localhost",
            root_path: str = "",
            allowed_origins: Iterable[str] = (),

    ):
        self._database = database
        self._binance_service = binance_service
        self._broker_producer = broker_producer

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
            self._binance_service,
        ]

    @property
    def database(self) -> CurrencyCourseDatabaseService:
        return self._database

    @property
    def binance(self) -> BinanceService:
        return self._binance_service

    @property
    def broker_producer(self) -> CourseBrokerProducerService:
        return self._broker_producer


def get_service(
        database: CurrencyCourseDatabaseService,
        settings: CurrencyCourseSettings,
        binance_service: BinanceService,
        broker_producer: CourseBrokerProducerService,
) -> CurrencyCourseAPIService:
    return CurrencyCourseAPIService(
        database=database,
        binance_service=binance_service,
        broker_producer=broker_producer,
        version="0.0.0",
        port=settings.port,
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
    )
