import asyncio

import typer
from loguru import logger

from . import api, database, binance, broker
from .broker.consumer_service import get_service as get_consumer_service
from .broker.producer_service import get_service as get_producer_service
from .service import get_service
from .settings import CourseSettings, get_settings




@logger.catch
def run(ctx: typer.Context):
    settings: CourseSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    broker_producer_service = get_producer_service(loop=loop, settings=settings)
    broker_consumer_service = get_consumer_service(loop=loop, database=database_service, settings=settings)
    binance_course = binance.get_binan(settings=settings,
                                       database=database_service,
                                       broker_producer=broker_producer_service)

    api_service = api.get_service(
        database=database_service,
        settings=settings,
        broker_producer_service=broker_producer_service,
        broker_consumer_service=broker_consumer_service
    )
    currency_course_service = get_service(api=api_service,
                                          binance_course=binance_course,
                                          broker_producer=broker_producer_service,
                                          broker_consumer=broker_consumer_service,
                                          )

    loop.run_until_complete(currency_course_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(database.get_cli(), name="database")
    cli.add_typer(broker.get_cli(), name="broker")

    return cli
