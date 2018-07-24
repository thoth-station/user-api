#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thoth-user-api
# Copyright(C) 2018 Fridolin Pokorny
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

"""Common library-wide utilities."""

import logging
import requests

from kubernetes import client, config
from openshift.dynamic import DynamicClient
import openshift

from .configuration import Configuration
from .exceptions import NotFoundException

# Load in-cluster configuration that is exposed by OpenShift/k8s configuration.
config.load_incluster_config()

_OPENSHIFT_CLIENT = DynamicClient(client.ApiClient(configuration=client.Configuration()))
_LOGGER = logging.getLogger('thoth.user_api.utils')


def _set_env_var(template: dict, **env_var):
    """Set environment in the given template."""
    for env_var_name, env_var_value in env_var.items():
        for entry in template['spec']['containers'][0]['env']:
            if entry['name'] == env_var_name:
                entry['value'] = env_var_value
                break
        else:
            template['spec']['containers'][0]['env'].append(
                {'name': env_var_name, 'value': str(env_var_value)}
            )


def _set_template_parameters(template: dict, **parameters: object) -> None:
    """Set parameters in the template - replace existing ones or append to parameter list if not exist.

    >>> _set_template_parameters(template, THOTH_LOG_ADVISER='DEBUG')
    """
    if 'parameters' not in template:
        template['parameters'] = []

    for parameter_name, parameter_value in parameters.items():
        for entry in template['parameters']:
            if entry['name'] == parameter_name:
                entry['value'] = str(parameter_value)
                break
        else:
            template['parameters'].append({
                'name': parameter_name,
                'value': str(parameter_value)
            })


def run_sync(force_analysis_results_sync: bool = False, force_solver_results_sync: bool = False) -> str:
    """Run graph sync, base pod definition based on job definition."""
    # Let's reuse pod definition from the cronjob definition so any changes in
    # deployed application work out of the box.
    _LOGGER.debug("Retrieving graph-sync CronJob definition")
    response = _OPENSHIFT_CLIENT.resources.get(api_version='v2alpha1', kind='CronJob').get(
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
        name='graph-sync'
    )
    template = response.to_dict()['spec']['jobTemplate']['spec']['template']
    _set_env_var(
        template,
        THOTH_GRAPH_SYNC_FORCE_ANALYSIS_RESULTS_SYNC=int(force_analysis_results_sync),
        THOTH_GRAPH_SYNC_FORCE_SOLVER_RESULTS_SYNC=int(force_solver_results_sync)
    )

    # Construct a Pod spec.
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": 'graph-sync-',
            "labels": template['metadata'].get('labels', {})
        },
        "spec": template['spec']
    }

    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Pod').create(
        body=template,
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )

    _LOGGER.debug(f"Started graph-sync pod with name {response.metadata.name}")
    return response.metadata.name


def get_pod_log(pod_id: str) -> str:
    """Get log of a pod based on assigned pod ID."""
    # TODO: rewrite to OpenShift rest client once it will support it.
    endpoint = "{}/api/v1/namespaces/{}/pods/{}/log".format(
        Configuration.KUBERNETES_API_URL,
        Configuration.THOTH_MIDDLETIER_NAMESPACE,
        pod_id
    )

    response = requests.get(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response for pod log (%d): %r", response.status_code, response.text)
    response.raise_for_status()

    return response.text


def get_pod_status(pod_id: str) -> dict:
    """Get status entry for a pod - this applies only for solver and package-extract pods."""
    try:
        response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Pod').get(
            namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
            name=pod_id
        )
    except openshift.dynamic.exceptions.NotFoundError as exc:
        raise NotFoundException(f"The given pod with id {pod_id} could not be found") from exc

    _LOGGER.debug("OpenShift master response for pod status (%d): %r", response.to_dict())
    return response.to_dict()['status']['containerStatuses'][0]['state']


def get_solver_names() -> list:
    """Retrieve name of solvers available in installation."""
    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Template').get(
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
        label_selector='template=solver'
    )
    _LOGGER.debug("OpenShift response for getting solver template: %r", response.to_dict())
    _raise_on_invalid_response_size(response)
    return [obj['metadata']['labels']['component'] for obj in response.to_dict()['items'][0]['objects']]


def run_solver(packages: str, debug: bool = False, transitive: bool = True, solver: str = None) -> dict:
    """Run solver or all solver to solve the given requirements."""
    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Template').get(
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
        label_selector='template=solver'
    )
    _LOGGER.debug("OpenShift response for getting solver template: %r", response.to_dict())

    _raise_on_invalid_response_size(response)
    template = response.to_dict()['items'][0]

    _set_template_parameters(
        template,
        THOTH_SOLVER_NO_TRANSITIVE=int(not transitive),
        THOTH_SOLVER_PACKAGES=packages.replace('\n', '\\n'),
        THOTH_LOG_SOLVER='DEBUG' if debug else 'INFO',
        THOTH_SOLVER_OUTPUT=Configuration.THOTH_SOLVER_OUTPUT
    )

    template = _oc_process(Configuration.THOTH_MIDDLETIER_NAMESPACE, template)

    solvers = {}
    for obj in template['objects']:
        solver_name = obj['metadata']['labels']['component']
        if solver and solver != solver_name:
            _LOGGER.debug(f"Skipping solver %r as the requested solver is %r", solver_name, solver)
            continue

        response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind=obj['kind']).create(
            body=obj,
            namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
        )

        _LOGGER.debug("Starting solver %r", solver_name)
        _LOGGER.debug("OpenShift response for creating a pod: %r", response.to_dict())
        solvers[solver_name] = response.metadata.name

    return solvers


def run_package_extract(image: str, debug: bool = False,
                        registry_user: str = None, registry_password: str = None, verify_tls: bool = True) -> str:
    """Run package-extract analyzer to extract information from the provided image."""
    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Template').get(
        namespace=Configuration.THOTH_INFRA_NAMESPACE,
        label_selector='template=package-extract'
    )
    _LOGGER.debug("OpenShift response for getting package-extract template: %r", response.to_dict())
    _raise_on_invalid_response_size(response)
    template = response.to_dict()['items'][0]

    _set_template_parameters(
        template,
        THOTH_LOG_PACKAGE__EXTRACT='DEBUG' if debug else 'INFO',
        THOTH_ANALYZED_IMAGE=image,
        THOTH_ANALYZER_NO_TLS_VERIFY=int(not verify_tls),
        THOTH_ANALYZER_OUTPUT=Configuration.THOTH_ANALYZER_OUTPUT
    )

    if registry_user and registry_password:
        _set_template_parameters(
            template,
            THOTH_REGISTRY_CREDENTIALS=f"{registry_user}:{registry_password}"
        )

    template = _oc_process(Configuration.THOTH_MIDDLETIER_NAMESPACE, template)
    analyzer = template['objects'][0]

    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind=analyzer['kind']).create(
        body=analyzer,
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )

    _LOGGER.debug("OpenShift response for creating a pod: %r", response.to_dict())
    return response.metadata.name


def run_adviser(application_stack: dict, type: str, runtime_environment: str = None, debug: bool = False) -> str:
    """Run adviser on the provided user input."""
    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind='Template').get(
        namespace=Configuration.THOTH_INFRA_NAMESPACE,
        label_selector='template=adviser'
    )
    _LOGGER.debug("OpenShift response for getting adviser template: %r", response.to_dict())
    _raise_on_invalid_response_size(response)

    template = response.to_dict()['items'][0]
    _set_template_parameters(
        template,
        THOTH_ADVISER_REQUIREMENTS=application_stack.pop('requirements'),
        THOTH_ADVISER_REQUIREMENTS_LOCKED=application_stack.get('requirements_lock', ''),
        THOTH_ADVISER_REQUIREMENTS_FORMAT=application_stack.get('requirements_formant', 'pipenv'),
        THOTH_ADVISER_RECOMMENDATION_TYPE=type,
        THOTH_ADVISER_RUNTIME_ENVIRONMENT=runtime_environment,
        THOTH_ADVISER_OUTPUT=Configuration.THOTH_ADVISER_OUTPUT,
        THOTH_LOG_ADVISER='DEBUG' if debug else 'INFO'
    )

    template = _oc_process(Configuration.THOTH_MIDDLETIER_NAMESPACE, template)
    adviser = template['objects'][0]

    response = _OPENSHIFT_CLIENT.resources.get(api_version='v1', kind=adviser['kind']).create(
        body=adviser,
        namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )

    _LOGGER.debug("OpenShift response for creating a pod: %r", response.to_dict())
    return response.metadata.name


def _raise_on_invalid_response_size(response):
    """It is expected that there is only one object type for the given item."""
    if len(response.items) != 1:
        raise RuntimeError(
            f"Application misconfiguration - number of templates available in the infra namespace "
            f"{Configuration.THOTH_INFRA_NAMESPACE!r} is {len(response.items)}, should be 1."
        )


def _oc_process(namespace: str, template: dict) -> dict:
    """Process the given template in OpenShift."""
    # This does not work - see issue reported upstream:
    #   https://github.com/openshift/openshift-restclient-python/issues/190
    # return TemplateOpenshiftIoApi().create_namespaced_processed_template_v1(namespace, template)
    endpoint = "{}/apis/template.openshift.io/v1/namespaces/{}/processedtemplates".format(
        Configuration.OPENSHIFT_API_URL,
        namespace
    )
    response = requests.post(
        endpoint,
        json=template,
        headers={
            'Authorization': 'Bearer {}'.format(Configuration.KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        verify=Configuration.KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("OpenShift master response template (%d): %r", response.status_code, response.text)

    try:
        response.raise_for_status()
    except Exception:
        _LOGGER.error("Failed to process template: %s", response.text)
        raise

    return response.json()
