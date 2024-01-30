import pathlib
from contextlib import asynccontextmanager

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from loguru import logger
from facet import ServiceMixin
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class BaseDatabaseService(ServiceMixin):
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._engine = create_async_engine(self._dsn, pool_recycle=60)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_alembic_config_path(self) -> pathlib.Path:
        raise NotImplementedError

    def get_alembic_config(self) -> AlembicConfig:
        migrations_path = self.get_alembic_config_path()

        config = AlembicConfig()
        config.set_main_option("script_location", str(migrations_path))
        config.set_main_option("sqlalchemy.url", self._dsn.replace("%", "%%"))

        return config

    @asynccontextmanager
    async def transaction(self):
        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    def migrate(self):
        alembic_command.upgrade(self.get_alembic_config(), "head")

    def rollback(self, revision: str | None = None):
        revision = revision or "-1"

        alembic_command.downgrade(self.get_alembic_config(), revision)

    def show_migrations(self):
        alembic_command.history(self.get_alembic_config())

    def create_migration(self, message: str | None = None):
        alembic_command.revision(
            self.get_alembic_config(), message=message, autogenerate=True,
        )

    async def start(self):
        logger.info("Start Database service")

    async def stop(self):
        logger.info("Stop Database service")