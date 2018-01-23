#!/usr/bin/env python3
from datetime import datetime
import json
import logging

from flask import redirect, jsonify
import connexion
from flask_script import Manager

from .configuration import Configuration


class SafeJSONEncoder(json.JSONEncoder):
    """Convert objects to JSON, safely."""

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return repr(o)


def init_logging():
    """Initialize application logging."""
    # Initialize flask logging
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)

    # Use flask App instead of Connexion's one
    application.logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    liblog = logging.getLogger('thoth_pkgdeps')
    liblog.setLevel(logging.DEBUG)
    liblog.addHandler(handler)


# Expose for uWSGI.
app = connexion.App(__name__)
application = app.app
init_logging()
app.add_api(Configuration.SWAGGER_YAML_PATH)
application.json_encoder = SafeJSONEncoder
manager = Manager(application)
# Needed for session.
application.secret_key = Configuration.APP_SECRET_KEY


@app.route('/')
def base_url():
    # Be nice with user access
    return redirect('api/v1/ui')


@app.route('/api/v1')
def api_v1():
    paths = []

    for rule in application.url_map.iter_rules():
        rule = str(rule)
        if rule.startswith('/api/v1'):
            paths.append(rule)

    return jsonify({'paths': paths})


@app.route('/readiness')
def api_readiness():
    # TODO: extend
    return jsonify(None)


@app.route('/liveness')
def api_liveness():
    # TODO: extend
    return jsonify(None)


if __name__ == '__main__':
    manager.run()
