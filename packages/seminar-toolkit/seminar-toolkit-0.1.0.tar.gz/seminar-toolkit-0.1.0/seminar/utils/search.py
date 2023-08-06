"""TODO docstring
"""
from typing import Union

from click import Context

from seminar.utils import Config
from seminar.models import Meeting


def for_meeting(cfg: Config, value: Union[str, Meeting]) -> Meeting:
    """Searches for the nearest matching meeting.

    :param cfg: Config
    :param query: Union[str, Meeting]
    """
    # NOTE solution at https://stackoverflow.com/a/36438326/2714651
    if not value:
        cfg.meetings = cfg.syllabus
    elif isinstance(value, Meeting):
        cfg.meetings = [value]
    elif type(value) == str:

        def is_substr(m: Meeting):
            return value.lower() in m.filename.lower()

        try:
            bytitle = filter(is_substr, cfg.syllabus)
            cfg.meetings = [next(bytitle)]
        except StopIteration:
            mtg_ls = "\n- ".join(cfg.syllabus)
            raise ValueError(
                f"Failed to find a `Meeting` containing `{value}`. "
                f"Here's a current list of meetings:{mtg_ls}"
            )
    else:
        raise ValueError("`query` must be a `str` or `Meeting`.")

    cfg.query = cfg.meetings[0]

    return value
