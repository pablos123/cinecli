"""Print movies"""
import sqlite3

import arrow
import click
from arrow import Arrow
from colorama import Back, Fore, Style

from .database_utils import execute_query

DEFAULT = "[Nothing to show...]"


def truncate(string: str, start_len: int = 0):
    """
    Truncate a string to only be 80 characters long.
    start_len represents the lenght of a title for the string.
    """
    first_line_len = 80 - start_len

    if len(string) <= first_line_len:
        return string.replace("\n", " ").strip()

    out: str = ""
    lines: list[str] = [string[0:first_line_len]]
    lines.extend([string[i: i + 80]
                 for i in range(first_line_len, len(string), 80)])
    for line in lines:
        out += f"{line}\n"

    return out.strip()


class MoviePrinter:
    """
    Movie printing utilities for echoing with click.
    """

    def __init__(self, images: bool, no_extra_info: bool, urls: bool):
        self.images = images
        self.no_extra_info = no_extra_info
        self.urls = urls

    def echo_query(self, cursor: sqlite3.Cursor, cinema: str, date_int: int) -> None:
        """
        Print a cinema's movie shows after the execution
        of the cinema query in a particular cursor.
        """

        try:
            movies = execute_query(cursor, cinema, date_int)
            self.echo_list(movies)
        except sqlite3.OperationalError:
            click.echo(
                "There is something wrong with the database, populate again...")

    def echo_list(self, movies: list) -> None:
        """
        Print a list of movies
        """

        for movie in movies:
            click.echo(f"{Back.WHITE}{Fore.BLACK}{80*'-'}{Style.RESET_ALL}\n")

            self.echo_title(movie)

            if self.images:
                self.echo_image(movie)

            if not self.no_extra_info:
                self.echo_extra_info(movie)

            if self.urls:
                self.echo_urls(movie)

            click.echo()

    @staticmethod
    def echo_title(movie: dict) -> None:
        """
        Echo the movie title with the date of the show.
        """

        def get_nice_date(event_date: str) -> str:
            """
            Format the date information a return a nice show's date
            """
            if not event_date:
                return DEFAULT

            arrow_date: Arrow = arrow.get(event_date)
            format_date: str = arrow_date.format("DD-MM-YYYY HH:mm:ss")
            human_date: str = arrow_date.humanize(locale="es")

            return f"{format_date} ({human_date})"

        name: str = movie["name"] or DEFAULT

        date = get_nice_date(movie["date"])

        click.echo(
            f"{Style.BRIGHT}{Style.BRIGHT}{name}{Style.RESET_ALL}   {date}")

    @staticmethod
    def echo_image(movie) -> None:
        """
        Echo an image.
        """
        image = movie["image"] or DEFAULT
        click.echo(f"\n{image}")

    @staticmethod
    def echo_extra_info(movie: dict) -> None:
        """
        Echo extra info.
        """

        def echo_extra_info_data(
            data: str,
            title: str,
            color: str = Fore.YELLOW,
        ) -> None:
            """
            Echo data in the extra info.
            """

            if not data:
                data = DEFAULT

            click.echo(
                f"{color}{title}{Style.RESET_ALL}{truncate(data, len(title))}")

        synopsis = movie["synopsis"] or DEFAULT

        click.echo(f"\n{Style.DIM}{truncate(synopsis)}{Style.RESET_ALL}\n")

        click.echo(f"{Style.BRIGHT}{80*'*'}{Style.RESET_ALL}")

        echo_extra_info_data(movie["direction"], "Dirección: ")
        echo_extra_info_data(movie["cast"], "Elenco: ")
        echo_extra_info_data(movie["genre"], "Género: ")
        echo_extra_info_data(movie["duration"], "Duración: ")
        echo_extra_info_data(movie["origin"], "Origen: ")
        echo_extra_info_data(movie["year"], "Año: ")
        echo_extra_info_data(movie["age"], "Calificación: ")

        click.echo(f"{Style.BRIGHT}{80*'*'}{Style.RESET_ALL}\n")

        echo_extra_info_data(movie["cost"], "Valor: ", Fore.GREEN)

    @staticmethod
    def echo_urls(movie: dict) -> None:
        """
        Add new lines to the urls list.
        """
        click.echo(f"\n{Fore.YELLOW}Más info:{Style.RESET_ALL}")
        if not movie["urls"]:
            click.echo(DEFAULT)

        click.echo(movie["urls"].replace(" ", "\n"))
