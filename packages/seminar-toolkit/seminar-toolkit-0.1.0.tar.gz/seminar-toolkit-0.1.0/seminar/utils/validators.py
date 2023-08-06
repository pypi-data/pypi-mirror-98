from typing import Union

from seminar.models import Meeting


def search(ctx, query: Union[str, Meeting] = None) -> Union[list, Meeting]:
    # NOTE solution at https://stackoverflow.com/a/36438326/2714651
    # @functools.wraps(func)
    # def wrapper(ctx, *args, **kwargs):
    if not query:
        return ctx.syllabus
    elif isinstance(query, Meeting):
        return query
    elif type(query) == str:
        is_substr = lambda x: query.lower() in x.filename.lower()
        bytitle = filter(is_substr, ctx.syllabus)
        try:
            return next(bytitle)
        except StopIteration:
            mtg_ls = "\n- ".join(ctx.syllabus)
            raise ValueError(
                f"Failed to find a `Meeting` containing `{query}`. "
                f"Here's a current list of meetings:{mtg_ls}"
            )
    else:
        raise ValueError("`query` must be of type: {`str`, `Meeting`}.")
