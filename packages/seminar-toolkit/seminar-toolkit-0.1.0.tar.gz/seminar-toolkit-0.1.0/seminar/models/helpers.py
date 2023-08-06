"""TODO docstring."""
from typing import List
import string

import requests
from requests import codes as status_codes
from jinja2 import Template

from seminar.utils import requests_headers


def dashify(string: str) -> str:
    return "-".join(string.split("_"))


def downcase_dashify_name(name: str) -> str:
    # latter bit is to keep those symbols from being stripped
    for punc in set(string.punctuation) - {
        "-",
        "_",
    }:
        name = name.replace(punc, "")

    name = name.replace(" ", "-")
    name = name.replace("_", "-")

    # partially inspired by: https://stackoverflow.com/a/40382663
    name_len = len(name)

    def is_lower_around(n: int) -> bool:
        prev_char = name[n - 1].islower()
        next_char = (n + 1) < name_len and name[n + 1].islower()
        return prev_char or next_char

    start = 0
    parts = []
    for c in range(1, name_len):
        if name[c].isupper() and is_lower_around(c):
            parts.append(name[start:c])
            start = c
    parts.append(name[start:])

    name = "-".join(parts)

    return name.lower()


def test_url(slug: str, test_urls: List[str] = [""]) -> str:
    if not slug:
        return ""

    for test in test_urls:
        url = Template(test).render(slug=slug) if test != "" else slug
        query = requests.get(url, headers=requests_headers)
        if query.status_code == status_codes.OK:
            return query.url

    raise ValueError(f"Could not find {slug} at any test URLs: {test_urls}")
