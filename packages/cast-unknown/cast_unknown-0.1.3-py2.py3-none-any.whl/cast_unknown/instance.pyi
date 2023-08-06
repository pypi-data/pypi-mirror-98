import typing

T = typing.TypeVar("T")


def instance(
        object: typing.Any,
        class_or_tuple: typing.Union[
            typing.Type[T],
            typing.Tuple[typing.Type[T], ...],
        ],
        /,
) -> T:
    ...
