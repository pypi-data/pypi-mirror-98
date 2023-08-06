""" TODO docstring """
from pathlib import Path

import pandas as pd
import requests

from ruamel.yaml import YAML

_yaml = YAML()
_config = Path(__file__).parent.parent.parent / "config.yml"
_config = _yaml.load(_config.open("r", encoding="utf-8"))
del _yaml


def make_schedule(group, delta: int = 7, new_semester: bool = False):
    if not new_semester and group.startdate.time().hour == 0:
        raise ValueError("Please set a time for the meetings.")

    calendar, holidays = parse_calendar(group.semester)
    dates = [group.startdate]
    while dates[-1] < calendar.iloc[-1]:
        dates.append(dates[-1] + pd.Timedelta(days=delta))

    # Removes Holidays, if the array is non-empty.
    holidays = list(map(lambda x: x.date(), holidays))
    meeting_dates = list(filter(lambda x: x.date() not in holidays, dates))

    schedule = [pd.Timestamp(x) for x in meeting_dates]

    return schedule


def parse_calendar(semester: str) -> tuple:
    from jinja2 import Template

    calendar_url = Template(_config["calendar"]["format"])
    calendar_base_url = _config["calendar"]["url"]

    semesters = _config["semesters"]

    lookup = {v["short"]: k for k, v in semesters.items()}
    lookup_sm = lookup[semester[:2]]
    lookup_yr = 2000 + int(semester[-2:])
    semester = semesters[lookup_sm]

    # This is the URL for the calendar's JSON-based API. This will vary by institution.
    calendar_url = "http://" + calendar_url.render(
        url=calendar_base_url, year=lookup_yr, longname=lookup_sm
    )
    url = str(requests.get(calendar_url).url)
    url = url.replace(calendar_base_url, f"{calendar_base_url}/json")

    # UCF's JSON object holds all the "events" in an "events" identifier
    ucf_parsed = requests.get(url).json()["terms"][0]["events"]
    df_calendar = pd.DataFrame.from_dict(ucf_parsed)

    # The "summary" column of the new DataFrame holds the names of the events
    summary_mask = df_calendar["summary"]
    # Events are stored as arrays. It's easier to parse this way than reducing
    #   the list-containing column to something that isn't.
    starts = df_calendar.loc[summary_mask.str.contains("Classes Begin")].iloc[0]
    ends = df_calendar.loc[summary_mask.str.contains("Classes End")].iloc[0]

    # generate a DataFrame with all possible dates (to act like a calendar)
    calendar = pd.Series(
        pd.date_range(start=starts["dtstart"][:-1], end=ends["dtstart"][:-1])
    )

    # Remove the Holidays, since we assume students won't meet on those days.
    holidays = []
    for holiday in semester["holidays"]:
        lookup = df_calendar.loc[summary_mask.str.contains(holiday)]
        for _, day2rm in lookup.iterrows():
            beg = day2rm["dtstart"][:-1]
            end = day2rm["dtend"][:-1] if day2rm["dtend"] else beg
            holidays.append(pd.Series(pd.date_range(start=beg, end=end)))

    holidays = pd.concat(holidays).reset_index(drop=True)

    return calendar, holidays
