from facet import ServiceMixin

from .api.service import CourseAPIService


class CourseService(ServiceMixin):
    def __init__(self,
                 api: CourseAPIService,
                 ):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
        ]

    @property
    def api(self) -> CourseAPIService:
        return self._api


def get_service(api: CourseAPIService,
                ) -> CourseService:
    return CourseService(api=api)

