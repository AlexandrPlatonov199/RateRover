import asyncio

import typer
from loguru import logger

from raterover.currency_course.settings import CourseSettings
from raterover.currency_course.database.service import get_service as get_database_service
from .consumer_service import get_service as get_consumer_service


@logger.catch
def run(ctx: typer.Context):
    settings: CourseSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = get_database_service(settings=settings)
    consumer_service = get_consumer_service(
        loop=loop,
        database=database_service,
        settings=settings,
    )

    loop.run_until_complete(consumer_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli
