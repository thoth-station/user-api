"""Common library-wide utilities."""

import logging
import requests

from .configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def run_analyzer(image: str, analyzer: str, debug=False, timeout=None):
    """Run an analyzer for the given image."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/api/v1/namespaces/{}/pods".format(Configuration.KUBERNETES_API_URL,
                                                     Configuration.THOTH_ANALYZER_NAMESPACE)

    name_prefix = "{}-{}".format(analyzer, image.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
    # TODO: labels
    payload = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": name_prefix + '-',
            "namespace": Configuration.THOTH_ANALYZER_NAMESPACE,
            "labels": {
                "thothtype": "analyzer"
            }
        },
        "spec": {
            "restartPolicy": "Never",
            "automountServiceAccountToken": False,
            "containers": [{
                "name": analyzer.rsplit('/', maxsplit=1)[-1],
                "image": analyzer,
                "livenessProbe": {
                    "tcpSocket": {
                        "port": 8080
                    },
                    "initialDelaySeconds": Configuration.THOTH_ANALYZER_HARD_TIMEOUT,
                    "failureThreshold": 1,
                    "periodSeconds": 10
                },
                "env": [
                    {"name": "THOTH_ANALYZED_IMAGE", "value": str(image)},
                    {"name": "THOTH_ANALYZER", "value": str(analyzer)},
                    {"name": "THOTH_ANALYZER_DEBUG", "value": str(int(debug))},
                    {"name": "THOTH_ANALYZER_TIMEOUT", "value": str(timeout or 0)}
                ]
            }]
        }
    }

    _LOGGER.debug("Requesting to run analyzer %r with payload %s, OpenShift URL is %r", analyzer, payload, endpoint)
    response = requests.post(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        json=payload,
        verify=False
    )
    _LOGGER.debug("OpenShift master response: %r", response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()
    # TODO: return pod name
