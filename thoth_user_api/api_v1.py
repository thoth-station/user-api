#!/usr/bin/env python3

import logging

from .utils import get_analysis_log
from .utils import run_analyzer
from .parsing import parse_buildlog

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def api_analyze(image, analyzer, debug=False, timeout=None):
    try:
        analysis_id = run_analyzer(image, analyzer, debug=debug, timeout=timeout)
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc)}, 400
    return {'analysis_id': analysis_id}, 202


def api_parse_buildlog(buildlog_info):
    try:
        return parse_buildlog(buildlog_info.get('buildlog', '')), 200
    except Exception as exc:
        return {'error': str(exc)}, 400


def api_analysis_log(analysis_id):
    try:
        analysis_log = get_analysis_log(analysis_id)
    except Exception as exc:
        return {'error': str(exc)}, 400
    return {'analysis_log': analysis_log, 'analysis_id': analysis_id}, 200
