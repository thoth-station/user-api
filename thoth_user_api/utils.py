"""Common library-wide utilities."""

import logging
import requests

from .configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def _do_run_pod(template: dict, namespace: str) -> str:
    """Run defined template in Kubernetes."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/api/v1/namespaces/{}/pods".format(Configuration.KUBERNETES_API_URL,
                                                     namespace)
    _LOGGER.debug("Sending POST request to Kubernetes master %r", Configuration.KUBERNETES_API_URL)
    response = requests.post(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        json=template,
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response (%d) from %r: %r",
                  response.status_code, Configuration.KUBERNETES_API_URL, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()

    return response.json()['metadata']['name']


def run_analyzer(image: str, analyzer: str, debug: bool=False, timeout: int=None,
                 cpu_request: str=None, memory_request: str=None) -> str:
    """Run an analyzer for the given image."""
    name_prefix = "{}-{}".format(analyzer, image.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": name_prefix + '-',
            "namespace": Configuration.THOTH_MIDDLEEND_NAMESPACE,
            "labels": {
                "thothtype": "userpod",
                "thothpod": "analyzer"
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
                    {"name": "THOTH_ANALYZER_OUTPUT", "value": Configuration.THOTH_ANALYZER_OUTPUT}
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

    _LOGGER.debug("Requesting to run analyzer %r with payload %s", analyzer, template)
    return _do_run_pod(template, Configuration.THOTH_MIDDLEEND_NAMESPACE)


def run_solver(solver: str, packages: str, debug: bool=False, transitive: bool=True,
               cpu_request: str=None, memory_request: str=None) -> str:
    """Run a solver for the given packages."""
    name_prefix = "{}-{}".format(solver, solver.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": name_prefix + '-',
            "namespace": Configuration.THOTH_MIDDLEEND_NAMESPACE,
            "labels": {
                "thothtype": "userpod",
                "thothpod": "analyzer"
            }
        },
        "spec": {
            "restartPolicy": "Never",
            "automountServiceAccountToken": False,
            "containers": [{
                "name": solver.rsplit('/', maxsplit=1)[-1],
                "image": solver,
                "livenessProbe": {
                    "tcpSocket": {
                        "port": 80
                    },
                    "initialDelaySeconds": Configuration.THOTH_ANALYZER_HARD_TIMEOUT,
                    "failureThreshold": 1,
                    "periodSeconds": 10
                },
                "env": [
                    {"name": "THOTH_SOLVER", "value": str(solver)},
                    {"name": "THOTH_SOLVER_TRANSITIVE", "value": str(int(transitive))},
                    {"name": "THOTH_SOLVER_PACKAGES", "value": str(packages.replace('\n', '\\n'))},
                    {"name": "THOTH_SOLVER_DEBUG", "value": str(int(debug))},
                    {"name": "THOTH_SOLVER_OUTPUT", "value": Configuration.THOTH_SOLVER_OUTPUT}
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

    _LOGGER.debug("Requesting to run solver %r with payload %s", solver, template)
    return _do_run_pod(template, Configuration.THOTH_MIDDLEEND_NAMESPACE)


def run_adviser(packages: str, debug: bool=False, packages_only: bool=False) -> str:
    """Request to run adviser in the backend part."""
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": 'fridex-thoth-adviser-',
            "namespace": Configuration.THOTH_BACKEND_NAMESPACE,
            "labels": {
                "thothpod": "analyzer"
            }
        },
        "spec": {
            "restartPolicy": "Never",
            "automountServiceAccountToken": False,
            "containers": [{
                "name": "thoth-adviser",
                "image": "fridex/thoth-adviser",
                "livenessProbe": {
                    "tcpSocket": {
                        "port": 80
                    },
                    "initialDelaySeconds": Configuration.THOTH_ANALYZER_HARD_TIMEOUT,
                    "failureThreshold": 1,
                    "periodSeconds": 10
                },
                "env": [
                    {"name": "THOTH_ADVISER_PACKAGES", "value": str(packages.replace('\n', '\\n'))},
                    {"name": "THOTH_ADVISER_DEBUG", "value": str(int(debug))},
                    {"name": "THOTH_ADVISER_PACKAGES_ONLY", "value": str(int(packages_only))},
                    {"name": "THOTH_ADVISER_OUTPUT", "value": Configuration.THOTH_ADVISER_OUTPUT}
                ],
            }]
        }
    }

    _LOGGER.debug("Requesting to run adviser with payload %s", template)
    return _do_run_pod(template, Configuration.THOTH_BACKEND_NAMESPACE)


def run_pod(image: str, environment: dict, cpu_request: str=None, memory_request: str=None) -> str:
    """Run a container inside a pod."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    name_prefix = "run-{}".format(image.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": name_prefix + '-',
            "namespace": Configuration.THOTH_MIDDLEEND_NAMESPACE,
            "labels": {
                "thothtype": "userpod",
                "thothpod": "pod"
            }
        },
        "spec": {
            "restartPolicy": "Never",
            "automountServiceAccountToken": False,
            "containers": [{
                "name": image.rsplit('/', maxsplit=1)[-1],
                "image": image,
                "livenessProbe": {
                    "tcpSocket": {
                        "port": 80
                    },
                    "initialDelaySeconds": Configuration.THOTH_ANALYZER_HARD_TIMEOUT,
                    "failureThreshold": 1,
                    "periodSeconds": 10
                },
                "env": environment,
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
    _LOGGER.debug("Requesting to run pod with image %r with payload %s", image, template)
    return _do_run_pod(template, Configuration.THOTH_MIDDLEEND_NAMESPACE)


def run_sync(sync_observations: bool=False) -> str:
    """Run a graph sync."""
    # Let's reuse pod definition from the cronjob definition so any changes in deployed application work out of the box.
    cronjob_def = get_cronjob('thoth-graph-sync-job')
    pod_spec = cronjob_def['spec']['jobTemplate']['spec']['template']['spec']

    # We silently assume that the first container is actually the syncing container.
    for env_conf in pod_spec['containers'][0]['env']:
        if env_conf['name'] == 'THOTH_SYNC_OBSERVATIONS':
            env_conf['value'] = str(int(sync_observations))
            break
    else:
        pod_spec['containers'][0]['env'].append({
            'name': 'THOTH_SYNC_OBSERVATIONS',
            'value': str(int(sync_observations))
        })

    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": 'thoth-graph-sync-',
            "namespace": Configuration.THOTH_BACKEND_NAMESPACE,
            "labels": {
                "thothtype": "userpod",
                "thothpod": "pod",
                "name": "thoth-graph-sync"
            }
        },
        "spec": pod_spec
    }
    _LOGGER.debug("Requesting to run graph sync")
    return _do_run_pod(template, Configuration.THOTH_BACKEND_NAMESPACE)


def get_pod_log(pod_id: str) -> str:
    """Get log of a pod based on assigned pod ID."""
    endpoint = "{}/api/v1/namespaces/{}/pods/{}/log".format(Configuration.KUBERNETES_API_URL,
                                                            Configuration.THOTH_MIDDLEEND_NAMESPACE,
                                                            pod_id)
    response = requests.get(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response for pod log (%d): %r", response.status_code, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()

    return response.text


def get_pod_status(pod_id: str) -> dict:
    """Get status entry for a pod."""
    endpoint = "{}/api/v1/namespaces/{}/pods/{}".format(Configuration.KUBERNETES_API_URL,
                                                        Configuration.THOTH_MIDDLEEND_NAMESPACE,
                                                        pod_id)
    response = requests.get(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response for pod status (%d): %r", response.status_code, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()
    return response.json()['status']['containerStatuses'][0]['state']


def get_cronjob(cronjob_name: str) -> dict:
    endpoint = '{}/apis/batch/v2alpha1/namespaces/{}/cronjobs/{}'.format(Configuration.KUBERNETES_API_URL,
                                                                         Configuration.THOTH_BACKEND_NAMESPACE,
                                                                         cronjob_name)
    response = requests.get(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response for cronjob query with HTTP status code %d", response.status_code)
    if 200 <= response.status_code <= 399:
        _LOGGER.error(response.text)
    response.raise_for_status()
    return response.json()
