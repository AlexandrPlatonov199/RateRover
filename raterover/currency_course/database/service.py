import pathlib
from contextlib import asynccontextmanager
from typing import Type

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from raterover.common.database.service import BaseDatabaseService
from .models import CurrencyCourse

from raterover.currency_course.settings import CurrencyCourseSettings


class CurrencyCourseDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    @asynccontextmanager
    async def transaction(self):
        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    async def get_course(self,
                         session: AsyncSession,
                         base_symbol: str,
                         ) -> CurrencyCourse | None:

        stmt = select(CurrencyCourse).filter_by(direction=base_symbol)
        result = await session.execute(stmt)
        course = result.unique().scalar_one_or_none()

        return course

    async def create_course(self,
                            session: AsyncSession,
                            exchanger: str,
                            direction: str,
                            value: float,
                            ) -> CurrencyCourse:

        existing_course = await session.execute(
            select(CurrencyCourse).filter_by(exchanger=exchanger, direction=direction)
        )
        existing_course = existing_course.scalar_one_or_none()

        if existing_course:
            existing_course.value = value
        else:
            existing_course = CurrencyCourse(exchanger=exchanger,
                                             direction=direction,
                                             value=value)

        session.add(existing_course)
        await session.commit()

        return existing_course


def get_service(settings: CurrencyCourseSettings) -> CurrencyCourseDatabaseService:
    return CurrencyCourseDatabaseService(dsn=str(settings.db_dsn))
