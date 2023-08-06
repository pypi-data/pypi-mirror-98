__version__ = "0.1.0"

import click

from seminar import models
from seminar import apis

from seminar.utils import Config

pass_config = click.make_pass_decorator(Config, ensure=True)

from seminar.commands import group, meeting, markdown, notebook, paper
from seminar import cli
