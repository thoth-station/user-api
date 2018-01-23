"""Common library-wide utilities."""

import logging
import requests

from .configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def run_analyzer(image: str, analyzer: str, debug=False, timeout=None):
    """Run an analyzer for the given image."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/oapi/v1/namespaces/{}/buildconfigs/" \
               "{}/webhooks/secret/generic".format(Configuration.OPENSHIFT_API_URL,
                                                   Configuration.OPENSHIFT_PROJECT_NAME,
                                                   analyzer)
    payload = {
        'env': [
            {
                'name': 'THOTH_IMAGE',
                'value': image,
            },
            {
                'name': 'THOTH_DEBUG',
                'value': str(int(debug)),
            },
        ]
    }

    if timeout:
        payload['env'].append({
            'name': 'THOTH_TIMEOUT',
            'value': str(int(timeout))
        })

    _LOGGER.debug("Requesting to run analyzer %r with payload %s, OpenShift URL is %r", analyzer, payload, endpoint)
    response = requests.post(
        endpoint,
        headers={
            'Authorization': 'Bearer: {}'.format(Configuration.OPENSHIFT_API_TOKEN),
            'Content-Type': 'application/json'
        },
        json=payload,
        verify=False
    )
    response.raise_for_status()
