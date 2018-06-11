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

"""Configuration of user-facing API service."""

import os
import datetime


def _get_api_token():
    """Get token from service account token file."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc


class Configuration:
    """Configuration of user-facing API service."""

    APP_SECRET_KEY = os.environ['THOTH_USER_API_APP_SECRET_KEY']
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'swagger.yaml')

    KUBERNETES_API_URL = os.getenv('KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
    KUBERNETES_VERIFY_TLS = bool(int(os.getenv('KUBERNETES_VERIFY_TLS', True)))
    KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN') or _get_api_token()

    THOTH_MIDDLETIER_NAMESPACE = os.environ['THOTH_MIDDLETIER_NAMESPACE']
    THOTH_BACKEND_NAMESPACE = os.environ['THOTH_BACKEND_NAMESPACE']
    THOTH_ANALYZER_HARD_TIMEOUT = int(os.getenv('THOTH_ANALYZER_HARD_TIMEOUT',
                                                datetime.timedelta(hours=24).total_seconds()))
    THOTH_RESULT_API_URL = os.environ['THOTH_RESULT_API_URL']
    THOTH_ADVISER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/adviser-result'
    THOTH_ANALYZER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/analysis-result'
    THOTH_SOLVER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/solver-result'
    THOTH_MIDDLETIER_POD_MEMORY_LIMIT = os.getenv('THOTH_MIDDLETIER_POD_MEMORY_LIMIT', '0.5Gi')
    THOTH_MIDDLETIER_POD_CPU_LIMIT = os.getenv('THOTH_MIDDLETIER_POD_CPU_LIMIT', '0.5')
    THOTH_MIDDLETIER_POD_MEMORY_REQUEST = os.getenv('THOTH_MIDDLETIER_POD_MEMORY_REQUEST', '32Mi')
    THOTH_MIDDLETIER_POD_CPU_REQUEST = os.getenv('THOTH_MIDDLETIER_POD_CPU_REQUEST', '0.1')
    THOTH_SECRET = os.environ['THOTH_SECRET']
