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
"""Core Thoth user API."""

import logging
from datetime import datetime

import connexion

from flask import redirect, jsonify
from flask_script import Manager
from prometheus_flask_exporter import PrometheusMetrics

from thoth.common import SafeJSONEncoder
from thoth.common import init_logging
from thoth.common import logger_setup
from thoth.storages import SolverResultsStore

import thoth.user_api as thoth_user_api

from .configuration import Configuration

# Expose for uWSGI.
app = connexion.App(__name__)
application = app.app
init_logging()
_LOGGER = logging.getLogger("thoth.user_api")

app.add_api(Configuration.SWAGGER_YAML_PATH)
application.json_encoder = SafeJSONEncoder
metrics = PrometheusMetrics(application)
manager = Manager(application)

# Needed for session.
application.secret_key = Configuration.APP_SECRET_KEY

# static information as metric
metrics.info("user_api_info", "User API info", version=thoth_user_api.__version__)


@app.route("/")
@metrics.do_not_track()
def base_url():
    """Redirect to UI by default."""
    return redirect("api/v1/ui")


@app.route("/api/v1")
@metrics.do_not_track()
def api_v1():
    """Provide a listing of all available endpoints."""
    paths = []

    for rule in application.url_map.iter_rules():
        rule = str(rule)
        if rule.startswith("/api/v1"):
            paths.append(rule)

    return jsonify({"paths": paths})


def _healthiness():
    """Check service healthiness."""
    # Check that Ceph is reachable.
    adapter = SolverResultsStore()
    adapter.connect()
    adapter.ceph.check_connection()

    return jsonify({"status": "ready", "version": thoth_user_api.__version__}), 200, {"ContentType": "application/json"}


@logger_setup("werkzeug", logging.WARNING)
@logger_setup("botocore.vendored.requests.packages.urllib3.connectionpool", logging.WARNING)
@app.route("/readiness")
@metrics.do_not_track()
def api_readiness():
    """Report readiness for OpenShift readiness probe."""
    return _healthiness()


@logger_setup("werkzeug", logging.WARNING)
@logger_setup("botocore.vendored.requests.packages.urllib3.connectionpool", logging.WARNING)
@app.route("/liveness")
@metrics.do_not_track()
def api_liveness():
    """Report liveness for OpenShift readiness probe."""
    return _healthiness()


@application.errorhandler(404)
@metrics.do_not_track()
def page_not_found(exc):
    """Adjust 404 page to be consistent with errors reported back from API."""
    # Flask has a nice error message - reuse it.
    return jsonify({"error": str(exc)}), 404


@application.errorhandler(500)
@metrics.do_not_track()
def internal_server_error(exc):
    """Adjust 500 page to be consistent with errors reported back from API."""
    # Provide some additional information so we can easily find exceptions in logs (time and exception type).
    # Later we should remove exception type (for security reasons).
    return (
        jsonify(
            {
                "error": "Internal server error occurred, please contact administrator with provided details.",
                "details": {"type": exc.__class__.__name__, "datetime": datetime.utcnow().isoformat()},
            }
        ),
        500,
    )


if __name__ == "__main__":
    _LOGGER.info(f"Thoth User API v{thoth_user_api.__version__}")
    manager.run()
