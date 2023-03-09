"""
El Cairo command group.
"""

import os
import sqlite3
from sqlite3.dbapi2 import Connection

import arrow
import click
from arrow import Arrow

from .lib.database_utils import execute_query
from .lib.movie_printer import MoviePrinter


@click.group()
@click.pass_context
def elcairo(ctx) -> None:
    """
    Print El Cairo movie shows.
    """
    script_dir: str = os.path.realpath(os.path.dirname(__file__))
    database_file: str = os.path.join(script_dir, "cinecli.db")

    if not os.path.exists(database_file):
        click.echo("Create the database first!...")
        ctx.exit(1)

    connection: Connection = sqlite3.connect(database_file)

    connection.row_factory = sqlite3.Row
    ctx.obj["cursor"] = connection.cursor()

    ctx.obj["printer"] = MoviePrinter(
        images=ctx.obj["images"],
        no_extra_info=ctx.obj["no_extra_info"],
        urls=ctx.obj["urls"],
    )


@elcairo.command()
@click.pass_context
def today(ctx) -> None:
    """
    Print todays movie shows.
    """
    date_int: int = int(arrow.now().format("YYYYMMDD"))
    ctx.ob["printer"].echo_query(ctx.obj["cursor"], "elcairo", date_int)


@elcairo.command()
@click.pass_context
def tomorrow(ctx) -> None:
    """
    Print tomorrow movie shows.
    """
    date_int: int = int(arrow.now().dehumanize("in a day").format("YYYYMMDD"))
    ctx.ob["printer"].echo_query(ctx.obj["cursor"], "elcairo", date_int)


@elcairo.command()
@click.pass_context
def upcoming(ctx) -> None:
    """
    Print upcoming movie shows.
    """
    date_int: int = int(arrow.now().format("YYYYMMDD"))
    ctx.ob["printer"].echo_query(ctx.obj["cursor"], "elcairo", date_int)


@elcairo.command()
@click.option("--date", type=click.DateTime(formats=["%d-%m-%Y"]), required=True)
@click.pass_context
def day(ctx, date) -> None:
    """
    Print movie shows of a given date.
    """
    year: str = str(date.year).zfill(4)
    month: str = str(date.month).zfill(2)
    day_date: str = str(date.day).zfill(2)

    date_arrow: Arrow = arrow.get(f"{year}-{month}-{day_date}")
    date_int: int = int(date_arrow.format("YYYYMMDD"))
    ctx.ob["printer"].echo_query(ctx.obj["cursor"], "elcairo", date_int)


@elcairo.command()
@click.option("--date", type=click.DateTime(formats=["%d-%m-%Y"]), required=True)
@click.pass_context
def until(ctx, date) -> None:
    """
    Print movie shows until a given date.
    """
    year: str = str(date.year).zfill(4)
    month: str = str(date.month).zfill(2)
    day_date: str = str(date.day).zfill(2)

    date_arrow: Arrow = arrow.get(f"{year}-{month}-{day_date}")
    date_int: int = int(date_arrow.format("YYYYMMDD"))
    ctx.ob["printer"].echo_query(ctx.obj["cursor"], "elcairo", date_int)
