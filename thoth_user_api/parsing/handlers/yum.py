"""Handle output of yum command - parse installed packages."""

import logging
import re
import typing

import attr

from .base import HandlerBase

_RE_EPOCH_VERSION = re.compile(r'([0-9]+):(.+)')
_RE_DEPENDENCY = re.compile(r'--> Processing Dependency: '
                            r'([a-zA-Z_\-.():/0-9>=< ]+) for package: ([a-zA-Z_\-.():0-9]+)')

_LOG = logging.getLogger(__name__)


@attr.s
class YUM(HandlerBase):
    """Handle extracting packages from build logs - yum installer."""

    @staticmethod
    def _parse_yum_table_heading(lines: typing.List[str], start_index: int) -> int:
        """Parse yum table heading, return increment for which there should be done proceeding."""
        header_items = ['Package', 'Arch', 'Version', 'Repository', 'Size']
        heading = [item for item in lines[start_index].split(' ') if item]
        if heading != header_items:
            # yum can break table into multiple lines for some reason - this can be inconsistent
            # regardless of terminal size in a single run
            second_line = [item for item in lines[start_index + 1].split(' ') if item]
            heading.extend(second_line)
            if heading != header_items:
                return 0

            return 2

        return 1

    @classmethod
    def _parse_yum_table(cls, lines: typing.List[str], start_index: int) -> typing.Tuple[list, int]:
        """Parse installed packages from a table reported by yum installer."""
        table_offset = cls._parse_yum_table_heading(lines, start_index + 1)
        if not table_offset:
            _LOG.debug("Unable to parse heading for yum table, skipping (line was: %r)", lines[start_index + 1])
            return [], 0

        start_index += table_offset

        if lines[start_index + 1] != '='*80:
            _LOG.debug("Unable to find table start, giving up (line was: %r)", lines[start_index + 1])
            return [], 0

        if lines[start_index + 2].startswith('Installing:'):
            upgrading = False
        elif lines[start_index + 2].startswith('Upgrading:'):
            upgrading = True
        else:
            _LOG.debug("Unable to find table start with 'Installing', giving up (line was: %r)", lines[start_index + 2])
            return [], 0

        reported_packages = []
        index_increment = start_index + 3
        is_dependency = False
        while index_increment < len(lines):
            items = [item for item in lines[index_increment].split(' ') if item]
            if lines[index_increment].startswith(' ') and len(items) == 6:
                epoch = None
                version = items[2]
                match = _RE_EPOCH_VERSION.fullmatch(version)
                if match:
                    epoch = int(match.group(1))
                    version = match.group(2)

                # Number of items is 5 but yum reports size with a space between size and unit (e.g. '1.5 M')
                reported_packages.append({
                    'name': items[0],
                    'arch': items[1],
                    'version': version,
                    'epoch': epoch,
                    'repository': items[3],
                    'size': "".join(items[4:]),
                    'dependency': is_dependency,
                    'upgrading': upgrading
                })
                _LOG.debug("Found installed package report: %s", reported_packages[-1])
            elif lines[index_increment].startswith(('Installing dependencies:', 'Installing for dependencies:')):
                if is_dependency:
                    _LOG.warning("Dependency listing heading was already present in the output, seen again")
                is_dependency = True
            elif lines[index_increment] == '='*80:
                _LOG.debug("Found table ending, finished installed packages parsing")
                index_increment += 1
                break

            index_increment += 1

        return reported_packages, index_increment

    def run(self, input_text: str) -> list:
        """Find and parse installed packages and their versions from a build log."""
        result = []

        lines = input_text.split('\n')
        index = 0
        while index < len(lines):
            line = lines[index]
            line.strip()

            # TODO: parsing lines like '--> Processing Dependency' can result in a malformed package name
            # For example line:
            # --> Processing Dependency: perl(Pod::Escapes) >= 1.04 for package: 1:perl-Pod-Simple-3.28-4.el7.noarch
            # results in installing perl-Pod-Escapes. Do we want to parse such lines to keep pkgs with direct deps?
            if line.startswith('='*80):
                installed_packages, table_end_idx = self._parse_yum_table(lines, index)
                result.extend(installed_packages)
                index += table_end_idx or 1  # on errors move to the next line
            else:
                index += 1

        return result


HandlerBase.register(YUM)
