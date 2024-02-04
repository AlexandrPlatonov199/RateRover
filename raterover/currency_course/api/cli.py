import asyncio

import typer
from loguru import logger

from raterover.currency_course.broker.producer_service import get_service as get_producer_service
from raterover.currency_course import database
from raterover.currency_course.settings import CurrencyCourseSettings

from .service import get_service
from ...common.binance import get_binance_course


@logger.catch
def run(ctx: typer.Context):
    settings: CurrencyCourseSettings = ctx.obj["settings"]
    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    binance_service = get_binance_course(settings=settings)
    broker_producer = get_producer_service(loop=loop, settings=settings)
    api_service = get_service(
        database=database_service,
        settings=settings,
        binance_service=binance_service,
        broker_producer=broker_producer,
    )

    loop.run_until_complete(api_service.run())




def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.command(name="run")(run)

    return cli
