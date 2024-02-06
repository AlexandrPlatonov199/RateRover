from facet import ServiceMixin

from .api.service import CourseAPIService
from .binance.service import BinanceCourseService


class CourseService(ServiceMixin):
    def __init__(self,
                 api: CourseAPIService,
                 binance_course: BinanceCourseService,
                 ):
        self._api = api
        self._binance_course = binance_course

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._binance_course
        ]

    @property
    def api(self) -> CourseAPIService:
        return self._api

    @property
    def binance_course(self) -> BinanceCourseService:
        return self._binance_course


def get_service(api: CourseAPIService,
                binance_course: BinanceCourseService,
                ) -> CourseService:
    return CourseService(api=api, binance_course=binance_course)

