"""
El Cairo command.
"""

import json
import os
import shutil
import sqlite3
import threading
from functools import partial
from time import sleep

import arrow
import click
import climage
import requests
from colorama import Fore, Style
from progress.spinner import MoonSpinner

from ..apis.elcairo import ElCairo


def get_ascii_image(url: str, uid: str) -> str:
    """
    Creates a temporal file reads it, removes it and return the ascii art.
    """
    output: str = ""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        file_name = f"/tmp/{uid}.jpeg"
        with open(file_name, "wb") as image_file:
            shutil.copyfileobj(response.raw, image_file)
            output = climage.convert(file_name)
        os.remove(file_name)
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException,
        OSError,
    ) as _:
        output = "[Cannot show image...]"

    return output


def loading(task: str, thread: threading.Thread) -> None:
    """
    Echo a task with a spinner
    """
    with MoonSpinner(task + "...  ") as spinner:
        while thread.is_alive():
            sleep(0.1)
            spinner.next()


@click.group()
@click.option("--silent", is_flag=True, show_default=True)
@click.pass_context
def database(ctx, silent) -> None:
    """
    Populate or clean the database.
    """
    if not silent:
        click.echo("📽️ Executing tasks 📽️")

    ctx.obj["silent"] = silent

    def bye_msg(silent):
        if not silent:
            click.echo("📽️ All finished 📽️")

    bye_call = partial(bye_msg, silent)
    ctx.call_on_close(bye_call)


@database.command()
@click.pass_context
def populate(ctx) -> None:
    """
    Populate the database.
    """
    script_dir: str = os.path.realpath(os.path.dirname(__file__))
    database_file: str = os.path.join(script_dir, "cinecli.db")
    if os.path.exists(database_file):
        try:
            os.remove(database_file)
        except OSError as _:
            if not ctx.obj["silent"]:
                click.echo("Cannot remove cinecli.db, try again...")
            ctx.exit(1)

    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    create_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        compare_date INT NOT NULL,
        synopsis TEXT NOT NULL,
        direction TEXT NOT NULL,
        cast TEXT NOT NULL,
        genre TEXT NOT NULL,
        duration TEXT NOT NULL,
        origin TEXT NOT NULL,
        year TEXT NOT NULL,
        age TEXT NOT NULL,
        cost TEXT NOT NULL,
        image TEXT NOT NULL,
        urls TEXT NOT NULL,
        cinema TEXT NOT NULL
    );"""

    if not ctx.obj["silent"]:
        click.echo(f"Using database {database_file}")
        click.echo("Creating the table...")

    cursor.execute(create_query)

    def get_events(events_dict: dict):
        elcairo: ElCairo = ElCairo()
        events_dict.update(json.loads(elcairo.get_upcoming_shows_json()))

    events_dict: dict = {}
    thread_fetch: threading.Thread = threading.Thread(
        target=get_events, args=(events_dict,)
    )

    thread_fetch.start()

    if not ctx.obj["silent"]:
        click.echo(f"{Fore.BLUE}El Cairo Cinema{Style.RESET_ALL}")
        # This will wait for thread to finish
        loading("Fetching data", thread_fetch)

    # If you go silent wait for the thread, anyway close the thread safely
    thread_fetch.join()

    if not ctx.obj["silent"]:
        click.echo(f"Fetched {len(events_dict)} movies...")

    def create_events(events_dict: dict, data_insert: list):
        for uid, movie_data in events_dict.items():
            event = (
                movie_data["name"],
                str(arrow.get(movie_data["date"])),
                int(arrow.get(movie_data["date"]).format("YYYYMMDD")),
                movie_data["synopsis"],
                movie_data["direction"],
                movie_data["cast"],
                movie_data["genre"],
                movie_data["duration"],
                movie_data["origin"],
                movie_data["year"],
                movie_data["age"],
                movie_data["cost"],
                get_ascii_image(movie_data["image_url"], uid),
                " ".join(movie_data["urls"]),
                "elcairo",
            )
            data_insert.append(event)

    data_insert: list = []
    thread_events: threading.Thread = threading.Thread(
        target=create_events,
        args=(
            events_dict,
            data_insert,
        ),
    )

    thread_events.start()

    if not ctx.obj["silent"]:
        loading("Creating events", thread_events)

    thread_events.join()

    cursor.executemany(
        """
        INSERT INTO movies (
            'name',
            'date',
            'compare_date',
            'synopsis',
            'direction',
            'cast',
            'genre',
            'duration',
            'origin',
            'year',
            'age',
            'cost',
            'image',
            'urls',
            'cinema')
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        data_insert,
    )

    if not ctx.obj["silent"]:
        click.echo("Populating the table...")

    connection.commit()


@database.command()
@click.pass_context
def clean(ctx) -> None:
    """
    Clean the database.
    """
    if not ctx.obj["silent"]:
        click.echo("Deleting the database...")

    script_dir: str = os.path.realpath(os.path.dirname(__file__))
    database_file: str = os.path.join(script_dir, "cinecli.db")
    if not os.path.exists(database_file):
        if not ctx.obj["silent"]:
            click.echo("The database does not exists!")
        ctx.exit(1)

    try:
        os.remove(database_file)
    except OSError as _:
        if not ctx.obj["silent"]:
            click.echo("Cannot remove cinecli.db, try again...")
        ctx.exit(1)
