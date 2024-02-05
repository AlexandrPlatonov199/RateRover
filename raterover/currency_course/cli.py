import asyncio

import typer
from loguru import logger

from . import api, database

from .service import get_service
from .settings import CourseSettings, get_settings
from ..common.request_course import get_request_service


@logger.catch
def run(ctx: typer.Context):
    settings: CourseSettings = ctx.obj["settings"]

    loop = asyncio.get_event_loop()
    database_service = database.get_service(settings=settings)
    request_service = get_request_service(settings=settings)
    api_service = api.get_service(
        database=database_service,
        settings=settings,
        request_service=request_service,
    )
    currency_course_service = get_service(api=api_service)

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

    return cli
