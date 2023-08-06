from typing import (

    overload,
    TypeVar,
    Optional,
    Iterable
)


T = TypeVar("T")


@overload
def one(v: Iterable[T]) -> Optional[T]: ...


@overload
def one(v: T) -> T: ...
