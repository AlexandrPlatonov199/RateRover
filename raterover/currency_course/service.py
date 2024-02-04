from facet import ServiceMixin

from .api.service import CurrencyCourseAPIService
from .broker.consumer_service import CourseBrokerConsumerService
from .broker.producer_service import CourseBrokerProducerService


class CurrencyCourseService(ServiceMixin):
    def __init__(self,
                 api: CurrencyCourseAPIService,
                 broker_producer: CourseBrokerProducerService,
                 broker_consumer: CourseBrokerConsumerService,
                 ):
        self._api = api
        self._broker_producer = broker_producer
        self._broker_consumer = broker_consumer

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker_producer,
            self._broker_consumer,
        ]

    @property
    def api(self) -> CurrencyCourseAPIService:
        return self._api

    @property
    def broker_producer(self) -> CourseBrokerProducerService:
        return self._broker_producer

    @property
    def broker_consumer(self) -> CourseBrokerConsumerService:
        return self._broker_consumer


def get_service(api: CurrencyCourseAPIService,
                broker_producer: CourseBrokerProducerService,
                broker_consumer: CourseBrokerConsumerService,
                ) -> CurrencyCourseService:
    return CurrencyCourseService(api=api,
                                 broker_producer=broker_producer,
                                 broker_consumer=broker_consumer)
