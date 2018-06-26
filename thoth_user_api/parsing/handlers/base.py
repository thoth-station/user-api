#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thoth-user-api
# Copyright(C) 2018 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A base class for implementing extraction handlers."""

import abc
import typing

import attr

_HandlerBaseType = typing.TypeVar('T', bound='Repository')


@attr.s
class HandlerBase(object):
    """Handle extracting packages from build logs."""

    handlers:
        # Ignore PycodestyleBear (E701)
        typing.ClassVar[typing.List[_HandlerBaseType]] = []

    @classmethod
    def register(cls, handler_instance: _HandlerBaseType) -> None:
        """Register a handler instance to be used."""
        cls.handlers.append(handler_instance)

    @classmethod
    def get_handler_names(cls) -> typing.List[str]:
        """Get names of all registered handlers."""
        return [handler.__name__ for handler in cls.handlers]

    @classmethod
    # Ignore PycodestyleBear (E501)
    def instantiate_handlers(cls) -> typing.Generator[_HandlerBaseType, None, None]:
        """Instantiate handlers with corresponding arguments."""
        for handler in cls.handlers:
            yield handler()

    @abc.abstractmethod
    def run(self, input_text: str) -> dict:
        """Extract installed packages and their versions from a build log."""
        raise NotImplementedError
