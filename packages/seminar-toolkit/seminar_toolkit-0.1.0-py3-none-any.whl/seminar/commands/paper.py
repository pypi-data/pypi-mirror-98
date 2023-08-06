""" TODO docstring """
from typing import Union

import requests
import click

from seminar.models import Meeting
from seminar.utils import search, requests_headers
from seminar import pass_config


@click.group(name="paper", help="Strictly interacts with a Meeting's papers.")
@click.option("-n", "--name", "query")
@pass_config
def cli(cfg, query: str = ""):
    search.for_meeting(cfg, query)
    pass


# @task(pre=[preprocess])
@cli.command()
@pass_config
def download(cfg, mtg: Meeting):
    """Downloads papers and names them based on keys for meetings."""
    if mtg.papers is None:
        return

    folder = mtg.as_dir(prefix=cfg.path)

    for title, link in mtg.papers.items():
        try:
            with (folder / f"{title}.pdf").open("wb") as pdf:
                pdf.write(requests.get(link, headers=requests_headers).content)
            # TODO Check for corruptness / PDF headers
        except ConnectionError:
            raise ConnectionError(
                f"Failed to connect to {link}, please check it produces a PDF."
            )
