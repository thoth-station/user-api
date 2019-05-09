#!/usr/bin/env python3
# User API gRPC server
# Copyright(C) 2019 Christoph Görn, Fridolin Pokorny
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

"""Thoth User API gRPC server."""

import os

from concurrent import futures
import time
import logging

import grpc

from grpc_opentracing import open_tracing_server_interceptor
from grpc_opentracing.grpcext import intercept_server

from thoth.common import init_logging

from thoth.user_api import __version__
from thoth.user_api.configuration import Configuration
from thoth.user_api.configuration import init_jaeger_tracer

import thoth.user_api.api_v1 as api
import thoth.user_api.user_api_pb2 as user_api_pb2
import thoth.user_api.user_api_pb2_grpc as user_api_pb2_grpc


# Configure global application logging using Thoth's init_logging.
init_logging(logging_env_var_start="THOTH_USER_API_LOG_")

_LOGGER = logging.getLogger("thoth.user_api")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("THOTH_USER_API_DEBUG", 0))) else logging.INFO)

_LOGGER.info(f"This is User API gRPC server v{__version__}")
_LOGGER.debug("DEBUG mode is enabled!")


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UserApiServicer(user_api_pb2_grpc.StubServicer):
    """Provides methods that implement functionality of the User API gRPC server."""

    def __init__(self, tracer):
        """Initialize servicer."""
        self._tracer = tracer

    def Info(self, request, context):
        """Provide info interface."""
        versions = api.info.info_response()

        with self._tracer.start_span("user_api_server_span", child_of=context.get_active_span().context):
            return user_api_pb2.InfoResponse(
                version=versions["version"],
                connexionVersion=versions["connexionVersion"],
                jaegerClientVersion=versions["jaegerClientVersion"],
            )


def serve():
    """Serve service via gRPC."""
    Configuration.tracer = init_jaeger_tracer("stub_api")

    # read in key and certificate
    with open("certs/tls.key", "rb") as f:
        private_key = f.read()
    with open("certs/tls.crt", "rb") as f:
        certificate_chain = f.read()

    # create server credentials
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))

    tracer_interceptor = open_tracing_server_interceptor(Configuration.tracer)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_server(server, tracer_interceptor)

    user_api_pb2_grpc.add_UserApiServicer_to_server(UserApiServicer(Configuration.tracer), server)
    server.add_secure_port(f"[::]:{Configuration.GRPC_PORT}", server_credentials)
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

    Configuration.tracer.close()


if __name__ == "__main__":
    serve()
