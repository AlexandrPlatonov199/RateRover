from facet import ServiceMixin

from .api.service import ExchangeAPIService


class ExchangeService(ServiceMixin):
    def __init__(self, api: ExchangeAPIService):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api
        ]

    @property
    def api(self) -> ExchangeAPIService:
        return self._api


def get_service(api: ExchangeAPIService) -> ExchangeService:
    return ExchangeService(api=api)
