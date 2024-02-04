from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings
from raterover.common.binance.settings import BaseBinanceSettings
from raterover.common.broker.settings import BaseBrokerProducerSettings, BaseBrokerConsumerSettings

from raterover.common.database.settings import BaseDatabaseSettings


class CurrencyCourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
    BaseBinanceSettings,
    BaseBrokerProducerSettings,
    BaseBrokerConsumerSettings,

):

    uri: str = "wss://stream.binance.com:9443/ws/"

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")

    producer_servers: str = "amqp://guest:guest@localhost/"

    consumer_servers: str = "amqp://guest:guest@localhost/"

    queues_name: str = "binance"

    exchange_name: str = "binance"


def get_settings() -> CurrencyCourseSettings:
    return CurrencyCourseSettings()
