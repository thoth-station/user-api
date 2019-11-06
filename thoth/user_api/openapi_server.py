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

"""Thoth User API entrypoint."""


import os
import sys
import logging
from datetime import datetime

import connexion
from connexion.resolver import RestyResolver

from flask import redirect, jsonify, request
from flask_script import Manager
from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS

from thoth.common import datetime2datetime_str
from thoth.common import init_logging
from thoth.storages import GraphDatabase
from thoth.storages.exceptions import DatabaseNotInitialized
from thoth.user_api import __version__
from thoth.user_api.configuration import Configuration
from thoth.user_api.configuration import init_jaeger_tracer


# Configure global application logging using Thoth's init_logging.
init_logging(logging_env_var_start="THOTH_USER_API_LOG_")

_LOGGER = logging.getLogger("thoth.user_api")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("THOTH_USER_API_DEBUG", 0))) else logging.INFO)

_LOGGER.info(f"This is User API v%s", __version__)
_LOGGER.debug("DEBUG mode is enabled!")

_THOTH_API_HTTPS = bool(int(os.getenv("THOTH_API_HTTPS", 1)))

# Expose for uWSGI.
app = connexion.FlaskApp(__name__, specification_dir=Configuration.SWAGGER_YAML_PATH, debug=True)

# Add Cross Origin Request Policy to all
CORS(app.app)

app.add_api(
    "openapi.yaml",
    options={"swagger_ui": True},
    arguments={"title": "User API"},
    resolver=RestyResolver(default_module_name="thoth.user_api.api_v1"),
    strict_validation=True,
    validate_responses=False,
)


application = app.app


# create tracer and put it in the application configuration
Configuration.tracer = init_jaeger_tracer("user_api")

# create metrics and manager
metrics = PrometheusMetrics(application, group_by="endpoint")
manager = Manager(application)

# Needed for session.
application.secret_key = Configuration.APP_SECRET_KEY

# static information as metric
metrics.info("user_api_info", "User API info", version=__version__)
_API_GAUGE_METRIC = metrics.info("user_api_schema_up2date", "User API schema up2date")


@application.before_request
def before_request_callback():
    """Callback registered, runs before each request to this service."""
    method = request.method
    path = request.path

    # Update up2date metric exposed.
    if method == "GET" and path == "/metrics":
        graph = GraphDatabase()
        graph.connect()
        try:
            _API_GAUGE_METRIC.set(int(graph.is_schema_up2date()))
        except DatabaseNotInitialized as exc:
            # This can happen if database is erased after the service has been started as we
            # have passed readiness probe with this check.
            _LOGGER.exception("Cannot determine database schema as database is not initialized: %s", str(exc))
            _API_GAUGE_METRIC.set(0)


@app.route("/")
def base_url():
    """Redirect to UI by default."""
    # https://github.com/pallets/flask/issues/773
    request.environ['wsgi.url_scheme'] = 'https' if _THOTH_API_HTTPS else 'http'
    return redirect("api/v1/ui/")


@app.route("/api/v1")
def api_v1():
    """Provide a listing of all available endpoints."""
    paths = []
    for rule in application.url_map.iter_rules():
        rule = str(rule)
        if rule.startswith("/api/v1"):
            paths.append(rule)

    return jsonify({"paths": paths})


def _healthiness():
    graph = GraphDatabase()
    graph.connect()
    return jsonify({"status": "ready", "version": __version__}), 200, {"ContentType": "application/json"}


@app.route("/readiness")
def api_readiness():
    """Report readiness for OpenShift readiness probe."""
    graph = GraphDatabase()
    graph.connect()
    try:
        if not graph.is_schema_up2date():
            _LOGGER.warning("Database schema is not up to date")
            return jsonify({"status": "Database schema is not up to date"}), 503, {"ContentType": "application/json"}
    except DatabaseNotInitialized as exc:
        _LOGGER.warning("Database schema is not initialized")
        return jsonify({"status": str(exc)}), 503, {"ContentType": "application/json"}

    return _healthiness()


@app.route("/liveness")
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
                "details": {"type": exc.__class__.__name__, "datetime": datetime2datetime_str(datetime.utcnow())},
            }
        ),
        500,
    )


@application.after_request
def apply_headers(response):
    """Add headers to each response."""
    response.headers["X-Thoth-Version"] = __version__
    return response


if __name__ == "__main__":
    app.run()

    Configuration.tracer.close()

    sys.exit(1)
