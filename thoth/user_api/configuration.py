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

import logging
import os

_LOGGER = logging.getLogger(__name__)

_AMUN_API_URL = os.getenv('AMUN_API_URL') or '-'
if _AMUN_API_URL == '-':
    _LOGGER.warning("Amun API URL was not configured, Dependency Monkey results will not "
                    "be submitted to Amun for inspection!")


class Configuration:
    """Configuration of user-facing API service."""

    APP_SECRET_KEY = os.environ['THOTH_USER_API_APP_SECRET_KEY']
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'swagger.yaml')
    SKOPEO_BIN_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'bin', 'skopeo')
    THOTH_RESULT_API_URL = os.environ['THOTH_RESULT_API_URL']
    THOTH_ADVISER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/adviser-result'
    THOTH_ANALYZER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/analysis-result'
    THOTH_SOLVER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/solver-result'
    THOTH_DEPENDENCY_MONKEY_OUTPUT = _AMUN_API_URL
    THOTH_PROVENANCE_CHECKER_OUTPUT = THOTH_RESULT_API_URL + '/api/v1/provenance-checker-result'
    THOTH_SECRET = os.environ['THOTH_SECRET']
    THOTH_MIDDLETIER_NAMESPACE = os.environ['THOTH_MIDDLETIER_NAMESPACE']
    THOTH_BACKEND_NAMESPACE = os.environ['THOTH_BACKEND_NAMESPACE']
