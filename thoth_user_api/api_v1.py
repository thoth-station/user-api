#!/usr/bin/env python3

from .utils import get_pod_log
from .utils import run_analyzer
from .parsing import parse_log


def api_analyze(image: str, analyzer: str, debug: bool=False, timeout: int=None):
    """Run an analyzer in a restricted namespace."""
    try:
        return {
            'analysis_id': run_analyzer(image, analyzer, debug=debug, timeout=timeout),
        }, 202
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc), 'image': image, 'analyzer': analyzer, 'debug': debug, 'timeout': timeout}, 400


def api_parse_log(log_info: dict):
    """Parse image build log or install log endpoint handler."""
    if not log_info:
        return {'error': 'No log provided'}, 400
    try:
        return parse_log(log_info.get('log', '')), 200
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc)}, 400


def api_pod_log(pod_id: str):
    """Get pod log based on analysis id."""
    try:
        return {
            'pod_id': pod_id,
            'pod_log': get_pod_log(pod_id)
        }
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc), 'pod_id': pod_id}, 400
