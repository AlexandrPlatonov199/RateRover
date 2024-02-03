import typer

from . import currency_course


def get_cli() -> typer.Typer:
    cli = typer.Typer()

    cli.add_typer(currency_course.get_cli(), name="currency_course")

    return cli
