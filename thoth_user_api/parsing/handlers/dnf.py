"""Parse packages installed using dnf."""

import attr

from .yum import HandlerBase


@attr.s
class DNF(HandlerBase):
    """Handle extracting packages from build logs - dnf installer."""

    def run(self, input_text: str) -> dict:
        """Find and parse installed packages and their versions from a build log."""
        return {}


# It looks like the output of dnf is same as for yum. Omit implementation and registering for now.
# HandlerBase.register(DNF)
