#!/usr/bin/env python3
# thoth-user-api
# Copyright(C) 2018, 2019 Fridolin Pokorny
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

"""Exceptions raised in the whole user-api implementation."""


class UserApiException(Exception):
    """A base class for user API exceptions."""


class NotFoundException(UserApiException):
    """An exception raised if the requested resource could not be found."""


class ImageError(UserApiException):
    """An exception raised if inspection of the given image was not successful."""


class ImageManifestUnknownError(ImageError):
    """An exception raised if manifest of the given image is not known."""


class ImageAuthenticationRequired(ImageError):
    """An exception raised if there is a need to authenticate against registry to inspect the given image."""
