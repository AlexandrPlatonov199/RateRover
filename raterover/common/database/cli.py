from typing import Optional

import typer
from loguru import logger

from .service import BaseDatabaseService


@logger.catch
def migrations_list(ctx: typer.Context):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.show_migrations()


@logger.catch
def migrations_apply(ctx: typer.Context):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.migrate()


@logger.catch
def migrations_rollback(
    ctx: typer.Context,
    revision: Optional[str] = typer.Argument(
        None,
        help="Revision id or relative revision (`-1`, `-2`)",
    ),
):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.rollback(revision=revision)


@logger.catch
def migrations_create(
        ctx: typer.Context,
        message: Optional[str] = typer.Option(
            None,
            "-m", "--message",
            help="Migration short message",
        ),
):
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.create_migration(message=message)


def get_migrations_cli() -> typer.Typer:
    cli = typer.Typer(name="Migration")

    cli.command(name="apply")(migrations_apply)
    cli.command(name="rollback")(migrations_rollback)
    cli.command(name="create")(migrations_create)
    cli.command(name="list")(migrations_list)

    return cli