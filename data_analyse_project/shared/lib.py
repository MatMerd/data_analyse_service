import collections.abc as collections_abc
import re
from collections.abc import Iterable
from typing import Any, TypeGuard


def is_non_string_iterable(obj: Any) -> TypeGuard[Iterable[Any]]:
    return isinstance(obj, collections_abc.Iterable) and not isinstance(obj, (str, bytes))


def to_list(x: Any, default: list[Any] | None = None) -> list[Any]:
    if x is None:
        return default  # type: ignore
    if not is_non_string_iterable(x):
        return [x]
    if isinstance(x, list):
        return x
    return list(x)
