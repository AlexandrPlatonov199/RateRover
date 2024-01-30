import typer

from . import exchange


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.add_typer(exchange.get_cli(), name="exchange")

    return cli
