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

import asyncio
import logging
from itertools import islice

from thoth.storages import AdvisersResultsStore
from thoth.storages import AnalysisResultsStore
from thoth.storages import SolverResultsStore
from thoth.storages import BuildLogsStore
from thoth.storages import GraphDatabase
from thoth.storages.exceptions import NotFoundError
from thoth.common import OpenShift

from .configuration import Configuration
from .parsing import parse_log as do_parse_log


PAGINATION_SIZE = 100
_LOGGER = logging.getLogger('thoth.user_api.api_v1')
_OPENSHIFT = OpenShift()


def analyze(image: str, debug: bool = False, registry_user: str = None, registry_password=None,
            verify_tls: bool = True):
    """Run an analyzer in a restricted namespace."""
    parameters = locals()
    try:
        return {
            'analysis_id': _OPENSHIFT.run_package_extract(**parameters, output=Configuration.THOTH_ANALYZER_OUTPUT),
            'parameters': parameters
        }, 202
    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def list_solvers():
    """List available registered solvers."""
    # We are fine with 500 here in case of some OpenShift/configuration failures.
    return {
        'solvers': _OPENSHIFT.get_solver_names(),
        'parameters': {}
    }


def solve(packages: dict, debug: bool = False, transitive: bool = False, solver: str = None):
    """Run a solver in a restricted namespace."""
    parameters = locals()
    packages = packages.pop('requirements', '')
    try:
        return {
            'analysis_id': _OPENSHIFT.run_solver(**parameters, output=Configuration.THOTH_SOLVER_OUTPUT),
            'parameters': parameters
        }, 202
    except Exception as exc:
        _LOGGER.exception("Failed to run solver for packages: %s", str(exc))
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def post_recommendation_python(application_stack: dict, type: str,
                               runtime_environment: str = None, debug: bool = False):
    """Compute results for the given package or package stack using adviser."""
    parameters = locals()
    try:
        return {
            'analysis_id': _OPENSHIFT.run_adviser(**parameters, output=Configuration.THOTH_ADVISER_OUTPUT),
            'parameters': parameters
        }, 202
    except Exception as exc:
        _LOGGER.error(f"Failed to run adviser for {application_stack!r}")
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so
        # they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def post_provenance_python(application_stack: dict, debug: bool = False):
    """Check provenance for the given application stack."""
    parameters = locals()
    try:
        return {
            'analysis_id:': _OPENSHIFT.run_provenance_checker(
                **parameters,
                output=Configuration.THOTH_PROVENANCE_CHECKER_OUTPUT
            ),
            'parameters': parameters
        }, 202
    except Exception as exc:
        _LOGGER.error("Failed to run provenance checker: %s", str(exc))
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def sync(secret: str, force_analysis_results_sync: bool = False, force_solver_results_sync: bool = False):
    """Sync results to graph database."""
    parameters = locals()
    if secret != Configuration.THOTH_SECRET:
        return {
            'error': 'Wrong secret provided'
        }, 401

    try:
        return {
            'sync_id': _OPENSHIFT.run_sync(
                force_analysis_results_sync=force_analysis_results_sync,
                force_solver_results_sync=force_solver_results_sync
            ),
            'parameters': parameters
        }, 202
    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so
        # they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def parse_log(log_info: dict):
    """Parse image build log or install log endpoint handler."""
    if not log_info:
        return {'error': 'No log provided'}, 400
    try:
        return do_parse_log(log_info.get('log', '')), 200
    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so
        # they are not exposed to users.
        return {'error': str(exc)}, 400


def get_analysis_log(analysis_id: str):
    """Get pod log based on analysis id."""
    parameters = locals()

    if analysis_id.rsplit(maxsplit=1)[0] == 'result-api':
        return {'error': "Cannot view pod logs, see OpenShift logs directly to browse result-api logs"}, 403

    try:
        return {
            'parameters': parameters,
            'log': _OPENSHIFT.get_pod_log(analysis_id)
        }

    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: for production we will need to filter out some errors so
        # they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def get_analysis_status(analysis_id: str):
    """Get status for a pod."""
    parameters = locals()

    if analysis_id.rsplit(maxsplit=1)[0] == 'result-api':
        return {'error': "Cannot view pod logs, see OpenShift logs directly to browse result-api logs"}, 403

    try:
        return {
            'parameters': parameters,
            'status': _OPENSHIFT.get_pod_status(analysis_id)
        }
    except Exception as exc:
        _LOGGER.exception("Failed to retrieve analysis status: %s", str(exc))
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': parameters
        }, 400


def post_buildlog(log_info: dict):
    """Store the given build log."""
    adapter = BuildLogsStore()
    adapter.connect()
    document_id = adapter.store_document(log_info)

    return {
        'document_id': document_id
    }, 202


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


def get_runtime_environment(runtime_environment_name: str,
                            analysis_id: str = None):
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


def list_runtime_environment_analyses(runtime_environment_name: str,
                                      page: int = 0):
    """List analyses for the given runtime environment."""
    parameters = locals()

    graph = GraphDatabase()
    graph.connect()
    try:
        results = graph.runtime_environment_analyses_listing(
            runtime_environment_name, page, PAGINATION_SIZE)
    except NotFoundError as exc:
        return {
            'error': str(exc),
            'parameters': parameters
        }, 404

    return {
        'results': results,
        'parameters': parameters
    }, 200, {
        'page': page,
        'page_size': PAGINATION_SIZE,
        'results_count': len(results)
    }


def list_buildlogs(page: int = 0):
    """List available build logs."""
    return _do_listing(BuildLogsStore, page)


def list_analyzer_results(page: int = 0):
    """Retrieve image analyzer result."""
    return _do_listing(AnalysisResultsStore, page)


def list_adviser_results(page: int = 0):
    """List available runtime environments."""
    return _do_listing(AdvisersResultsStore, page)


def list_solver_results(page: int = 0):
    """Retrieve image analyzer result."""
    return _do_listing(SolverResultsStore, page)


def _do_listing(adapter_class, page: int) -> tuple:
    """Perform actual listing."""
    try:
        adapter = adapter_class()
        adapter.connect()
        result = adapter.get_document_listing()
        # TODO: not sure if Ceph returns objects in the same order each time.
        # We will need to abandon this logic later anyway once we will be
        # able to query results on data hub side.
        results = list(islice(result, page * PAGINATION_SIZE,
                              page * PAGINATION_SIZE + PAGINATION_SIZE))
        return {
            'results': results,
            'parameters': {'page': page}
        }, 200, {
            'page': page,
            'page_size': PAGINATION_SIZE,
            'results_count': len(results)
        }
    except Exception as exc:
        _LOGGER.exception(str(exc))
        # TODO: some errors should be filtered out
        return {
            'error': str(exc),
            'parameters': {'page': page}
        }, 400


def get_solver_result(document_id: str):
    """Retrieve solver result."""
    return _get_document(SolverResultsStore, document_id)


def get_analyzer_result(document_id: str):
    """Retrieve image analyzer result."""
    return _get_document(AnalysisResultsStore, document_id)


def get_buildlog(document_id: str):
    """Retrieve the given buildlog."""
    return _get_document(BuildLogsStore, document_id)


def get_recommendation_python_id(recommendation_id):
    """Retrieve the given recommendation based on its id."""
    return _get_document(AdvisersResultsStore, recommendation_id)


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


def _get_document(adapter_class, document_id: str) -> tuple:
    """Perform actual document retrieval."""
    try:
        adapter = adapter_class()
        adapter.connect()
        result = adapter.retrieve_document(document_id)
        return result, 200
    except NotFoundError:
        return {
            'error': f'Requested document {document_id!r} was not found',
            'parameters': {
                'document_id': document_id
            }
        }, 404
    except Exception as exc:
        _LOGGER.exception(str(exc))
        return {
            'error': str(exc),
            'parameters': {
                'document_id': document_id
            }
        }, 400
