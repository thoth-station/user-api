#!/usr/bin/env python3
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

"""Implementation of API v1."""

import hashlib
from itertools import islice
import logging
import typing
import json

from thoth.storages import AdvisersResultsStore
from thoth.storages import AnalysisResultsStore
from thoth.storages import BuildLogsStore
from thoth.storages import GraphDatabase
from thoth.storages import ProvenanceResultsStore
from thoth.storages import AnalysesCacheStore
from thoth.storages.exceptions import CacheMiss
from thoth.storages.exceptions import NotFoundError
from thoth.common import OpenShift
from thoth.common.exceptions import NotFoundException as OpenShiftNotFound

from .configuration import Configuration
from .parsing import parse_log as do_parse_log
from .image import get_image_metadata
from .exceptions import ImageError
from .exceptions import ImageManifestUnknownError
from .exceptions import ImageAuthenticationRequired


PAGINATION_SIZE = 100
_LOGGER = logging.getLogger(__name__)
_OPENSHIFT = OpenShift()


def _compute_digest_params(parameters: dict):
    """Compute digest on parameters passed."""
    return hashlib.sha256(json.dumps(parameters, sort_keys=True).encode()).hexdigest()


def post_analyze(image: str, debug: bool = False, registry_user: str = None, registry_password: str = None,
                 verify_tls: bool = True, force: bool = False):
    """Run an analyzer in a restricted namespace."""
    parameters = locals()
    force = parameters.pop('force', None)

    # Always extract metadata to check for authentication issues and such.
    metadata = _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )

    if isinstance(metadata, tuple):
        # There was an error extracting metadata, tuple holds dictionary with error report and HTTP status code.
        return metadata

    # We compute digest of parameters so we do not reveal any authentication specific info.
    parameters_digest = _compute_digest_params(parameters)
    cache = AnalysesCacheStore()
    cache.connect()
    cached_document_id = metadata['digest'] + '+' + parameters_digest

    if not force:
        try:
            return {
                'analysis_id': cache.retrieve_document_record(cached_document_id).pop('analysis_id'),
                'cached': True,
                'parameters': parameters
            }
        except CacheMiss:
            pass

    response, status_code = _do_run(
        parameters, _OPENSHIFT.run_package_extract, output=Configuration.THOTH_ANALYZER_OUTPUT
    )

    if status_code == 202:
        cache.store_document_record(cached_document_id, {'analysis_id': response['analysis_id']})

    return response, status_code


def post_image_metadata(image: str, registry_user: str = None, registry_password: str = None,
                        verify_tls: bool = True) -> dict:
    """Get image metadata."""
    return _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )


def list_analyze(page: int = 0):
    """Retrieve image analyzer result."""
    return _do_listing(AnalysisResultsStore, page)


def get_analyze(analysis_id: str):
    """Retrieve image analyzer result."""
    return _get_document(
        AnalysisResultsStore, analysis_id,
        name_prefix='package-extract-', namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )


def get_analyze_log(analysis_id: str):
    """Get image analysis log."""
    return _get_job_log(locals(), 'package-extract-', Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_analyze_status(analysis_id: str):
    """Get status of an image analysis."""
    return _get_job_status(locals(), 'package-extract-', Configuration.THOTH_MIDDLETIER_NAMESPACE)


def post_provenance_python(application_stack: dict, debug: bool = False, force: bool = False):
    """Check provenance for the given application stack."""
    parameters = locals()
    # TODO: check cache here
    parameters.pop('force', False)
    return _do_run(parameters, _OPENSHIFT.run_provenance_checker, output=Configuration.THOTH_PROVENANCE_CHECKER_OUTPUT)


def get_provenance_python(analysis_id: str):
    """Retrieve a provenance check result."""
    return _get_document(
        ProvenanceResultsStore, analysis_id,
        name_prefix='provenance-checker-', namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def get_provenance_python_log(analysis_id: str):
    """Get provenance-checker logs."""
    return _get_job_log(locals(), 'provenance-checker-', Configuration.THOTH_BACKEND_NAMESPACE)


def get_provenance_python_status(analysis_id: str):
    """Get status of a provenance check."""
    return _get_job_status(locals(), 'provenance-checker-', Configuration.THOTH_BACKEND_NAMESPACE)


def post_advise_python(input: dict, recommendation_type: str, count: int = None, limit: int = None,
                       debug: bool = False, force: bool = False):
    """Compute results for the given package or package stack using adviser."""
    parameters = locals()
    parameters['application_stack'] = parameters['input'].pop('application_stack')
    parameters['runtime_environment'] = parameters['input'].pop('runtime_environment', None)
    parameters.pop('input')
    # TODO: check cache here
    parameters.pop('force', None)
    return _do_run(parameters, _OPENSHIFT.run_adviser, output=Configuration.THOTH_ADVISER_OUTPUT)


def list_advise_python(page: int = 0):
    """List available runtime environments."""
    return _do_listing(AdvisersResultsStore, page)


def get_advise_python(analysis_id):
    """Retrieve the given recommendation based on its id."""
    return _get_document(
        AdvisersResultsStore, analysis_id,
        name_prefix='adviser-', namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def get_advise_python_log(analysis_id: str):
    """Get adviser log."""
    return _get_job_log(locals(), 'adviser-', Configuration.THOTH_BACKEND_NAMESPACE)


def get_advise_python_status(analysis_id: str):
    """Get status of an adviser run."""
    return _get_job_status(locals(), 'adviser-', Configuration.THOTH_BACKEND_NAMESPACE)


def list_runtime_environments(page: int = 0):
    """List available runtime environments."""
    parameters = locals()

    graph = GraphDatabase()
    graph.connect()

    result = graph.runtime_environment_listing(page, PAGINATION_SIZE)
    return {
        'parameters': parameters,
        'results': result
    }, 200, {
        'page': page,
        'page_size': PAGINATION_SIZE,
        'results_count': len(result)
    }


def get_runtime_environment(runtime_environment_name: str, analysis_id: str = None):
    """Get packages inside the given runtime environment."""
    parameters = locals()

    graph = GraphDatabase()
    graph.connect()

    try:
        results, analysis_document_id = graph.get_runtime_environment(runtime_environment_name, analysis_id)
    except NotFoundError as exc:
        return {
            'error': str(exc),
            'parameters': parameters,
        }, 404

    results = list(map(lambda x: x.to_pretty_dict(), results))
    return {
        'results': results,
        'analysis': graph.get_analysis_metadata(analysis_document_id),
        'results_count': len(results),
        'parameters': parameters,
    }, 200


def list_runtime_environment_analyses(runtime_environment_name: str, page: int = 0):
    """List analyses for the given runtime environment."""
    parameters = locals()

    graph = GraphDatabase()
    graph.connect()
    results = graph.runtime_environment_analyses_listing(runtime_environment_name, page, PAGINATION_SIZE)

    return {
        'results': results,
        'parameters': parameters
    }, 200, {
        'page': page,
        'page_size': PAGINATION_SIZE,
        'results_count': len(results)
    }


def post_buildlog(log_info: dict):
    """Store the given build log."""
    adapter = BuildLogsStore()
    adapter.connect()
    document_id = adapter.store_document(log_info)

    return {
        'document_id': document_id
    }, 202


def get_buildlog(document_id: str):
    """Retrieve the given buildlog."""
    return _get_document(BuildLogsStore, document_id)


def parse_log(log_info: dict):
    """Parse image build log or install log."""
    if not log_info:
        return {
            'error': 'No log provided',
        }, 400

    try:
        return do_parse_log(log_info.get('log', '')), 200
    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc)}, 400


def list_buildlogs(page: int = 0):
    """List available build logs."""
    return _do_listing(BuildLogsStore, page)


def _do_listing(adapter_class, page: int) -> tuple:
    """Perform actual listing of documents available."""
    adapter = adapter_class()
    adapter.connect()
    result = adapter.get_document_listing()
    # TODO: make sure if Ceph returns objects in the same order each time.
    # We will need to abandon this logic later anyway once we will be
    # able to query results on data hub side.
    results = list(islice(result, page * PAGINATION_SIZE, page * PAGINATION_SIZE + PAGINATION_SIZE))
    return {
        'results': results,
        'parameters': {'page': page}
    }, 200, {
        'page': page,
        'page_size': PAGINATION_SIZE,
        'results_count': len(results)
    }


def _get_document(adapter_class, analysis_id: str, name_prefix: str = None, namespace: str = None) -> tuple:
    """Perform actual document retrieval."""
    # Parameters to be reported back to a user of API.
    parameters = {'analysis_id': analysis_id}
    if not analysis_id.startswith(name_prefix):
        return {
            'error': 'Wrong analysis id provided',
            'parameters': parameters
        }, 400

    try:
        adapter = adapter_class()
        adapter.connect()
        result = adapter.retrieve_document(analysis_id)
        return result, 200
    except NotFoundError:
        if namespace:
            try:
                status = _OPENSHIFT.get_job_status_report(analysis_id, namespace=namespace)
                if status['state'] == 'running' or \
                        (status['state'] == 'terminated' and status['exit_code'] == 0):
                    # In case we hit terminated and exit code equal to 0, the analysis has just finished and
                    # before this call (document retrieval was unsuccessful, pod finished and we asked later
                    # for status). To fix this time-dependent issue, let's user ask again. Do not do pod status
                    # check before document retrieval - this solution is more optimal as we do not ask master
                    # status each time.
                    return {
                        'error': 'Analysis is still in progress',
                        'status': status,
                        'parameters': parameters
                    }, 202
                elif status['state'] == 'terminated':
                    return {
                        'error': 'Analysis was not successful',
                        'status': status,
                        'parameters': parameters
                    }, 404
                elif status['state'] in ('scheduling', 'waiting'):
                    return {
                        'error': 'Analysis is being scheduled',
                        'status': status,
                        'parameters': parameters
                    }, 202
                else:
                    # Can be:
                    #   - return 500 to user as this is our issue
                    raise ValueError(f"Unreachable - unknown job state: {status}")
            except OpenShiftNotFound:
                pass
        return {
            'error': f'Requested result for analysis {analysis_id!r} was not found',
            'parameters': parameters
        }, 404


def _get_job_log(parameters: dict, name_prefix: str, namespace: str):
    """Get job log based on analysis id."""
    job_id = parameters.get('analysis_id')
    if not job_id.startswith(name_prefix):
        return {
            'error': 'Wrong analysis id provided',
            'parameters': parameters
        }, 400

    return {
        'parameters': parameters,
        'log': _OPENSHIFT.get_job_log(job_id, namespace=namespace)
    }, 200


def _get_job_status(parameters: dict, name_prefix: str, namespace: str):
    """Get status for a job."""
    job_id = parameters.get('analysis_id')
    if not job_id.startswith(name_prefix):
        return {
            'error': 'Wrong analysis id provided',
            'parameters': parameters
        }, 400

    status = _OPENSHIFT.get_job_status_report(job_id, namespace=namespace)
    return {
        'parameters': parameters,
        'status': status
    }


def _do_run(parameters: dict, runner: typing.Callable, **runner_kwargs):
    """Run the given job - a generic method for running any analyzer, solver, ..."""
    return {
        'analysis_id': runner(**parameters, **runner_kwargs),
        'parameters': parameters,
        'cached': False
    }, 202


def _do_get_image_metadata(image: str, registry_user: str = None, registry_password: str = None,
                           verify_tls: bool = True) -> dict:
    """Wrap function call with additional checks."""
    try:
        return get_image_metadata(
            image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
        )
    except ImageManifestUnknownError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageAuthenticationRequired as exc:
        status_code = 401
        error_str = str(exc)
    except ImageError as exc:
        status_code = 400
        error_str = str(exc)

    return {
        'error': error_str,
        'parameters': locals()
    }, status_code
