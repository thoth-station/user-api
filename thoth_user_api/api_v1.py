#!/usr/bin/env python3

import json
import os
import re
from itertools import islice

from thoth.storages import AnalysisResultsStore
from thoth.storages import SolverResultsStore
from thoth.storages import BuildLogsStore

from .configuration import Configuration
from .parsing import parse_log as do_parse_log
from .utils import get_pod_log as do_get_pod_log
from .utils import get_pod_status as do_get_pod_status
from .utils import run_adviser
from .utils import run_analyzer
from .utils import run_pod
from .utils import run_solver
from .utils import run_sync

_BUILDLOG_ID_RE = re.compile(r'[a-zA-Z0-9]+')
PAGINATION_SIZE = 100


def analyze(image: str, analyzer: str, debug: bool=False, timeout: int=None,
            cpu_request: str=None, memory_request: str=None):
    """Run an analyzer in a restricted namespace."""
    params = locals()
    try:
        return {
            'pod_id': run_analyzer(**params),
            'parameters': params
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': params
        }, 400


def get_analyzer_result(document_id: str):
    """Retrieve image analyzer result."""
    try:
        adapter = AnalysisResultsStore()
        adapter.connect()
        result = adapter.retrieve_document(document_id)
        return result
    except Exception as exc:
        # TODO: handle 404 as a special case here
        return {
            'error': str(exc),
            'parameters': {
                'document_id': document_id
            }
        }, 400


def list_analyzer_results(page: int):
    """Retrieve image analyzer result."""
    try:
        adapter = AnalysisResultsStore()
        adapter.connect()
        result = adapter.get_document_listing()
        # TODO: I'm not sure if Ceph returns objects in the same order each time.
        # We will need to abandon this logic later anyway once we will be able to query results on data hub side.
        return {
            "results": list(islice(result, page, page + PAGINATION_SIZE)),
            "page": page,
            "page_size": PAGINATION_SIZE
        }
    except Exception as exc:
        # TODO: some errors should be filtered out
        return {
            'error': str(exc),
        }, 400


def run(image: str, environment: dict, cpu_request: str=None, memory_request: str=None):
    """Run an image."""
    params = locals()
    try:
        return {
            'pod_id': run_pod(**params),
            'parameters': params
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': params
        }, 400


def solve(solver: str, packages: dict, debug: bool=False, cpu_request: str=None, memory_request: str=None):
    """Run a solver in a restricted namespace."""
    packages = packages.pop('requirements', '')
    params = locals()
    try:
        return {
            'pod_id': run_solver(**params),
            'parameters': params
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': params
        }, 400


def get_solver_result(document_id: str):
    """Retrieve solver result."""
    try:
        adapter = SolverResultsStore()
        adapter.connect()
        result = adapter.retrieve_document(document_id)
        return result
    except Exception as exc:
        # TODO: handle 404 as a special case here
        return {
            'error': str(exc),
            'parameters': {
                'document_id': document_id
            }
        }, 400


def list_solver_results(page: int):
    """Retrieve image analyzer result."""
    try:
        adapter = SolverResultsStore()
        adapter.connect()
        result = adapter.get_document_listing()
        # TODO: I'm not sure if Ceph returns objects in the same order each time.
        # We will need to abandon this logic later anyway once we will be able to query results on data hub side.
        return {
            "results": list(islice(result, page, page + PAGINATION_SIZE)),
            "page": page,
            "page_size": PAGINATION_SIZE
        }
    except Exception as exc:
        # TODO: some errors should be filtered out
        return {
            'error': str(exc),
        }, 400


def advise(packages: dict, debug: bool=False, packages_only: bool=False):
    """Compute results for the given package or package stack using adviser."""
    packages = packages.pop('requirements', '')
    params = locals()
    try:
        return {
            'pod_id': run_adviser(**params),
            'parameters': params
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
            'parameters': params
        }, 400


def sync(sync_observations: bool=False):
    """Sync results to graph database."""
    try:
        return {
            'pod_id': run_sync(sync_observations),
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {
            'error': str(exc),
        }, 400


def parse_log(log_info: dict):
    """Parse image build log or install log endpoint handler."""
    if not log_info:
        return {'error': 'No log provided'}, 400
    try:
        return do_parse_log(log_info.get('log', '')), 200
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc)}, 400


def get_pod_log(pod_id: str):
    """Get pod log based on analysis id."""
    if pod_id.rsplit(maxsplit=1)[0] == 'thoth-result-api':
        return {'error': "Cannot view pod logs, see OpenShift logs directly to browse thoth-result-api logs"}, 403

    try:
        return {
            'pod_id': pod_id,
            'pod_log': do_get_pod_log(pod_id)
        }
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc), 'pod_id': pod_id}, 400


def get_pod_status(pod_id: str):
    """Get status for a pod."""
    if pod_id.rsplit(maxsplit=1)[0] == 'thoth-result-api':
        return {'error': "Cannot view pod logs, see OpenShift logs directly to browse thoth-result-api logs"}, 403

    try:
        return {
            'pod_id': pod_id,
            'status': do_get_pod_status(pod_id)
        }
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc), 'pod_id': pod_id}, 400


def post_buildlog(log_info: dict):
    """Store the given build log."""
    adapter = BuildLogsStore()
    adapter.connect()
    document_id = adapter.store_document(log_info)

    # Duplicate storing also on PV for now.
    content = json.dumps(log_info, sort_keys=True, indent=2)
    document_path = os.path.join(Configuration.THOTH_BUILDLOGS_PERSISTENT_VOLUME_PATH, document_id + '.json')
    with open(document_path, 'w') as output_file:
        output_file.write(content)

    return {
        'log_id': document_id
    }, 202


def get_buildlog(log_id: str):
    """Retrieve the given buildlog."""
    # adapter = BuildLogsStore()
    # adapter.connect()
    # document = adapter.retrieve_document(log_id)
    if not _BUILDLOG_ID_RE.fullmatch(log_id):
        return {
            'error': 'Invalid buildlog identifier {!r}'.format(log_id),
            'log_id': log_id
        }, 400

    log_file = os.path.join(Configuration.THOTH_BUILDLOGS_PERSISTENT_VOLUME_PATH, log_id + '.json')
    try:
        with open(log_file, 'r') as build_log:
            content = json.load(build_log)
    except FileNotFoundError:
        return {
            'error': 'Buildlog file with id {!r} was not found'.format(log_id),
            'log_id': log_id
        }, 404

    return content, 200
