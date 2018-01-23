"""Common library-wide utilities."""

import datetime
import logging
import requests

from .configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def run_analyzer(image: str, analyzer: str, debug=False, timeout=None):
    """Run an analyzer for the given image."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/apis/batch/v1/namespaces/{}/jobs".format(Configuration.OPENSHIFT_API_URL,
                                                            Configuration.THOTH_ANALYZER_NAMESPACE)
    job_name = "{}-{}-{}".format(analyzer,
                                 image.rsplit('/', maxsplit=1)[-1],
                                 datetime.datetime.now().strftime("%y%m%d-%H%M%S"))
    job_name = job_name.replace(':', '-').replace('/', '-')
    payload = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": job_name,
        },
        "spec": {
            "automountServiceAccountToken": False,
            "backoffLimit": 0,
            "activeDeadlineSeconds": int(datetime.timedelta(days=1).total_seconds()),
            "template": {
                "metadata": {
                    "name": job_name,
                    "namespace": Configuration.THOTH_ANALYZER_NAMESPACE,
                },
                "spec": {
                    "automountServiceAccountToken": False,
                    "restartPolicy": "Never",
                    "containers": [{
                        "name": analyzer.rsplit('/', maxsplit=1)[-1],
                        "image": analyzer,
                        "env": [
                            {"name": "THOTH_ANALYZER", "value": str(analyzer)},
                            {"name": "THOTH_ANALYZER_IMAGE", "value": str(image)},
                            {"name": "THOTH_ANALYZER_DEBUG", "value": str(int(debug))},
                            {"name": "THOTH_ANALYZER_TIMEOUT", "value": str(timeout or 0)}
                        ]
                    }]
                }
            }
        }
    }

    # TODO: add env?
    _LOGGER.debug("Requesting to run analyzer %r with payload %s, OpenShift URL is %r", analyzer, payload, endpoint)
    response = requests.post(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.OPENSHIFT_API_TOKEN),
            'Content-Type': 'application/json'
        },
        json=payload,
        verify=False
    )
    _LOGGER.debug("OpenShift master response: %r", response.text)
    response.raise_for_status()
