"""TODO doctstring."""
from typing import List
from pathlib import Path

import requests
import pandas as pd
from pydantic import (
    BaseModel,
    Field,
    root_validator,
)

from seminar.models import helpers


def _load_config() -> dict:
    from ruamel.yaml import YAML

    yaml = YAML()
    config = Path(__file__).parent.parent.parent / "config.yml"
    config = dict(yaml.load(config.open("r", encoding="utf-8")))
    return config


def infer_current_semester() -> str:
    config = _load_config()

    calendar_url = config["calendar"]["url"]
    url = requests.get(f"http://{calendar_url}/").url

    year, semester = url.split(f"{calendar_url}/")[-1].split("/")

    year = str(year)[-2:]
    sem = config["semesters"][semester]["short"]

    return f"{sem}{year}"


def infer_next_semester() -> str:
    """Infers the current semester based on today's date.

    Takes advantage of the redirection https://ucf.calendar.edu/ has built-in.
    """
    semester = infer_current_semester()

    semester, year = semester[:2], semester[-2:]

    config = _load_config()
    semesters = config["semesters"]

    semester = next(filter(lambda x: x.startswith(semester), semesters.keys()))

    if semester == "fall":
        year = f"{int(year) + 1}"

    sem = semesters[semester]["next"]
    sem = semesters[sem]["short"]

    return f"{sem}{year}"


def infer_startdate(semester: str = infer_next_semester()) -> pd.Timestamp:
    from seminar.utils.ucfcal import parse_calendar

    calendar, _ = parse_calendar(semester)
    return calendar[0] + pd.Timedelta(days=7)


class Group(BaseModel):
    name: str
    room: str = ""

    semester: str = Field(default_factory=infer_next_semester)
    startdate: pd.Timestamp = Field(default_factory=infer_startdate)

    directors: List[str] = []
    coordinators: List[str] = []
    guests: List[str] = []
    advisors: List[str] = []

    abstract: str = ""

    class Config:
        alias_generator = helpers.dashify

    @root_validator
    def _check_semester_and_startdate_match(cls, values):
        semester, startdate = values.get("semester"), values.get("startdate")
        if semester is None or startdate is None:
            raise ValueError(
                f"`semester` and `startdate` must be set. Got {(semester, startdate)}"
            )
        expected_startdate = infer_startdate(semester)
        exp_yr, exp_mo, _ = str(expected_startdate.date()).split("-")

        cur_yr, cur_mo, _ = str(startdate.date()).split("-")
        cur_hr, cur_mn, _ = map(int, str(startdate.time()).split(":"))

        # Check that we're setting dates that make sense for the semester; but also
        #   avoid overwriting manually set dates by checking the time.
        if (cur_hr == 0) and (exp_yr != cur_yr or exp_mo != cur_mo):
            values["startdate"] = expected_startdate

        return values

    def __str__(self) -> str:
        return self.name

    @property
    def authors(self) -> set:
        return set(self.directors + self.coordinators + self.guests + self.advisors)
