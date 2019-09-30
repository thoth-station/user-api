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

"""Configuration of user-facing API service."""

import logging
import os
from datetime import timedelta

from jaeger_client import Config as JaegerConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

_LOGGER = logging.getLogger(__name__)


class Configuration:
    """Configuration of user-facing API service."""

    APP_SECRET_KEY = os.environ["THOTH_USER_API_APP_SECRET_KEY"]
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../openapi")
    SKOPEO_BIN_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "bin", "skopeo")
    THOTH_RESULT_API_URL = os.environ["THOTH_RESULT_API_URL"]
    THOTH_ADVISER_OUTPUT = THOTH_RESULT_API_URL + "/api/v1/adviser-result"
    THOTH_ANALYZER_OUTPUT = THOTH_RESULT_API_URL + "/api/v1/analysis-result"
    THOTH_BUILDLOG_ANALYZER_OUTPUT = THOTH_RESULT_API_URL + "/api/v1/buildlogs-analysis-result"
    THOTH_PROVENANCE_CHECKER_OUTPUT = THOTH_RESULT_API_URL + "/api/v1/provenance-checker-result"
    THOTH_MIDDLETIER_NAMESPACE = os.environ["THOTH_MIDDLETIER_NAMESPACE"]
    THOTH_BACKEND_NAMESPACE = os.environ["THOTH_BACKEND_NAMESPACE"]
    # Give cache 3 hours by default.
    THOTH_CACHE_EXPIRATION = int(os.getenv("THOTH_CACHE_EXPIRATION", timedelta(hours=3).total_seconds()))

    JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")

    OPENAPI_PORT = 8080
    GRPC_PORT = 8443

    tracer = None


def init_jaeger_tracer(service_name):
    """Create a Jaeger/OpenTracing configuration."""
    config = JaegerConfig(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "local_agent": {"reporting_host": Configuration.JAEGER_HOST},
        },
        service_name=service_name,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(namespace=service_name),
    )

    return config.initialize_tracer()
