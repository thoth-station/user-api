"""Common library-wide utilities."""

import logging
import requests

from .configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def run_analyzer(image: str, analyzer: str, debug: bool=False, timeout: int=None,
                 cpu_request: str=None, memory_request: str=None) -> str:
    """Run an analyzer for the given image."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/api/v1/namespaces/{}/pods".format(Configuration.KUBERNETES_API_URL,
                                                     Configuration.THOTH_ANALYZER_NAMESPACE)

    name_prefix = "{}-{}".format(analyzer, image.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
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
                    {"name": "THOTH_ANALYZER_TIMEOUT", "value": str(timeout or 0)},
                    {"name": "THOTH_RESULT_API_HOSTNAME", "value": Configuration.THOTH_RESULT_API_HOSTNAME}
                ],
                "resources": {
                    "limits": {
                        "memory": Configuration.THOTH_MIDDLEEND_POD_MEMORY_LIMIT,
                        "cpu": Configuration.THOTH_MIDDLEEND_POD_CPU_LIMIT
                    },
                    "requests": {
                        "memory": memory_request or Configuration.THOTH_MIDDLEEND_POD_MEMORY_REQUEST,
                        "cpu": cpu_request or Configuration.THOTH_MIDDLEEND_POD_CPU_REQUEST
                    }
                }
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
    _LOGGER.debug("Kubernetes master response (%d): %r", response.status_code, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()

    return response.json()['metadata']['name']


def get_pod_log(pod_id: str) -> str:
    """Get log of a pod based on assigned pod ID."""
    endpoint = "{}/api/v1/namespaces/{}/pods/{}/log".format(Configuration.KUBERNETES_API_URL,
                                                            Configuration.THOTH_ANALYZER_NAMESPACE,
                                                            pod_id)
    response = requests.get(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=False
    )
    _LOGGER.debug("Kubernetes master response (%d): %r", response.status_code, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()

    return response.text
