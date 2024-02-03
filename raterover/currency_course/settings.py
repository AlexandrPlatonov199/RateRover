from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings
from raterover.common.binance.settings import BaseBinanceSettings
from raterover.common.broker.settings import BaseBrokerProducerSettings

from raterover.common.database.settings import BaseDatabaseSettings


class CurrencyCourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
    BaseBinanceSettings,
    BaseBrokerProducerSettings,

):

    uri: str = "wss://stream.binance.com:9443/ws/!ticker@arr"

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")

    producer_servers: str = "amqp://guest:guest@localhost/"


def get_settings() -> CurrencyCourseSettings:
    return CurrencyCourseSettings()
