from typing import Any, Optional

from yarl import URL


def get_url(*args, **kwargs) -> str:
    # Create a URL object from args[0]
    url_obj = URL(args[0])

    # Add path segments from args[1:]
    for arg in args[1:]:
        if arg:
            url_obj = url_obj / arg

    # Add parameters
    filter_ = kwargs.get("filter_")
    if filter_:
        url_obj = str(url_obj) + filter_

    return str(url_obj)


def get_endpoint(*args: Any) -> str:
    return "/".join(str(arg).strip("/") for arg in args if arg is not None)
