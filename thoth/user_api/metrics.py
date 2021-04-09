#!/usr/bin/env python3
# thoth-user-api
# Copyright(C) 2021 Francesco Murdaca
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

"""Custom metrics for user-facing API service."""

import logging

_LOGGER = logging.getLogger(__name__)


class MetricsValues(object):
    """Metrics values for counters."""

    def __init__(self):
        """Initialize Metrics Values Class."""
        self.metric_cache_hit_adviser_auth = 0
        self.metric_cache_hit_adviser_unauth = 0
        self.metric_cache_hit_provenance_checker_auth = 0
        self.metric_cache_hit_provenance_checker_unauth = 0

    def update_adviser_cache_hit_metric(self, is_auth: bool = False):
        """Update adviser cache hit metric values."""
        if is_auth:
            self.metric_cache_hit_adviser_auth += 1
        else:
            self.metric_cache_hit_adviser_unauth += 1

    def update_provenance_checker_cache_hit_metric(self, is_auth: bool = False):
        """Update provenance checker cache hit metric values."""
        if is_auth:
            self.metric_cache_hit_provenance_checker_auth += 1
        else:
            self.metric_cache_hit_provenance_checker_unauth += 1
