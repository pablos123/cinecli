"""
Common database functions of all cinemas commands.
"""

import sqlite3


def execute_query(cursor: sqlite3.Cursor, cinema: str, date_int: int) -> list:
    """
    Execute query.
    """
    movies: list = []
    try:
        res = cursor.execute(
            f"SELECT * FROM movies WHERE cinema='{cinema}' AND compare_date <= {date_int};"
        )
        movies = [dict(row) for row in res.fetchall()]
    except sqlite3.OperationalError as _:
        raise _

    return movies
