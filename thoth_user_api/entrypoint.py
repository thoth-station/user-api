#!/usr/bin/env python3

import logging

import requests

from flask import redirect, jsonify
import connexion
from flask_script import Manager

from thoth.common import SafeJSONEncoder

from .configuration import Configuration


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
    return jsonify(None)


@app.route('/liveness')
def api_liveness():
    response = requests.get(Configuration.KUBERNETES_API_URL, verify=Configuration.KUBERNETES_VERIFY_TLS)
    response.raise_for_status()
    return jsonify(None)


if __name__ == '__main__':
    manager.run()
