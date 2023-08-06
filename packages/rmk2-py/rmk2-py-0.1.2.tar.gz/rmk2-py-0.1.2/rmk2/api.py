import functools
import json
import os
import re
from typing import Any, Dict, Iterator, Optional, Sequence, Union
from urllib.parse import urlparse, urlunparse
from uuid import uuid4


def save_response(prefix: str = None) -> callable:
    """Wrapper to save the return value of a function to JSON"""

    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            response = func(*args, **kwargs)

            _filename = os.path.join(
                os.path.dirname(__file__),
                prefix,
                f"{func.__name__}_{str(uuid4())}.json",
            )

            with open(_filename, mode="w", encoding="utf-8") as outfile:
                _response = (
                    list(response) if isinstance(response, Iterator) else response
                )

                json.dump(_response, outfile)

            return _response

        return wrapper

    return decorator


def _create_url(
    base_url: str,
    path: Optional[Sequence[str]],
    query: Optional[Dict[str, Union[str, int]]],
) -> str:
    """Helper function to create valid URLs by extending a base URL"""
    _scheme, _netloc, _path, _, _query, _ = urlparse(base_url)

    _path = (
        "/".join([re.sub(r"/$", "", _path), *[str(x) for x in path]])
        if path is not None
        else _path
    )
    _query = (
        "&".join([f"{k}={str(v)}" for k, v in query.items()])
        if query is not None
        else {}
    )

    return urlunparse((_scheme, _netloc, _path, None, _query, None))
