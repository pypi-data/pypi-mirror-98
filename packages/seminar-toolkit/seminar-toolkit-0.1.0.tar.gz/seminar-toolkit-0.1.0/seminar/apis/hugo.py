"""TODO docstring"""
import re
from functools import partial
from pathlib import Path
from typing import Dict

import docker
import click
from click import Context
from docker.models.containers import ContainerCollection
from jinja2 import Template

from seminar.models import Meeting
from seminar.utils import EditableFM, sort, requests_headers


command = Template("hugo new --kind {{ kind }} {{ path }}")


def via_docker(func):
    def hugo_via_container(ctx, *args, **kwargs):
        client = docker.from_env()

        import requests
        from requests.exceptions import RequestException

        try:
            raise RequestException
            compose_url = (
                f"{ctx.obj.settings.version_control.repo_owner}/"
                f"{ctx.obj.settings.website.repo}/raw/"
                f"{ctx.obj.settings.website.branch}/docker-compose.yml"
            )

            from ruamel.yaml import YAML

            yaml = YAML()

            compose_yml = yaml.load(
                requests.get(compose_url, headers=requests_headers).content
            )
            image = compose_yml["services"]["hugo"]["image"]
        except (RequestException, KeyError):
            image = ctx.obj.settings.website.image

        container = client.containers.create(
            image=image,
            auto_remove=False,
            detach=False,
            volumes={
                f"{ctx.obj.settings.website.site_src}": {
                    "bind": "/src",
                    "mode": "rw",
                },
            },
            working_dir="/src",
        )
        container.start()

        retval = func(ctx, *args, container=container, **kwargs)

        container.stop()
        container.remove()

        return retval

    return hugo_via_container


@via_docker
def touch_group(ctx: Context, container: ContainerCollection = None) -> None:
    """Creates a new .Group.
    Adds a `_index.md` page to create a new .Group landing page.

    :params ctx.obj: Invoke Context that should contain: .Group

    :returns: None
    """
    assert container
    group_path = f"groups/{ctx.obj.group.name}"
    new_author = command.render(
        kind="semester",
        path=group_path,
    )

    res = container.exec_run(new_author)
    output = res.output.decode("utf-8")

    # editor = EditableFM(f"{site_src}/content/{group_path}")
    # editor.load("_index.md")

    # NOTE Any programmatic edits to the Group should be made here

    # editor.dump()


@via_docker
def touch_semester(ctx: Context, container: ContainerCollection = None) -> None:
    """Creates a new semester for a given .ctx.obj.group.
    Adds a new `_index.md` page for display on the .Group landing page.

    :params ctx.obj: Invoke Context that should contain: .Group

    :returns: None
    """
    assert container

    group_path = f"groups/{ctx.obj.group.name}/{ctx.obj.group.semester}"
    new_semester = command.render(
        kind="semester",
        path=group_path,
    )

    expanded_path = f"{ctx.obj.settings.website.site_src}/content/{group_path}"
    Path(expanded_path).mkdir(exist_ok=True)

    res = container.exec_run(new_semester)
    output = res.output.decode("utf-8")

    editor = EditableFM(expanded_path)
    editor.load("_index.md")

    editor.fm["date"] = str(ctx.obj.group.startdate)
    editor.fm["location"] = ctx.obj.group.room
    editor.fm["abstract"] = ctx.obj.group.abstract

    editor.dump()


@via_docker
def touch_author(
    ctx: Context, author: str = "", container: ContainerCollection = None
) -> None:
    """Creates an author page everyone that contributes to a semester's content.

    :params ctx: click.Context that should contain: .Group

    :returns: None
    """
    assert container

    author_path = f"authors/{author}/"
    new_author = command.render(
        kind="author",
        path=author_path,
    )

    res = container.exec_run(new_author)
    output = res.output.decode("utf-8")

    editor = EditableFM(f"{ctx.obj.settings.website.site_src}/content/{author_path}")
    editor.load("_index.md")

    groups = []
    for role in ctx.obj.settings.website.config.bot_taggable_roles:
        if author in map(str.lower, getattr(ctx.obj.group, f"{role.lower()}s")):
            groups = list(map(Template, ctx.obj.settings.website.roles))
            groups = [g.render(group=ctx.obj.group, role=role) for g in groups]
            break

    try:
        roles = [groups[-1]]
    except IndexError:
        roles = []

    editor.fm = _sort_and_update_metadata(
        ctx,
        editor.fm,
        editor.fm["user_groups"] + groups,
        editor.fm["teams"],
        editor.fm["roles"] + roles,
    )

    editor.dump()


@via_docker
def touch_post(
    ctx: Context,
    mtg: Meeting,
    weight: int = -1,
    container: ContainerCollection = None,
) -> EditableFM:
    """Renders Jupyter Notebook to ctx.obj.settings["hugo"]-ready Markdown.

    :params ctx.obj: Invoke Context that should contain: [.Group, .Syllabus]

    :returns: None
    """
    assert container

    meeting_path = f"groups/{ctx.obj.group.name}/{ctx.obj.semester}"
    meeting_file = f"{mtg.filename}.md"
    new_meeting_post = command.render(
        kind="group-meeting", path=f"{meeting_path}/{meeting_file}"
    )
    res = container.exec_run(new_meeting_post)
    output = res.output.decode("utf-8")

    editor = EditableFM(ctx.obj.settings.website.site_src / "content" / meeting_path)
    editor.load(meeting_file)

    return editor


@click.pass_context
def touch_meeting(
    ctx: Context, mtg: Meeting, body: str, weight: int, from_nb: bool = False
) -> None:
    editor = touch_post(ctx, mtg)

    editor.fm["title"] = mtg.title
    editor.fm["linktitle"] = mtg.title

    editor.fm["date"] = mtg.date.isoformat()
    # ctx.settings.hugo ordering prefers 1-based indexing
    if weight > -1:
        editor.fm["weight"] = weight + 1

    editor.fm["authors"] = mtg.authors

    editor.fm["urls"] = {}

    try:
        editor.fm["urls"]["video"] = mtg.urls.video
    except AttributeError:
        pass

    try:
        editor.fm["urls"]["slides"] = mtg.urls.slides
    except AttributeError:
        pass

    if from_nb:
        from seminar.apis import kaggle

        soln = ctx.obj.settings.suffixes.solutionbook
        work = ctx.obj.settings.suffixes.workbook

        editor.fm["urls"]["github"] = str(mtg.as_file().with_suffix(soln))
        editor.fm["urls"]["kaggle"] = str(kaggle.slug_kernel(ctx.obj, mtg))
        editor.fm["urls"]["colab"] = str(mtg.as_file().with_suffix(work))

    editor.fm["location"] = mtg.room
    # editor.fm["cover"] = m.cover_image

    editor.fm["tags"] = mtg.tags
    editor.fm["abstract"] = mtg.abstract

    try:
        editor.fm["papers"] = {
            key: str(mtg.as_dir() / f"{key}.pdf") for key in mtg.papers.keys()
        }
    except (AttributeError):
        pass

    try:
        editor.content = ["\n", body]
    except NameError:
        pass

    editor.dump()


@click.pass_context
def cleanup_authors(ctx: Context) -> None:
    authors = Path(ctx.obj.settings.website.site_src) / "content/authors"

    for author in filter(Path.is_dir, authors.iterdir()):
        editor = EditableFM(author)
        editor.load("_index.md")

        author = author.stem
        author_groups = set(editor.fm["user_groups"])
        author_roles = set(editor.fm["roles"])
        author_teams = set(editor.fm["teams"])

        for role in ctx.obj.settings.website.config.bot_taggable_roles:
            role_group = map(str.lower, getattr(ctx.obj.group, f"{role.lower()}s"))
            if author not in list(role_group):
                roles = [Template(r) for r in ctx.obj.settings.website.roles]
                roles = [r.render(group=ctx.obj.group, role=role) for r in roles]
                roles = set(filter(lambda x: role.lower() in x, roles))
                author_groups -= roles

        rm_roles = []
        for role in author_roles:
            has_role = list(filter(lambda x: x.endswith(role.lower()), author_groups))
            if not has_role:
                rm_roles.append(role)

        author_roles -= set(rm_roles)

        rm_teams = []
        for team in author_teams:
            on_team = list(filter(lambda x: x.startswith(team.lower()), author_groups))
            if not on_team:
                rm_teams.append(team)

        author_roles -= set(rm_teams)

        editor.fm = _sort_and_update_metadata(
            ctx, editor.fm, author_groups, author_teams, author_roles
        )

        editor.dump()


def _sort_and_update_metadata(
    ctx: Context, fm: dict, user_groups: list, teams: list, roles: list
) -> Dict:
    # region Semi-Complex Group filtering/sorting
    groups = set(user_groups)

    sorter = partial(sort.by_roles, ctx.obj.settings.website.config.officers)

    non_sem = filter(lambda x: not re.match(r"(fa|sp|su)\d{2}", x), groups)
    non_sem_groups = sorted(list(non_sem))

    isa_sem = filter(lambda x: bool(re.match(r"(fa|sp|su)\d{2}", x)), groups)
    isa_sem_groups = sorted(list(isa_sem), key=sorter, reverse=True)

    fm["user_groups"] = non_sem_groups + isa_sem_groups
    # endregion

    # region Sort "teams" (semesterly activity)
    teams = list(set(teams))
    teams = sorted(teams, key=sort.by_semester, reverse=True)
    fm["teams"] = teams
    # endregion

    # region Sort "roles" alphabetically
    roles = sorted(list(set(roles)))
    fm["roles"] = roles
    # endregion

    return fm
