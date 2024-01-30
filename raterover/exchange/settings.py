from pydantic import AnyUrl

from raterover.common.api.settings import BaseAPISettings

from raterover.common.database.settings import BaseDatabaseSettings


class ExchangeSettings(BaseAPISettings, BaseDatabaseSettings):

    db_dsn: AnyUrl = AnyUrl("postgresql+asyncpg://postgres:postgres@localhost:5432/exchange")


def get_settings() -> ExchangeSettings:
    return ExchangeSettings()