"""Solutionbooks are the bread-and-butter of AI@UCF. These Notebooks are used
in all variety of tutorials and can be rendered as:
* Workbooks, to enable interactive tutorial/self-study sessions.
* Markdown Posts, to enable publication on the club website.

Currently, the following can be invoked:
* :meth:`.standardize`
* :meth:`.to_post`
* :meth:`.to_workbook`
"""
import json
from typing import Union
from pathlib import Path

import click
from click import Context
import nbformat as nbf
from jinja2 import Template
from nbconvert.exporters import MarkdownExporter, NotebookExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from nbgrader.preprocessors import ClearOutput, ClearSolutions

from seminar.utils import j2env, search
from seminar.models import Meeting
from seminar.apis import hugo


@click.group(
    name="notebook", help="Strictly interacts with a Meeting's Jupyter Notebooks."
)
@click.option("-n", "--name", "query")
@click.pass_context
def cli(ctx, query: str = ""):
    search.for_meeting(ctx.obj, query)
    pass


def _default_notebook(ctx: Context, mtg: Meeting) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()

    # Inject Heading
    html_header = j2env.get_template("notebooks/header.html.j2")
    banner_url = Template(ctx.obj.settings.hugo.banner_url).render(
        group=ctx.obj.group, meeting=mtg
    )
    header = html_header.render(banner_url=banner_url, meeting=mtg, group=ctx.obj.group)
    header_metadata = {"title": mtg.title, "tags": ["nb-title", "template"]}
    nb.cells.insert(0, nbf.v4.new_markdown_cell(header, metadata=header_metadata))

    # Inject data-loading cell
    from seminar.apis import kaggle

    py_dataset_path = j2env.get_template("notebooks/data-pathing.py.j2")
    dataset = py_dataset_path.render(slug=kaggle.slug_competition(ctx.obj, mtg))
    dataset_metadata = {"language": "python", "tags": ["template"]}
    nb.cells.insert(1, nbf.v4.new_code_cell(dataset, metadata=dataset_metadata))

    # Inject Notebook Metadata
    nb_metadata = j2env.get_template("notebooks/nb-metadata.json.j2")
    metadata = nb_metadata.render(meeting=mtg, group=ctx.obj.group)
    nb.metadata.update(json.loads(metadata))

    return nb


def _read_solutionbook(mtg: Meeting, path: Path) -> nbf.NotebookNode:
    standard = NotebookExporter()
    standard.register_preprocessor(
        TagRemovePreprocessor(remove_cell_tags=["template"]), enabled=True
    )

    nb, _ = standard.from_filename(str(path))
    nb = nbf.reads(nb, as_version=4)

    return nb


@cli.command()
@click.pass_context
def make_solutionbook(ctx, mtg: Meeting):
    """Ensures that all Solutionbooks have accurate headings, pathing, and metadata."""
    _solnbook = ctx.obj.settings.suffixes.solutionbook
    path = mtg.as_file(prefix=ctx.obj.path).with_suffix(_solnbook)

    base_nb = _default_notebook(ctx, mtg)

    # If the notebook doesn't exist, or it's empty
    if not path.exists() or path.stat().st_size == 0:
        nbf.write(base_nb, open(path, "w"))

    read_nb = _read_solutionbook(mtg, path)

    read_nb.cells = base_nb.cells + read_nb.cells[len(base_nb.cells) :]
    read_nb.metadata.merge(base_nb.metadata)

    nbf.write(read_nb, path.open("w"))


@cli.command()
@click.pass_context
def make_workbook(ctx, mtg: Meeting) -> None:
    """Generates a Workbook from a Solutionbook.

    Workbooks are stripped down Solutionbooks that, namely:
    - Have no output cells.
    - Replace `### BEGIN SOLUTION ... ### END SOLUTION` blocks with
      `raise NotImplementedError()` snippets for viewers to practice on.
    """
    path = mtg.as_file()
    _workbook = path.with_suffix(ctx.obj.settings.suffixes.workbook)
    _solnbook = path.with_suffix(ctx.obj.settings.suffixes.solutionbook)

    workbook = NotebookExporter()

    preprocessors = [ClearOutput(), ClearSolutions(enforce_metadata=False)]
    for preprocessor in preprocessors:
        workbook.register_preprocessor(preprocessor, enabled=True)
    # TODO migrate back to `enforce_metadata=True`

    # workbook.register_preprocessor(ValidateNBGrader(), enabled=True)
    # this is only useful if we can migrate back to `enforce_metadata=True`

    try:
        nb, _ = workbook.from_filename(str(_solnbook))
        nb = nbf.reads(nb, as_version=4)

        nbf.write(nb, _workbook.open("w", encoding="utf-8"))
    except Exception:
        raise Exception(f"Workbook export failed on `{mtg}`.")


@cli.command()
@click.pass_context
def make_post(ctx: Context, mtg: Meeting, weight: int = -1) -> None:
    """Preprocess a Solutionbook and prepare it to post on https://ucfai.org/."""
    cfg = ctx.obj

    _solnbook = cfg.settings.suffixes.solutionbook
    path = mtg.as_file(prefix=cfg.path).with_suffix(_solnbook)

    as_post = MarkdownExporter()
    as_post.extra_loaders = [j2env.loader]
    as_post.template_file = "notebooks/to-post.md.j2"
    as_post.no_prompt = True
    as_post.register_preprocessor(
        TagRemovePreprocessor(remove_cell_tags=["nb-title"], enabled=True)
    )

    # Default to `git`-based "Last modified..."
    # lastmod = pd.Timestamp(name.stat().st_mtime, unit="s")
    # setattr(m, "lastmod", lastmod)

    try:
        nb, _ = as_post.from_filename(str(path))
    except FileNotFoundError:
        return False

    if not diff_notebook(ctx, mtg):
        return False

    ctx.invoke(hugo.touch_meeting, mtg=mtg, body=nb, weight=weight, from_nb=True)

    return True


def diff_notebook(ctx: Context, mtg: Meeting) -> bool:
    tmpl = _default_notebook(ctx, mtg)

    standard = NotebookExporter()
    disk = mtg.as_file().with_suffix(ctx.obj.settings.suffixes.solutionbook)
    disk, _ = standard.from_filename(str(disk))
    disk = nbf.reads(disk, as_version=4)

    return tmpl != disk


@cli.command()
@click.pass_context
def kaggle_metadata(ctx: Context, mtg: Meeting):
    if not diff_notebook(ctx, mtg):
        return

    from seminar.apis import kaggle

    ctx.invoke(kaggle.kernel_metadata, mtg=mtg)


@cli.command()
@click.pass_context
def push_kaggle(ctx: Context, mtg: Meeting):
    """TODO docstring"""
    if not diff_notebook(ctx, mtg):
        return

    from seminar.apis import kaggle

    ctx.invoke(kaggle.push_kernel, mtg=mtg)


@click.command()
@click.pass_context
def cleanup(ctx: Context, mtg: Meeting) -> None:
    tmpl = _default_notebook(ctx, mtg)
    disk = mtg.as_file()
    soln = disk.with_suffix(ctx.obj.settings.suffixes.solutionbook)
    work = disk.with_suffix(ctx.obj.settings.suffixes.workbook)
    kern = disk.with_name("kernel-metadata.json")

    try:
        disk = _read_solutionbook(mtg, soln)
    except (FileNotFoundError, nbf.NBFormatError):
        return

    rm = False
    rm = len(disk.cells) == 0 or tmpl.cells == disk.cells

    if rm:
        soln.unlink()
        work.unlink(missing_ok=True)
        kern.unlink(missing_ok=True)
