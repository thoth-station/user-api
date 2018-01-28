"""A base class for implementing extraction handlers."""

import abc
import typing

import attr

_HandlerBaseType = typing.TypeVar('T', bound='Repository')  # pylint: disable=invalid-name


@attr.s
class HandlerBase(object):
    """Handle extracting packages from build logs."""

    handlers: typing.ClassVar[typing.List[_HandlerBaseType]] = []

    @classmethod
    def register(cls, handler_instance: _HandlerBaseType) -> None:
        """Register a handler instance to be used."""
        cls.handlers.append(handler_instance)

    @classmethod
    def get_handler_names(cls) -> typing.List[str]:
        """Get names of all registered handlers."""
        return [handler.__name__ for handler in cls.handlers]

    @classmethod
    def instantiate_handlers(cls) -> typing.Generator[_HandlerBaseType, None, None]:
        """Instantiate handlers with corresponding arguments."""
        for handler in cls.handlers:
            yield handler()

    @abc.abstractmethod
    def run(self, input_text: str) -> dict:
        """Find and parse installed packages and their versions from a build log."""
        raise NotImplementedError
