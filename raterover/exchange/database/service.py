import pathlib

from raterover.common.database.service import BaseDatabaseService

from raterover.exchange.settings import ExchangeSettings


class ExchangeDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"


def get_service(settings: ExchangeSettings) -> ExchangeDatabaseService:
    return ExchangeDatabaseService(dsn=str(settings.db_dsn))
