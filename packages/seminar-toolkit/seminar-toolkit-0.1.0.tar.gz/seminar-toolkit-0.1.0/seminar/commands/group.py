""" TODO docstring """
import re
import shutil
from pathlib import Path

import click
from click import Context
import pandas as pd

from seminar import models


@click.group(name="group")
@click.pass_context
def cli(ctx: Context):
    """Performs administrative tasks for a given semester in the Group."""
    pass


@cli.command()
@click.pass_context
def validate(ctx: Context):
    """Validates the Group's Syllabus is typed properly, sorted, etc."""
    ondisk = list(filter(Path.is_dir, ctx.obj.path.iterdir()))
    empty = len(ondisk) == 0

    group = ctx.obj.group

    g_timedelta = pd.Timedelta(str(group.startdate.time()))
    g_date = group.startdate
    g_weekdelta = pd.Timedelta(7)

    prev_date = g_date
    for idx, meeting in enumerate(ctx.obj.syllabus):
        if re.search(r"meeting\d\d", meeting.filename):
            continue
        if empty or meeting.room == "":
            meeting.room = ctx.obj.group.room
        if g_date.time().hour != 0 and meeting.date.time().hour == 0:
            meeting.date += g_timedelta
        if (meeting.date - prev_date) % g_weekdelta != pd.Timedelta(0):
            print(
                "Not a N-weekly gap. "
                f"The current gap for {meeting} is {(meeting.date - prev_date)}. "
                "Not a failure condition, but take note."
            )
        prev_date = meeting.date

    g_authors = set(map(str.lower, ctx.obj.group.authors))
    for meeting in ctx.obj.syllabus:
        if re.search(r"meeting\d\d", meeting.filename):
            continue
        m_authors = set(map(str.lower, meeting.authors))
        # TODO check how the authors are missing
        if not m_authors and meeting.title and meeting.filename:
            _msg = f"Meeting {meeting} has no authors."
        elif not m_authors.intersection(g_authors):
            _msg = f"Meeting {meeting} authors not in Group {ctx.obj.group} authors."
        else:
            continue
        print(_msg)

    try:
        n_mtgs = len(ctx.obj.syllabus)
        n_uniq = len({m.date for m in ctx.obj.syllabus})
        assert n_mtgs == n_uniq
    except AssertionError:
        pass

    ctx.obj.syllabus = sorted(ctx.obj.syllabus, key=lambda m: m.date)

    # region Write out validated syllabus
    syllabus_yml = ctx.obj.path / "syllabus.yml"
    models.to_yaml(ctx.obj.syllabus, syllabus_yml)
    # endregion


# @task(pre=[preprocess])
@cli.command()
@click.pass_context
def touch(ctx: Context):
    """Mimics Unix `touch` and creates/updates the Group."""
    from seminar.apis import hugo

    cfg = ctx.obj

    # region Make this semester's meeting directories
    # In the repository
    cfg.path.mkdir(exist_ok=True)
    # On the website
    hugo.touch_semester(ctx)
    # endregion

    # region Write to `group.yml`
    group_yml = cfg.path / "group.yml"
    models.to_yaml(cfg.group, group_yml)
    # endregion

    # region Write to `syllabus.yml`
    syllabus_yml = cfg.path / "syllabus.yml"
    models.to_yaml(cfg.syllabus, syllabus_yml)
    # endregion

    # region Create and/or rename the Meeting directories
    # NOTE this section strictly creates directories and renames. If you want to create
    #  actual meeting files, use `meeting.touch`.
    def getid(p):
        return str((p / ".metadata").open("r", encoding="utf-8").read())

    syllid = {str(m.id): cfg.path / str(m) for m in cfg.syllabus}
    ondisk = sorted(list(filter(Path.is_dir, cfg.path.glob("??-??-*/"))))
    ondisk = {getid(p): p for p in ondisk}

    for id, meeting in syllid.items():
        try:
            ondisk[id].rename(meeting)
        except (KeyError, FileNotFoundError):
            meeting.mkdir()
            (meeting / ".metadata").open("w", encoding="utf-8").write(str(id))
            ondisk[id] = meeting

        prv = ondisk[id].stem[6:]  # only consider filenames
        needs_rename = filter(lambda x: x.stem.startswith(prv), meeting.iterdir())

        new = meeting.stem[6:]
        for child in needs_rename:
            ext = "".join(child.suffixes)
            child.rename(child.parent / f"{new}{ext}")
    # endregion

    # region Update Author Profiles on the website
    for author in cfg.group.authors:
        hugo.touch_author(ctx, author.lower())
    # endregion


# @task(post=[touch])
@cli.command()
@click.pass_context  # needed to call `touch` after
def new_semester(ctx: Context):
    """Creates a new semester. Filters the {group}.yml context for semester creation. Calls `group.touch` post completion."""
    from seminar.models import Group, Meeting
    from seminar.utils.ucfcal import make_schedule

    assert not isinstance(ctx.obj.group, Group), "Already made a new semester."

    kwargs = {}
    kwargs["name"] = ctx.obj.group
    kwargs["semester"] = ctx.obj.semester

    group = Group(**kwargs)

    calendar = make_schedule(group, new_semester=True)
    syllabus = [
        Meeting(title=f"meeting{idx:02d}", filename=f"meeting{idx:02d}", date=date)
        for idx, date in enumerate(calendar)
    ]

    ctx.obj.group = group
    ctx.obj.semester = group.semester
    if ctx.obj.path.parts.count(ctx.obj.semester) < 1:
        ctx.obj.path /= group.semester
    ctx.obj.syllabus = syllabus

    ctx.invoke(touch)


# @task(pre=[preprocess], post=[status_dump])
# @click.command()
# def publish(ctx):
#     """Prepares "camera-ready" versions of the Group for public consumption."""
#     pass


@cli.command()
@click.pass_context
def clean(ctx: Context):
    """Cleans up excess files, roles, and the like for a Group."""
    from seminar.apis import hugo

    # region Cleanup lingering syllabus entries and directories
    for idx, meeting in enumerate(ctx.obj.syllabus):
        if not re.match(r"meeting\d\d", meeting.filename):
            continue

        del ctx.obj.syllabus[idx]

    for path in filter(Path.is_dir, ctx.obj.path.iterdir()):
        if not re.search(r"meeting\d\d", path.stem):
            continue

        shutil.rmtree(str(path))
    # endregion

    # region Cleanup unused default files (e.g. blank Notebooks, SimpleSummaries, etc.)
    # TODO cleanup blanks
    # endregion

    ctx.invoke(hugo.cleanup_authors)
