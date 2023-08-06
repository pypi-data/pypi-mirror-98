"""TODO docstring"""
from .group import Group
from .meeting import Meeting

__all__ = [
    # "Syllabus",
    "Group",
    "Meeting",
]


def _inline_list(ls):
    from ruamel.yaml.comments import CommentedSeq
    from ruamel.yaml.scalarstring import DoubleQuotedScalarString

    ls = CommentedSeq(ls)
    for idx, item in enumerate(ls):
        if type(item) == str:
            ls[idx] = DoubleQuotedScalarString(item)
    ls.fa.set_flow_style()
    return ls


def _transform(v):
    if type(v) == list:
        pass
        # v = _inline_list(v)
    elif type(v) == dict:
        for key in v.keys():
            v[key] = _transform(v[key])
    elif type(v) == str:
        from ruamel.yaml.scalarstring import DoubleQuotedScalarString

        v = DoubleQuotedScalarString(v)

    return v


def to_yaml(model, path):
    """Handles dumping `group.yml` and `syllabus.yml` to files."""
    import json

    from ruamel.yaml import YAML
    from ruamel.yaml.comments import CommentedMap
    from ruamel.yaml.representer import FoldedScalarString

    yaml = YAML()
    yaml.width = 78
    yaml.preserve_quotes = True

    if type(model) != list:
        model = [model]

    model_cm = []
    for idx, part in enumerate(model):
        part = CommentedMap(json.loads(part.json()))
        part.yaml_set_start_comment("Check the Docs for details on editing this!")

        try:
            abstract = part["abstract"] or "We're filling this out!"
            part["abstract"] = FoldedScalarString(abstract)
        except KeyError:
            pass

        for key in part.keys():
            part[key] = _transform(part[key])

        model_cm.append(part)

    if len(model) == 1 and not isinstance(model[0], Meeting):
        model_cm = model_cm[0]

    yaml.dump(model_cm, path.open("w", encoding="utf-8"))
