#!/usr/bin/env python3

import logging

from .utils import run_analyzer

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def api_analyze(image, analyzer, debug=False, timeout=None):
    try:
        run_analyzer(image, analyzer, debug=debug, timeout=timeout)
    except Exception as exc:
        # TODO: for production we will need to filter out some errors so they are not exposed to users.
        return {'error': str(exc)}, 400
    return {}, 202
