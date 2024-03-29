import asyncio

import typer
from loguru import logger

from raterover.currency_course.broker.producer_service import get_service as get_broker_producer_service
from raterover.currency_course.broker.consumer_service import get_service as get_broker_consumer_service
from raterover.currency_course import database
from raterover.currency_course.settings import CourseSettings
from .service import get_service


@logger.catch
def run(ctx: typer.Context):
    settings: CourseSettings = ctx.obj["settings"]
    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    broker_producer_service = get_broker_producer_service(loop=loop, settings=settings)
    broker_consumer_service = get_broker_consumer_service(loop=loop, settings=settings, database=database_service)
    api_service = get_service(
        database=database_service,
        settings=settings,
        broker_producer_service=broker_producer_service,
        broker_consumer_service=broker_consumer_service,
    )

    loop.run_until_complete(api_service.run())


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli
