import pathlib
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from raterover.common.database.service import BaseDatabaseService
from .models import Course

from raterover.currency_course.settings import CourseSettings


class CourseDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    @asynccontextmanager
    async def transaction(self):
        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    async def get_course(self,
                         session: AsyncSession,
                         course: str,
                         ) -> Course:

        stmt = select(Course).where(Course.direction == course)
        result = await session.execute(stmt)
        db_course = result.scalars().first()

        return db_course

    async def create_course(self,
                            session: AsyncSession,
                            exchanger: str,
                            direction: str,
                            value: float,
                            ) -> Course:

        existing_course = await session.execute(
            select(Course).filter_by(exchanger=exchanger, direction=direction)
        )
        existing_course = existing_course.scalar_one_or_none()

        if existing_course:
            existing_course.value = value
        else:
            existing_course = Course(exchanger=exchanger,
                                     direction=direction,
                                     value=value)

        session.add(existing_course)
        await session.commit()

        return existing_course


def get_service(settings: CourseSettings) -> CourseDatabaseService:
    return CourseDatabaseService(dsn=str(settings.db_dsn))
