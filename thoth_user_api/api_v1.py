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

from itertools import islice
import asyncio
import logging
import typing

from thoth.storages import AdvisersResultsStore
from thoth.storages import AnalysisResultsStore
from thoth.storages import BuildLogsStore
from thoth.storages import GraphDatabase
from thoth.storages import ProvenanceResultsStore
from thoth.storages import SolverResultsStore
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
_LOGGER = logging.getLogger('thoth.user_api.api_v1')
_OPENSHIFT = OpenShift()


def post_analyze(image: str, debug: bool = False, registry_user: str = None, registry_password: str = None,
                 verify_tls: bool = True, force: bool = False):
    """Run an analyzer in a restricted namespace."""
    # TODO: check cache here
    return _do_run(locals(), _OPENSHIFT.run_package_extract, output=Configuration.THOTH_ANALYZER_OUTPUT)


def post_image_metadata(image: str, registry_user: str = None, registry_password: str = None,
                        verify_tls: bool = True) -> dict:
    """Get image metadata."""
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
    # TODO: check cache here
    return _do_run(locals(), _OPENSHIFT.run_provenance_checker, output=Configuration.THOTH_PROVENANCE_CHECKER_OUTPUT)


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


def post_solve_python(packages: dict, debug: bool = False, transitive: bool = False, solver: str = None):
    """Run a solver to solve the given ecosystem dependencies."""
    packages = packages.pop('requirements', '')
    parameters = locals()
    response, status_code = _do_run(parameters, _OPENSHIFT.run_solver, output=Configuration.THOTH_SOLVER_OUTPUT)

    # Handle a special case where no solvers for the given name were found.
    if status_code == 202 and not response['analysis_id']:
        if solver:
            return {
                'error': "No solver was run",
                'parameters': parameters
            }, 400
        else:
            return {
                'error': "Please contact administrator - no solvers were installed",
                'parameters': parameters
            }, 500

    return response, status_code


def get_solve_python(analysis_id: str):
    """Retrieve the given solver result."""
    return _get_document(
        SolverResultsStore, analysis_id,
        name_prefix='solver-', namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )


def get_solve_python_log(analysis_id: str):
    """Get solver log."""
    return _get_job_log(locals(), 'solver', Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_solve_python_status(analysis_id: str):
    """Get status of an ecosystem solver."""
    return _get_job_status(locals(), 'solver', Configuration.THOTH_MIDDLETIER_NAMESPACE)


def list_solve_python_results(page: int = 0):
    """Retrieve a listing of available solver results."""
    return _do_listing(SolverResultsStore, page)


def list_solvers():
    """List available registered solvers."""
    # We are fine with 500 here in case of some OpenShift/configuration failures.
    return {
        'solvers': {'python': _OPENSHIFT.get_solver_names()},
        'parameters': {}
    }


def post_advise_python(application_stack: dict, recommendation_type: str, runtime_environment: str = None,
                       debug: bool = False, force: bool = False):
    """Compute results for the given package or package stack using adviser."""
    # TODO: check cache here
    return _do_run(locals(), _OPENSHIFT.run_adviser, output=Configuration.THOTH_ADVISER_OUTPUT)


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


def post_dependency_monkey_python(application_stack: str, runtime_environment: str = None, debug: bool = False):
    """Run dependency monkey on the given application stack to produce all the possible software stacks."""
    # TODO: Change output to Amun once we will have it hosted.
    return _do_run(locals(), _OPENSHIFT.run_dependency_monkey, output=Configuration.THOTH_DEPENDENCY_MONKEY_OUTPUT)


def get_dependency_monkey_python_log(analysis_id: str):
    """Get dependency monkey container log."""
    return _get_job_log(locals(), 'dependency-monkey-', Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_dependency_monkey_python_status(analysis_id: str):
    """Get dependency monkey container status."""
    return _get_job_status(locals(), 'dependency-monkey-', Configuration.THOTH_MIDDLETIER_NAMESPACE)


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


def sync(secret: str, force_analysis_results_sync: bool = False, force_solver_results_sync: bool = False):
    """Sync results to graph database."""
    parameters = locals()
    if secret != Configuration.THOTH_SECRET:
        return {
            'error': 'Wrong secret provided'
        }, 401

    return {
        'sync_id': _OPENSHIFT.run_sync(
            force_analysis_results_sync=force_analysis_results_sync,
            force_solver_results_sync=force_solver_results_sync
        ),
        'parameters': parameters
    }, 202


def erase_graph(secret: str):
    """Clean content of the graph database."""
    if secret != Configuration.THOTH_SECRET:
        return {
            'error': 'Wrong secret provided'
        }, 401

    adapter = GraphDatabase()
    adapter.connect()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(adapter.g.V().drop().next())
    return {}, 201


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
                        (status['state'] == 'terminated' and status['terminated']['exitCode'] == 0):
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
