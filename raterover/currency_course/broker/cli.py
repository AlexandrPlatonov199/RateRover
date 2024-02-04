import asyncio

import typer
from loguru import logger

from raterover.currency_course.database import get_service as get_service_database
from raterover.currency_course.settings import CurrencyCourseSettings

from .consumer_service import get_service as get_service_consumer


@logger.catch
def run(ctx: typer.Context):
    settings: CurrencyCourseSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = get_service_database(settings=settings)
    consumer_service = get_service_consumer(
        loop=loop,
        database=database_service,
        settings=settings,
    )

    loop.run_until_complete(consumer_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli
