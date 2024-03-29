from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings


from raterover.common.database.settings import BaseDatabaseSettings
from .config import settings
from ..common.broker.settings import BaseBrokerProducerSettings, BaseBrokerConsumerSettings


class CourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
    BaseBrokerProducerSettings,
    BaseBrokerConsumerSettings,
):
    url_exchange: str = settings.URL_EXCHANGE

    btc_uri: str = settings.BTC_URI

    eth_uri: str = settings.ETH_URI

    api_key_exchange: str = settings.API_KEY_EXCHANGE

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")

    producer_servers: str = "amqp://guest:guest@localhost:5672/"

    consumer_servers: str = "amqp://guest:guest@localhost:5672/"

    queues: str = "binance"



def get_settings() -> CourseSettings:
    return CourseSettings()
