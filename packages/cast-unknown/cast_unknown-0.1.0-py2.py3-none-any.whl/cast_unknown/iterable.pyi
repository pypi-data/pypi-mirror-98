from typing import (
    TypeVar,
    overload,
    Iterable
)


T = TypeVar("T")


@overload
def iterable(v: Iterable[T]) -> Iterable[T]: ...


@overload
def iterable(v: T) -> Iterable[T]: ...
