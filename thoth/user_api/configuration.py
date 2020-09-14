#!/usr/bin/env python3
# thoth-user-api
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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

"""Configuration of user-facing API service."""

import logging
import os
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)


class Configuration:
    """Configuration of user-facing API service."""

    APP_SECRET_KEY = os.environ["THOTH_USER_API_APP_SECRET_KEY"]
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../openapi")
    SKOPEO_BIN_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "bin", "skopeo")
    THOTH_MIDDLETIER_NAMESPACE = os.environ["THOTH_MIDDLETIER_NAMESPACE"]
    THOTH_BACKEND_NAMESPACE = os.environ["THOTH_BACKEND_NAMESPACE"]
    THOTH_HOST = os.environ["THOTH_HOST"]
    # Give cache 3 hours by default.
    THOTH_CACHE_EXPIRATION = int(os.getenv("THOTH_CACHE_EXPIRATION", timedelta(hours=3).total_seconds()))

    JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")

    OPENAPI_PORT = 8080
    GRPC_PORT = 8443

    tracer = None

    # Kafka Config
    KAFKA_CAFILE = os.getenv("KAFKA_CAFILE", "ca.cert")
