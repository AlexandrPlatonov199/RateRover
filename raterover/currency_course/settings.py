from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings
from raterover.common.request_course.settings import BaseRequestSettings

from raterover.common.database.settings import BaseDatabaseSettings


class CourseSettings(
    BaseAPISettings,
    BaseDatabaseSettings,
    BaseRequestSettings,

):

    uri_binance: str = "https://api.binance.com/api/v3/ticker/price"

    uri_coingecko: str = "https://api.coingecko.com/api/v3/simple/price"

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/currency_course")


def get_settings() -> CourseSettings:
    return CourseSettings()
