#!/usr/bin/env python3
# Stub
# Copyright(C) 2019 Christoph Görn
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

"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc_tools import protoc

protoc.main(
    ("", "-I./protobuf_spec", "--python_out=.", "--grpc_python_out=.", "./protobuf_spec/thoth/user_api/user_api.proto")
)
