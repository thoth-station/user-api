"""Implementation of build log extraction."""

import logging
import typing

from .handlers import HandlerBase

_LOGGER = logging.getLogger(__name__)


def parse_log(input_text: str) -> typing.List[dict]:
    """Extract Docker image build log and get all installed packages based on ecosystem."""
    result = []
    for handler in HandlerBase.instantiate_handlers():
        result.append({
            'handler': handler.__class__.__name__.lower(),
            'result': handler.run(input_text)
        })

    return result
