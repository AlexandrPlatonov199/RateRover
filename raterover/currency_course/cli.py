import asyncio

import typer
from loguru import logger

from . import api, database, broker
from .broker.producer_service import get_service as get_service_producer
from .broker.consumer_service import get_service as get_service_consumer
from .service import get_service
from .settings import CurrencyCourseSettings, get_settings
from ..common.binance import get_binance_course


@logger.catch
def run(ctx: typer.Context):
    settings: CurrencyCourseSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    binance_service = get_binance_course(settings=settings)
    broker_producer = get_service_producer(loop=loop, settings=settings)
    api_service = api.get_service(
        database=database_service,
        settings=settings,
        binance_service=binance_service,
        broker_producer=broker_producer
    )
    broker_consumer = get_service_consumer(
        loop=loop,
        database=database_service,
        settings=settings,
    )
    currency_course_service = get_service(api=api_service,
                                          broker_producer=broker_producer,
                                          broker_consumer=broker_consumer)

    loop.run_until_complete(currency_course_service.run())

    # asyncio.run(currency_course_service.run())


def settings_callback(ctx: typer.Context):
    ctx.obj = ctx.obj or {}
    ctx.obj["settings"] = get_settings()


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.callback()(settings_callback)
    cli.command(name="run")(run)
    cli.add_typer(api.get_cli(), name="api")
    cli.add_typer(broker.get_cli(), name="broker")
    cli.add_typer(database.get_cli(), name="database")

    return cli
