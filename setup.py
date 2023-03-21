"""
Setup function
"""

from setuptools import setup

setup(
    name="cinecli",
    version="0.2.0",
    description="Cli program that shows movies available for watching in El Cario cinema",
    author="Pablo Saavedra",
    url="https://github.com/pablos123/cinecli",
    author_email="pablosaavedra123@gmail.com",
    py_modules=[
        "cinecli.main",
        "cinecli.commands",
        "cinecli.commands.elcairo",
        "cinecli.commands.database",
        "cinecli.commands.lib",
        "cinecli.commands.lib.movie_printer",
        "cinecli.commands.lib.database_utils",
        "cinecli.apis",
        "cinecli.apis.elcairo",
    ],
    python_requires=">=3.10",
    install_requires=[
        "ics",
        "icalendar",
        "climage",
        "requests",
        "colorama",
        "click",
        "arrow",
        "beautifulsoup4",
        "progress",
    ],
    entry_points={
        "console_scripts": [
            "cinecli = cinecli.main:main",
        ]
    },
)