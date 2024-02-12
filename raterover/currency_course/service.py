from facet import ServiceMixin

from .api.service import CourseAPIService
from .binance.service import BinanceCourseService
from .broker.consumer_service import CourseConsumerBrokerService
from .broker.producer_service import CourseProducerBrokerService
from ..common.broker.service import BaseBrokerProducerService


class CourseService(ServiceMixin):
    def __init__(self,
                 api: CourseAPIService,
                 binance_course: BinanceCourseService,
                 broker_producer: CourseProducerBrokerService,
                 broker_consumer: CourseConsumerBrokerService,
                 ):
        self._api = api
        self._binance_course = binance_course
        self._broker_producer = broker_producer
        self._broker_consumer = broker_consumer

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._binance_course,
            self._broker_producer,
            self._broker_consumer,
        ]

    @property
    def api(self) -> CourseAPIService:
        return self._api

    @property
    def binance_course(self) -> BinanceCourseService:
        return self._binance_course

    @property
    def broker_producer(self) -> CourseProducerBrokerService:
        return self._broker_producer

    @property
    def broker_consumer(self) -> CourseConsumerBrokerService:
        return self._broker_consumer


def get_service(
        api: CourseAPIService,
        binance_course: BinanceCourseService,
        broker_producer: CourseProducerBrokerService,
        broker_consumer: CourseConsumerBrokerService,
                ) -> CourseService:
    return CourseService(
        api=api,
        binance_course=binance_course,
        broker_producer=broker_producer,
        broker_consumer=broker_consumer,
    )


