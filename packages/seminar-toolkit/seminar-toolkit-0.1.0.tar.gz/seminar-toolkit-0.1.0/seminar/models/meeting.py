"""TODO docstring."""
from pathlib import Path
from typing import List, Union, Dict, Optional
from uuid import UUID, uuid4
import re

import pandas as pd
from pydantic import (
    BaseModel,
    Field,
    AnyHttpUrl,
    validator,
)

from seminar.models import helpers


class _OptionalURLs(BaseModel):
    slides: Optional[str] = ""
    video: Optional[str] = ""

    class Config:
        alias_generator = helpers.dashify

    @validator("slides")
    def validate_slides(cls, url: str) -> str:
        if "docs" in url and "presentation" in url:
            docs_base_url = "(?:https?://)?docs.google.com/presentation/d/e/"

            url = re.sub(f"{docs_base_url}|$", "", url)
            url = url.split("/", maxsplit=1)[0]

        test_urls = [
            "https://docs.google.com/presentation/d/e/{{ slug }}/embed",
            "https://ucfai.org/slides/{{ slug }}",
        ]

        return helpers.test_url(url, test_urls)

    @validator("video")
    def validate_videos(cls, url: str) -> str:
        if "youtu" in url:
            scheme = "(:?https?://)?"
            ln_old = "(?:www\.)?youtube.com/watch?v="
            ln_new = "youtu.be/"
            yt_full = f"{scheme}(?:{ln_old}|{ln_new})"
            url = re.sub(f"{yt_full}|$", "", url)
            url = re.search("([A-Za-z0-9-_]{9,11})", url).group(0)

        test_urls = [
            "https://youtube.com/embed/{{ slug }}",
        ]

        return helpers.test_url(url, test_urls)


class _OptionalKaggle(BaseModel):
    kernels: Union[List[str], bool] = []
    datasets: Union[List[str], bool] = []
    competitions: Union[List[str], bool] = []
    enable_gpu: bool = False

    class Config:
        alias_generator = helpers.dashify

    @validator("kernels", "datasets", each_item=True)
    def is_kaggle_slug_valid(cls, slug: str) -> str:
        try:
            assert slug.count("/") == 1
        except AssertionError:
            raise ValueError(f"Invalid slug: {slug}. Check the Kaggle API.")
        finally:
            return slug

    @validator("kernels", "datasets", "competitions", each_item=True)
    def is_kaggle_slug_live(cls, slug):
        test_urls = ["https://kaggle.com", "https://kaggle.com/c"]
        # kernel-metadata.json only accepts slugs. No error means it's live.
        _ = helpers.test_url(slug, test_urls)
        return slug


class Meeting(BaseModel):
    id: Union[str, UUID] = Field(default_factory=uuid4)
    title: str
    filename: str
    date: pd.Timestamp
    authors: List[str] = []
    cover_image: Union[str, AnyHttpUrl] = ""
    tags: List = []
    room: str = ""
    abstract: str = ""

    urls: Optional[_OptionalURLs] = {}
    kaggle: Optional[Union[_OptionalKaggle, bool]] = {}
    papers: Optional[Dict[str, AnyHttpUrl]] = {}

    class Config:
        alias_generator = helpers.dashify

    _normalize_filename = validator("filename")(helpers.downcase_dashify_name)

    @validator("papers")
    def normalize_paperkey(cls, papers) -> Dict:
        if papers is None:
            return None

        assert type(papers) == dict

        cleaned = {}
        for key, url in papers.items():
            normed = helpers.downcase_dashify_name(key)
            url = helpers.test_url(url)
            cleaned[normed] = url

        return cleaned

    def __repr__(self):
        s = self.filename

        if not pd.isnull(self.date):
            return f"{self.date.isoformat()[5:10]}-{s}"

        return s

    def __str__(self):
        return repr(self)

    def as_dir(self, prefix: Path = None):
        """Returns a ``Path`` of a ``Meeting`` as a directory.

        (normally used to place contents, e.g. Notebooks, Markdown, data, PDFs, etc.)
        """
        folder = Path(repr(self))
        if prefix:
            return prefix / folder
        return folder

    def as_file(self, prefix: Path = None, suffix: str = ""):
        """Returns ``Path`` of a ``Meeting`` as a file.

        (normally used for Notebook and Markdown files)
        """
        file: Path = self.as_dir(prefix) / self.filename
        if suffix:
            return file.with_suffix(suffix)
        return file
