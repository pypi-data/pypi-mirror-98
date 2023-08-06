import json

from jinja2 import Environment, PackageLoader

j2env = Environment(
    loader=PackageLoader("seminar", "templates"),
)
j2env.filters["jsonify"] = json.dumps


requests_headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
}


from .config import Config
from . import ucfcal, sort
from .editFM import EditableFM

__all__ = [
    "ucfcal",
    "EditableFM",
]
