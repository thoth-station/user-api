"""Parse packages installed using pip."""

import attr

from .yum import HandlerBase


@attr.s
class PIP(HandlerBase):
    """Handle extracting packages from build logs - pip installer."""

    def run(self, input_text: str) -> dict:
        """Find and parse installed packages and their versions from a build log."""
        return {}


# It looks like the output of pip is same as for pip3. Omit implementation and registering for now.
# HandlerBase.register(PIP)
