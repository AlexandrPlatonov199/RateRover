from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings
from raterover.common.request_course.settings import BaseRequestSettings
from raterover.common.broker.settings import BaseBrokerProducerSettings, BaseBrokerConsumerSettings

from raterover.common.database.settings import BaseDatabaseSettings


class CurrencyCourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
    BaseRequestSettings,
    BaseBrokerProducerSettings,
    BaseBrokerConsumerSettings,

):

    uri_binance: str = "https://api.binance.com/api/v3/ticker/price"

    uri_coingecko: str = "https://api.coingecko.com/api/v3/simple/price"

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")

    producer_servers: str = "amqp://guest:guest@rabbitmq:5672/"

    consumer_servers: str = "amqp://guest:guest@rabbitmq:5672/"

    queues_name: str = "request_course"

    exchange_name: str = "request_course"


def get_settings() -> CurrencyCourseSettings:
    return CurrencyCourseSettings()
