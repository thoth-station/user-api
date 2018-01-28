"""Parse packages installed using pip3."""

import logging
import re
import typing

import attr

from .base import HandlerBase

_RE_PACKAGE_NAME = re.compile(r'[a-zA-Z0-9_]')
_RE_COLLECTING_DEPENDENCY = re.compile(r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+)')
_RE_COLLECTING_DEPENDENCY_FROM = re.compile(r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+) '
                                            r'\(from ([a-zA-Z_\-.():/0-9>=<, ]+)\)')
_RE_COLLECTING_DEPENDENCY_REMOTE = re.compile(r'Collecting ([+a-zA-Z_\-.():/0-9>=<;,"]+) '
                                              r'from ([a-zA-Z_\-.():/0-9>=<, ]+)')
_RE_DOWNLOADING_ARTIFACT = re.compile(r'  Downloading ([+a-zA-Z_\-.:/0-9>=<;,"]+)( \(([a-zA-Z.,0-9]+)\))?')
_RE_ALREADY_SATISFIED = re.compile(r'Requirement already satisfied: ([+a-zA-Z_\-.():/0-9>=<;,"]+) in '
                                   r'([+a-zA-Z_\-.():/0-9>=<;,"]+) \(from ([a-zA-Z_\-.():/0-9>=<, ]+)\)')
_RE_ESCAPE_SEQ = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
_LOG = logging.getLogger(__name__)


@attr.s
class PIP3(HandlerBase):
    """Handle extracting packages from build logs - pip3 installer."""

    @staticmethod
    def _do_parse_package(package_specifier: str) -> typing.Tuple[str, typing.Optional[str]]:
        """Parse packages from a report line and return them in a tuple describing also version, version specifier."""
        if package_specifier.startswith('git+'):
            _LOG.warning("Detected installing a Python package from a git repository: %r", package_specifier)
            package_name = package_specifier
            version = 'master'

            # Try to find branch or commit specification.
            split_result = package_specifier.rsplit('@', maxsplit=1)
            if len(split_result) == 2:
                package_name = split_result[0]
                version = split_result[1]

            return package_name, version

        # See https://www.python.org/dev/peps/pep-0440/#version-specifiers for all possible values.
        version_start_idx = None
        for ver_spec in ('~=', '!=', '===', '==', '<=', '>=', '>', '<'):
            try:
                found_idx = package_specifier.index(ver_spec)
                if version_start_idx is None or found_idx < version_start_idx:
                    version_start_idx = found_idx
            except ValueError:
                pass

        if version_start_idx:
            return package_specifier[:version_start_idx], package_specifier[version_start_idx:]

        return package_specifier, None

    @classmethod
    def _parse_package(cls, package_specifier: str, is_from: bool = False) -> dict:
        """Parse packages and return them in a dictionary."""
        result = []
        if not is_from:
            parsed_package = cls._do_parse_package(package_specifier)
            result = {
                'package': parsed_package[0],
                'version_specified': parsed_package[1],
                'version_installed': None,
                'already_satisfied': None
            }
        else:
            for package in package_specifier.split('->'):
                parsed_package = cls._do_parse_package(package)
                result.append({
                    'package': parsed_package[0],
                    'version_specified': parsed_package[1]
                })

        return result or None

    @staticmethod
    def _check_entry(result, package_name, package_version):
        """Check parsed entries against reported installed entries by pip after successful installation."""
        matched = [entry for entry in result if entry['package'] == package_name]

        if len(matched) > 1:
            _LOG.warning('Package %r was installed multiple times in versions %s', package_name,
                         tuple(entry['version_specified'] for entry in matched))

        if not matched:
            _LOG.error('Package %r was not parsed in the output - detected installed version %r, error is not fatal',
                       package_name, package_version)

        if package_version not in (entry['version_specified'] for entry in matched):
            _LOG.debug('Installation of Python package %r using pip with version specifiers %s installed version %s',
                       package_name, [entry['version_specified'] for entry in matched], package_version)

        # Assign installed version.
        for entry in matched:
            entry['version_installed'] = package_version

    @staticmethod
    def _parse_artifact(line: str) -> typing.Optional[dict]:
        match_result = _RE_DOWNLOADING_ARTIFACT.fullmatch(line)
        if not match_result:
            _LOG.warning('Unable to parse downloaded artifact from line %r', line)
            return None

        size = match_result.group(2)
        return {
            'name': match_result.group(1),
            'size': size[2:-1] if size else None  # Omit braces and preceding space.
        }

    @staticmethod
    def _remove_escape_seq(line: str) -> str:
        """Remove escape characters that can occur on stdout (e.g. colored output)."""
        # TODO: move to some utils module
        return _RE_ESCAPE_SEQ.sub('', line)

    def run(self, input_text: str) -> list:
        """Find and parse installed packages and their versions from a build log."""
        result = []
        index = 0
        lines = input_text.split('\n')
        while index < len(lines):
            line = self._remove_escape_seq(lines[index])
            match_result = _RE_COLLECTING_DEPENDENCY_FROM.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency['from'] = self._parse_package(match_result.group(2), is_from=True)
                dependency['artifact'] = self._parse_artifact(lines[index + 1])
                result.append(dependency)
                index += 1
                continue

            match_result = _RE_COLLECTING_DEPENDENCY.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency['from'] = None
                dependency['artifact'] = self._parse_artifact(lines[index + 1])
                result.append(dependency)
                index += 1
                continue

            match_result = _RE_ALREADY_SATISFIED.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency['from'] = self._parse_package(match_result.group(3), is_from=True)
                dependency['already_satisfied'] = match_result.group(2)
                result.append(dependency)

            match_result = _RE_COLLECTING_DEPENDENCY_REMOTE.fullmatch(line)
            if match_result:
                dependency = self._parse_package(match_result.group(1))
                dependency['artifact'] = self._parse_artifact(lines[index + 1])
                # The 'from' part is not reported - it looks same as dependency['artifact']['name'].
                result.append(dependency)
                index += 1
                continue

            if line.startswith('Successfully installed '):
                packages = line[len('Successfully installed '):].split(' ')
                for package in packages:
                    package_name, version = package.rsplit('-', maxsplit=1)
                    self._check_entry(result, package_name, version)
                index += 1
                continue

            index += 1

        return result


HandlerBase.register(PIP3)
