import fastapi
from loguru import logger

from raterover.currency_course.database.models import Course
from raterover.currency_course.database.service import CourseDatabaseService


async def get_path_course(
        request: fastapi.Request,
        course: str,
) -> Course:
    database: CourseDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_course = await database.get_course(session=session, course=course)
        logger.info("db_course {}", db_course)

    return db_course
