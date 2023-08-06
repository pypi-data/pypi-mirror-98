"""TODO docstring"""
from hashlib import sha256
from typing import Union

import click
from click import Context

from seminar.apis import hugo
from seminar.models import Meeting
from seminar.utils import search, j2env, Config
from seminar import pass_config


@click.group(
    name="markdown",
    help="Strictly interacts with a Meeting's associated Markdown Summary.",
)
@click.option("-n", "--name", "query")
@pass_config
def cli(cfg, query: str = ""):
    search.for_meeting(cfg, query)
    pass


@cli.command()
@click.pass_context
def make_summaryfile(ctx: Context, mtg: Meeting):
    ext = ctx.obj.settings.suffixes.simplesummary
    path = mtg.as_file(prefix=ctx.obj.path).with_suffix(ext)

    if not path.exists() or path.stat().st_size == 0:
        simple_instructions = j2env.get_template("summaryfile.md.j2")
        with path.open("w") as f:
            f.write(simple_instructions.render(meeting=mtg))


@cli.command()
@click.pass_context
def make_post(ctx: Context, mtg: Meeting, weight=-1):
    ext = ctx.obj.settings.suffixes.simplesummary
    path = mtg.as_file(prefix=ctx.obj.path).with_suffix(ext)

    try:
        with path.open("r", encoding="utf-8") as f:
            md = f.read()
    except FileNotFoundError:
        return False

    if not diff_summaryfile(ctx.obj, mtg):
        return False

    ctx.invoke(hugo.touch_meeting, mtg=mtg, body=md, weight=weight, from_nb=False)

    return True


def diff_summaryfile(cfg: Config, mtg: Meeting) -> None:
    tmpl = j2env.get_template("summaryfile.md.j2").render(meeting=mtg)

    try:
        ext = cfg.settings.suffixes.simplesummary
        path = mtg.as_file().with_suffix(ext)
        with path.open("r", encoding="utf-8") as f:
            disk = f.read()
    except FileNotFoundError:
        return True

    tmpl_sha = sha256(tmpl.encode("utf-8")).hexdigest()
    disk_sha = sha256(disk.encode("utf-8")).hexdigest()

    return tmpl_sha != disk_sha


@cli.command()
@click.pass_context
def cleanup(ctx: Context, mtg: Meeting) -> None:
    """Delete empty Markdown files associated with .Meeting.

    :param ctx: .Context
    :param mtg: .Meeting

    :rtype None
    """
    if diff_summaryfile(ctx.obj, mtg):
        ext = ctx.obj.settings.suffixes.simplesummary
        mtg.as_file().with_suffix(ext).unlink(missing_ok=True)
