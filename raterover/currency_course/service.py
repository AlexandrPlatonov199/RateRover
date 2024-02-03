from facet import ServiceMixin

from .api.service import CurrencyCourseAPIService
from .broker.producer_service import CourseBrokerProducerService


class CurrencyCourseService(ServiceMixin):
    def __init__(self,
                 api: CurrencyCourseAPIService,
                 broker_producer: CourseBrokerProducerService,
                 ):
        self._api = api
        self._broker_producer = broker_producer

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker_producer,
        ]

    @property
    def api(self) -> CurrencyCourseAPIService:
        return self._api

    @property
    def broker_producer(self) -> CourseBrokerProducerService:
        return self._broker_producer


def get_service(api: CurrencyCourseAPIService,
                broker_producer: CourseBrokerProducerService) -> CurrencyCourseService:
    return CurrencyCourseService(api=api, broker_producer=broker_producer)
