import typing

T = typing.TypeVar("T")


def not_none(value: typing.Optional[T], default: T = ...) -> T:
    ...
