from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings


from raterover.common.database.settings import BaseDatabaseSettings


class CourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
):
    url_exchange: str = "https://open.er-api.com/v6/latest/USD"

    btc_uri: str = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    eth_uri: str = "wss://stream.binance.com:9443/ws/ethusdt@trade"

    api_key_exchange: str = "0cfb8c9c7ef4aee82c72de7e"

    producer_servers: str = "amqp://guest:guest@localhost/"

    uri_binance: str = "https://api.binance.com/api/v3/ticker/price"

    uri_coingecko: str = "https://api.coingecko.com/api/v3/simple/price"

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")


def get_settings() -> CourseSettings:
    return CourseSettings()
