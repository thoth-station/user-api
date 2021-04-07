#!/usr/bin/env python3
# thoth-user-api
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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

import hashlib
from itertools import islice
import logging
import typing
import json
import datetime
import time
import connexion

from thoth.storages import AdvisersResultsStore
from thoth.storages import AnalysisResultsStore
from thoth.storages import BuildLogsStore
from thoth.storages import BuildLogsAnalysesCacheStore
from thoth.storages import ProvenanceResultsStore
from thoth.storages import AnalysesCacheStore
from thoth.storages import AdvisersCacheStore
from thoth.storages import ProvenanceCacheStore
from thoth.storages import AnalysisByDigest
from thoth.storages.exceptions import CacheMiss
from thoth.storages.exceptions import NotFoundError
from thoth.common import OpenShift
from thoth.common import RuntimeEnvironment
from thoth.common.exceptions import NotFoundException as OpenShiftNotFound
from thoth.python import Project
from thoth.python.exceptions import ThothPythonException
from thoth.user_api.payload_filter import PayloadProcess

import thoth.messaging.producer as producer
from thoth.messaging import MessageBase
from thoth.messaging import AdviserTriggerMessage
from thoth.messaging import KebechetTriggerMessage
from thoth.messaging import BuildAnalysisTriggerMessage
from thoth.messaging import PackageExtractTriggerMessage
from thoth.messaging import ProvenanceCheckerTriggerMessage
from thoth.messaging import QebHwtTriggerMessage

from .configuration import Configuration
from .image import get_image_metadata
from .exceptions import ImageError
from .exceptions import ImageBadRequestError
from .exceptions import ImageManifestUnknownError
from .exceptions import ImageAuthenticationRequired
from .exceptions import ImageInvalidCredentials
from . import __version__ as SERVICE_VERSION  # noqa
from . import __name__ as COMPONENT_NAME  # noqa


PAGINATION_SIZE = 100
_LOGGER = logging.getLogger(__name__)
_OPENSHIFT = OpenShift()

_ADVISE_PROTECTED_FIELDS = frozenset(
    {
        "github_event_type",
        "github_check_run_id",
        "github_installation_id",
        "github_base_repo_url",
        "kebechet_metadata",
    }
)

_PROVENANCE_CHECK_PROTECTED_FIELDS = frozenset({"kebechet_metadata"})


p = producer.create_producer()


def _compute_digest_params(parameters: dict):
    """Compute digest on parameters passed."""
    return hashlib.sha256(json.dumps(parameters, sort_keys=True).encode()).hexdigest()


def post_analyze(
    image: str,
    debug: bool = False,
    registry_user: str = None,
    registry_password: str = None,
    environment_type: str = None,
    origin: str = None,
    verify_tls: bool = True,
    force: bool = False,
):
    """Run an analyzer in a restricted namespace."""
    parameters = locals()
    force = parameters.pop("force", None)
    # Set default environment type if none provided. As we are serving user's
    # requests, we always analyze external container images.
    parameters["environment_type"] = parameters.get("runtime_environment") or "runtime"
    parameters["is_external"] = True

    # Always extract metadata to check for authentication issues and such.
    metadata_req = _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )

    if metadata_req[1] != 200:
        # There was an error extracting metadata, tuple holds dictionary with error report and HTTP status code.
        return metadata_req

    metadata = metadata_req[0]
    # We compute digest of parameters so we do not reveal any authentication specific info.
    parameters_digest = _compute_digest_params(parameters)
    cache = AnalysesCacheStore()
    cache.connect()
    cached_document_id = metadata["digest"] + "+" + parameters_digest

    if not force:
        try:
            return (
                {
                    "analysis_id": cache.retrieve_document_record(cached_document_id).pop("analysis_id"),
                    "cached": True,
                    "parameters": parameters,
                },
                202,
            )
        except CacheMiss:
            pass

    parameters["job_id"] = _OPENSHIFT.generate_id("package-extract")
    response, status_code = _send_schedule_message(parameters, PackageExtractTriggerMessage)
    analysis_by_digest_store = AnalysisByDigest()
    analysis_by_digest_store.connect()
    analysis_by_digest_store.store_document(metadata["digest"], response)

    if status_code == 202:
        cache.store_document_record(cached_document_id, {"analysis_id": response["analysis_id"]})

        # Store the request for traceability.
        store = AnalysisResultsStore()
        store.connect()
        store.store_request(parameters["job_id"], parameters)

    return response, status_code


def post_image_metadata(
    image: str, registry_user: str = None, registry_password: str = None, verify_tls: bool = True
) -> tuple:
    """Get image metadata."""
    return _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )


def list_analyze(page: int = 0):
    """Retrieve image analyzer result."""
    return _do_listing(AnalysisResultsStore, page)


def get_analyze(analysis_id: str):
    """Retrieve image analyzer result."""
    return _get_document(
        AnalysisResultsStore,
        analysis_id,
        name_prefix="package-extract-",
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
    )


def list_s2i_python() -> typing.Dict[str, typing.List[typing.Dict[str, str]]]:
    """List all available Python s2i."""
    from .openapi_server import GRAPH

    entries = []
    for thoth_s2i_image_name, thoth_s2i_image_version in GRAPH.get_thoth_s2i_all(is_external=False):
        analyses = GRAPH.get_thoth_s2i_package_extract_analysis_document_id_all(
            thoth_s2i_image_name, thoth_s2i_image_version, is_external=False
        )

        if not analyses:
            _LOGGER.error(
                "Thoth s2i image %r in version %r was not analyzed, please schedule container image "
                "analyses to make it available to users",
                thoth_s2i_image_name,
                thoth_s2i_image_version,
            )
            continue

        entries.append(
            {
                "thoth_s2i_image_name": thoth_s2i_image_name,
                "thoth_s2i_image_version": thoth_s2i_image_version,
                "thoth_s2i": f"{thoth_s2i_image_name}:v{thoth_s2i_image_version}",
                "analysis_id": analyses[-1],  # Show only the last, the most recent, one.
            }
        )

    return {"s2i": entries}


def list_container_images(page: int = 0) -> typing.Dict[str, typing.Any]:
    """List registered container images."""
    from .openapi_server import GRAPH

    entries = []
    for item in GRAPH.get_software_environments_all(is_external=False, start_offset=page):
        if item.get("env_image_name") and item.get("env_image_tag"):
            entries.append(item)

    return {"container_images": entries, "parameters": {"page": page}}


def get_analyze_by_hash(image_hash: str):
    """Get image analysis by hash of the analyzed image."""
    parameters = locals()

    analysis_by_digest_store = AnalysisByDigest()
    analysis_by_digest_store.connect()

    try:
        analysis_info = analysis_by_digest_store.retrieve_document(image_hash)
    except NotFoundError:
        return (
            {
                "error": "No analysis was performed for image described by the given image hash",
                "parameters": parameters,
            },
            404,
        )

    return get_analyze(analysis_info["analysis_id"])


def get_analyze_log(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get image analysis log."""
    return _get_log("extract-packages", analysis_id, namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_analyze_status(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get status of an image analysis."""
    return _get_status_with_queued(
        AnalysisResultsStore, "extract-packages", analysis_id, namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )


def post_provenance_python(
    input: dict,
    debug: bool = False,
    force: bool = False,
    origin: str = None,
    token: typing.Optional[str] = None,
):
    """Check provenance for the given application stack."""
    parameters = locals()
    # Translate request body parameters.
    parameters["application_stack"] = parameters["input"].pop("application_stack", None)
    parameters["justification"] = parameters["input"].pop("justification", None)
    parameters["stack_info"] = parameters["input"].pop("stack_info", None)
    parameters["kebechet_metadata"] = parameters["input"].pop("kebechet_metadata", None)

    token = parameters.pop("token", None)

    authenticated = False
    if token is not None:
        if Configuration.API_TOKEN != token:
            return {"error": "Bad token supplied"}, 401

        authenticated = True
    else:
        for k in _PROVENANCE_CHECK_PROTECTED_FIELDS:
            if parameters[k] is not None:
                return {"error": f"Parameter {k!r} requires token to be set to perform authenticated request"}, 401

    from .openapi_server import GRAPH

    try:
        project = Project.from_strings(
            parameters["application_stack"]["requirements"], parameters["application_stack"]["requirements_lock"]
        )
    except ThothPythonException as exc:
        return {"parameters": parameters, "error": f"Invalid application stack supplied: {str(exc)}"}, 400
    except Exception:
        return {"parameters": parameters, "error": "Invalid application stack supplied"}, 400

    parameters["whitelisted_sources"] = list(GRAPH.get_python_package_index_urls_all())

    force = parameters.pop("force", False)
    if authenticated:
        cached_document_id = _compute_digest_params(
            dict(**project.to_dict(), origin=origin, whitelisted_sources=parameters["whitelisted_sources"], debug=debug)
        )
    else:
        cached_document_id = _compute_digest_params(
            dict(**project.to_dict(), whitelisted_sources=parameters["whitelisted_sources"], debug=debug)
        )

    timestamp_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    cache = ProvenanceCacheStore()
    cache.connect()

    if not force:
        try:
            cache_record = cache.retrieve_document_record(cached_document_id)
            if cache_record["timestamp"] + Configuration.THOTH_CACHE_EXPIRATION > timestamp_now:
                return {
                    "analysis_id": cache_record.pop("analysis_id"),
                    "cached": True,
                    "authenticated": authenticated,
                    "parameters": parameters,
                }, 202
        except CacheMiss:
            pass

    parameters["job_id"] = _OPENSHIFT.generate_id("provenance-checker")
    message = dict(**parameters, authenticated=authenticated)
    message.pop("application_stack")  # Passed via Ceph.
    response, status = _send_schedule_message(message, ProvenanceCheckerTriggerMessage)

    if status == 202:
        cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

        # Store the request for traceability.
        store = ProvenanceResultsStore()
        store.connect()
        store.store_request(parameters["job_id"], parameters)

    return response, status


def get_provenance_python(analysis_id: str):
    """Retrieve a provenance check result."""
    result, status_code = _get_document(
        ProvenanceResultsStore,
        analysis_id,
        name_prefix="provenance-checker-",
        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
    )
    if status_code == 200:
        # Drop any metadata associated with the request (such as origin, GitHub application info, ...)
        result["metadata"]["arguments"]["thoth-adviser"].pop("metadata", None)
    return result, status_code


def get_provenance_python_log(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get provenance-checker logs."""
    return _get_log("provenance-check", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE)


def get_provenance_python_status(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get status of a provenance check."""
    return _get_status_with_queued(
        ProvenanceResultsStore, "provenance-check", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def post_advise_python(
    input: dict,
    recommendation_type: typing.Optional[str] = None,
    count: typing.Optional[int] = None,
    limit: typing.Optional[int] = None,
    source_type: typing.Optional[str] = None,
    debug: bool = False,
    force: bool = False,
    dev: bool = False,
    origin: typing.Optional[str] = None,
    token: typing.Optional[str] = None,
    github_event_type: typing.Optional[str] = None,
    github_check_run_id: typing.Optional[int] = None,
    github_installation_id: typing.Optional[int] = None,
    github_base_repo_url: typing.Optional[str] = None,
    kebechet_metadata: typing.Optional[dict] = None,
):
    """Compute results for the given package or package stack using adviser."""
    parameters = locals()
    # Translate request body parameters.
    parameters["application_stack"] = parameters["input"].pop("application_stack", None)
    parameters["justification"] = parameters["input"].pop("justification", None)
    parameters["stack_info"] = parameters["input"].pop("stack_info", None)
    parameters["kebechet_metadata"] = parameters["input"].pop("kebechet_metadata", None)

    token = parameters.pop("token", None)

    authenticated = False
    if token is not None:
        if Configuration.API_TOKEN != token:
            return {"error": "Bad token supplied"}, 401

        authenticated = True
    else:
        for k in _ADVISE_PROTECTED_FIELDS:
            if parameters[k] is not None:
                return {"error": f"Parameter {k!r} requires token to be set to perform authenticated request"}, 401

    # Always try to parse runtime environment so that we have it available in JSON reports in a unified form.
    try:
        parameters["runtime_environment"] = RuntimeEnvironment.from_dict(
            parameters["input"].pop("runtime_environment", {})
        ).to_dict()
    except Exception as exc:
        return {"parameters": parameters, "error": f"Failed to parse runtime environment: {str(exc)}"}

    parameters["library_usage"] = parameters["input"].pop("library_usage", None)
    parameters.pop("input")
    force = parameters.pop("force", False)

    if parameters["library_usage"]:  # Sort library usage to hit cache properly.
        for key, value in (parameters["library_usage"].get("report") or {}).items():
            parameters["library_usage"]["report"][key] = sorted(value)

    try:
        project = Project.from_strings(
            parameters["application_stack"]["requirements"],
            parameters["application_stack"].get("requirements_lock"),
            runtime_environment=RuntimeEnvironment.from_dict(parameters["runtime_environment"]),
        )
    except ThothPythonException as exc:
        return {"parameters": parameters, "error": f"Invalid application stack supplied: {str(exc)}"}, 400
    except Exception:
        return {"parameters": parameters, "error": "Invalid application stack supplied"}, 400

    # We could rewrite this to a decorator and make it shared with provenance
    # checks etc, but there are small glitches why the solution would not be
    # generic enough to be used for all POST endpoints.
    adviser_cache = AdvisersCacheStore()
    adviser_cache.connect()

    timestamp_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    if authenticated:
        cached_document_id = _compute_digest_params(
            dict(
                **project.to_dict(),
                count=parameters["count"],
                limit=parameters["limit"],
                library_usage=parameters["library_usage"],
                recommendation_type=recommendation_type,
                origin=origin,
                source_type=source_type.upper() if source_type else None,
                dev=dev,
                debug=parameters["debug"],
                github_event_type=parameters["github_event_type"],
                github_check_run_id=parameters["github_check_run_id"],
                github_installation_id=parameters["github_installation_id"],
                github_base_repo_url=parameters["github_base_repo_url"],
                kebechet_metadata=parameters["kebechet_metadata"],
            )
        )
    else:
        cached_document_id = _compute_digest_params(
            dict(
                **project.to_dict(),
                count=parameters["count"],
                limit=parameters["limit"],
                library_usage=parameters["library_usage"],
                recommendation_type=recommendation_type,
                dev=dev,
                debug=parameters["debug"],
            )
        )

    if not force:
        try:
            cache_record = adviser_cache.retrieve_document_record(cached_document_id)
            if cache_record["timestamp"] + Configuration.THOTH_CACHE_EXPIRATION > timestamp_now:
                return {
                    "analysis_id": cache_record.pop("analysis_id"),
                    "cached": True,
                    "authenticated": authenticated,
                    "parameters": parameters,
                }, 202
        except CacheMiss:
            pass

    # Enum type is checked on thoth-common side to avoid serialization issue in user-api side when providing response
    parameters["source_type"] = source_type.upper() if source_type else None
    parameters["job_id"] = _OPENSHIFT.generate_id("adviser")
    # Remove data passed via Ceph.
    message = dict(**parameters, authenticated=authenticated)
    message.pop("application_stack")
    message.pop("runtime_environment")
    message.pop("library_usage")
    response, status = _send_schedule_message(message, AdviserTriggerMessage)

    if status == 202:
        adviser_cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

        # Store the request for traceability.
        store = AdvisersResultsStore()
        store.connect()
        store.store_request(parameters["job_id"], parameters)

    return response, status


def list_advise_python(page: int = 0):
    """List available runtime environments."""
    return _do_listing(AdvisersResultsStore, page)


def get_advise_python(analysis_id):
    """Retrieve the given recommendation based on its id."""
    result, status_code = _get_document(
        AdvisersResultsStore, analysis_id, name_prefix="adviser-", namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )
    if status_code == 200:
        # Drop any metadata associated with the request (such as origin, GitHub application info, ...)
        result["metadata"]["arguments"]["thoth-adviser"].pop("metadata", None)
    return result, status_code


def get_advise_python_log(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get adviser log."""
    return _get_log("advise", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE)


def _get_log(node_name: str, analysis_id: str, namespace: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get log for a node in a workflow."""
    result: typing.Dict[str, typing.Any] = {"parameters": {"analysis_id": analysis_id}}
    try:
        log = _OPENSHIFT.get_workflow_node_log(node_name, analysis_id, namespace)
    except OpenShiftNotFound as exc:
        _LOGGER.exception(f"Log for {analysis_id} were not found: {str(exc)}")
        result.update({"error": f"Log for analysis {analysis_id} was not found or it has not started yet"})
        return result, 404
    else:
        result.update({"log": log})
        return result, 200


def get_advise_python_status(analysis_id: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get status of an adviser run."""
    return _get_status_with_queued(
        AdvisersResultsStore, "advise", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def list_python_package_indexes():
    """List registered Python package indexes in the graph database."""
    from .openapi_server import GRAPH

    return {"indexes": GRAPH.get_python_package_index_all()}


def get_python_platform() -> typing.Dict[str, typing.List[str]]:
    """List available platforms for the Python ecosystem."""
    from .openapi_server import GRAPH

    return {"platform": GRAPH.get_python_package_version_platform_all()}


def list_python_package_versions(
    name: str,
    page: int = 0,
) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get information about versions available."""
    parameters = locals()

    from .openapi_server import GRAPH

    try:
        query_result = GRAPH.get_python_package_versions_all(
            package_name=name,
            distinct=True,
            is_missing=False,
            start_offset=page,
        )
    except NotFoundError:
        return {"error": f"Package {name!r} not found", "parameters": parameters}, 404

    return {"versions": [{"package_name": i[0], "package_version": i[1], "index_url": i[2]} for i in query_result]}, 200


def get_python_package_dependencies(
    name: str,
    version: str,
    index: str,
    os_name: typing.Optional[str] = None,
    os_version: typing.Optional[str] = None,
    python_version: typing.Optional[str] = None,
    marker_evaluation_result: typing.Optional[bool] = None,
) -> typing.Tuple[typing.Any, int]:
    """Get dependencies for the given Python package."""
    parameters = locals()

    from .openapi_server import GRAPH

    if (os_name is None and os_version is not None) or (os_name is not None and os_version is None):
        return {
            "error": "Operating system is not fully specified",
            "parameters": parameters,
        }, 400

    if marker_evaluation_result is not None and (os_name is None or os_version is None or python_version is None):
        return (
            {
                "error": "Operating system and Python interpreter version need "
                "to be specified to obtain dependencies dependent on marker evaluation result",
                "parameters": parameters,
            },
            400,
        )

    try:
        query_result = GRAPH.get_depends_on(
            package_name=name,
            package_version=version,
            index_url=index,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
            marker_evaluation_result=marker_evaluation_result,
        )
    except NotFoundError:
        return (
            {
                "error": f"No record found for package {name!r} in version {version!r} from "
                f"index {index!r} for {os_name!r} in version {os_version!r} using Python "
                f"version {python_version!r}",
                "parameters": parameters,
            },
            404,
        )

    result = []
    for extra, entries in query_result.items():
        for entry in entries:
            result.append(
                {
                    "name": entry[0],
                    "version": entry[1],
                    "extra": extra,
                    "environment_marker": None,
                }
            )

            if os_name is not None and os_version is not None and python_version is not None:
                try:
                    result[-1]["environment_marker"] = GRAPH.get_python_environment_marker(
                        package_name=name,
                        package_version=version,
                        index_url=index,
                        dependency_name=entry[0],
                        dependency_version=entry[1],
                        os_name=os_name,
                        os_version=os_version,
                        python_version=python_version,
                    )
                except NotFoundError:
                    return (
                        {
                            "error": f"No environment marker records found for package {name!r} in version "
                            f"{version!r} from index {index!r} with dependency "
                            f"on {entry[0]!r} in version {entry[1]!r}",
                            "parameters": parameters,
                        },
                        404,
                    )
    return {"dependencies": result, "parameters": parameters}, 200


def list_hardware_environments(page: int = 0):
    """List hardware environments in the graph database."""
    from .openapi_server import GRAPH

    return {
        "parameters": {"page": page},
        "hardware_environments": GRAPH.get_hardware_environments_all(is_external=False, start_offset=page),
    }


def post_build(
    build_detail: typing.Dict[str, typing.Any],
    *,
    base_registry_password: typing.Optional[str] = None,
    base_registry_user: typing.Optional[str] = None,
    base_registry_verify_tls: bool = True,
    output_registry_password: typing.Optional[str] = None,
    output_registry_user: typing.Optional[str] = None,
    output_registry_verify_tls: bool = True,
    debug: bool = False,
    environment_type: typing.Optional[str] = None,
    force: bool = False,
    origin: typing.Optional[str] = None,
) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Run analysis on a build."""
    output_image = build_detail.get("output_image")
    base_image = build_detail.get("base_image")
    build_log = build_detail.get("build_log")

    if not output_image and not base_image and not build_log:
        return {"error": "No base, output nor build log provided"}, 400

    buildlog_analysis_id = None
    buildlog_document_id = None
    if build_log:
        buildlog_document_id, buildlog_analysis_id = _store_build_log(build_log, force=force)

    message_parameters = {
        "base_image_analysis_id": None,  # Assigned below.
        "base_image": base_image,
        "base_registry_password": base_registry_password,
        "base_registry_user": base_registry_user,
        "base_registry_verify_tls": base_registry_verify_tls,
        "output_image_analysis_id": None,  # Assigned below.
        "output_image": output_image,
        "output_registry_password": output_registry_password,
        "output_registry_user": output_registry_user,
        "output_registry_verify_tls": output_registry_verify_tls,
        "environment_type": environment_type,
        "buildlog_document_id": buildlog_document_id,
        "buildlog_parser_id": None if buildlog_analysis_id else OpenShift.generate_id("buildlog-parser"),
        "origin": origin,
        "debug": debug,
        "job_id": OpenShift.generate_id("build-analysis"),
    }

    cache = AnalysesCacheStore()
    cache.connect()

    # Handle the base container image used during the build process.
    base_image_analysis = None
    base_image_analysis_id = None
    base_cached_document_id = None
    base_image_analysis_cached = False
    if base_image:
        base_image_info = {
            "image": base_image,
            "registry_user": base_registry_user,
            "registry_password": base_registry_password,
            "verify_tls": base_registry_verify_tls,
        }
        metadata_req = _do_get_image_metadata(**base_image_info)

        if metadata_req[1] != 200:
            # There was an error extracting metadata, tuple holds dictionary with error report and HTTP status code.
            return metadata_req

        base_image_metadata = metadata_req[0]
        # We compute digest of parameters so we do not reveal any authentication specific info.
        parameters_digest = _compute_digest_params(base_image)
        base_cached_document_id = base_image_metadata["digest"] + "+" + parameters_digest

        base_image_analysis_id = OpenShift.generate_id("package-extract")
        if not force:
            try:
                base_image_analysis_id = cache.retrieve_document_record(base_cached_document_id).pop("analysis_id")
                base_image_analysis_cached = True
            except CacheMiss:
                pass

        base_image_analysis = {
            "analysis_id": base_image_analysis_id,
            "cached": base_image_analysis_cached,
            "parameters": {
                "base_image": base_image,
                # "registry_password": base_registry_password,
                # "registry_user": base_registry_user,
                "registry_verify_tls": base_registry_verify_tls,
            },
        }

        analysis_by_digest_store = AnalysisByDigest()
        analysis_by_digest_store.connect()
        analysis_by_digest_store.store_document(base_image_metadata["digest"], base_image_analysis)

    # Handle output ("resulting") container image used during the build process.
    output_image_analysis = None
    output_image_analysis_id = None
    output_cached_document_id = None
    output_image_analysis_cached = False
    if output_image:
        output_image_info = {
            "image": output_image,
            "registry_user": output_registry_user,
            "registry_password": output_registry_password,
            "verify_tls": output_registry_verify_tls,
        }
        metadata_req = _do_get_image_metadata(**output_image_info)

        if metadata_req[1] != 200:
            # There was an error extracting metadata, tuple holds dictionary with error report and HTTP status code.
            return metadata_req

        output_image_metadata = metadata_req[0]
        # We compute digest of parameters so we do not reveal any authentication specific info.
        parameters_digest = _compute_digest_params(output_image)
        output_cached_document_id = output_image_metadata["digest"] + "+" + parameters_digest

        output_image_analysis_id = OpenShift.generate_id("package-extract")
        if not force:
            try:
                output_image_analysis_id = cache.retrieve_document_record(output_cached_document_id).pop("analysis_id")
                output_image_analysis_cached = True
            except CacheMiss:
                pass

        output_image_analysis = {
            "analysis_id": output_image_analysis_id,
            "cached": output_image_analysis_cached,
            "parameters": {
                "output_image": output_image,
                # "registry_password": output_registry_password,
                # "registry_user": output_registry_user,
                "registry_verify_tls": output_registry_verify_tls,
            },
        }

        analysis_by_digest_store = AnalysisByDigest()
        analysis_by_digest_store.connect()
        analysis_by_digest_store.store_document(output_image_metadata["digest"], output_image_analysis)

    message_parameters["base_image_analysis_id"] = base_image_analysis_id if not base_image_analysis_cached else None
    message_parameters["output_image_analysis_id"] = (
        output_image_analysis_id if not output_image_analysis_cached else None
    )

    if build_log:
        pass

    response, status = _send_schedule_message(message_parameters, BuildAnalysisTriggerMessage)
    if status != 202:
        # We do not return response directly as it holds data flattened and to make sure secrets are propagated back.
        return response, status

    # Store all the ids to caches once the message is sent so subsequent calls work as expected.

    if base_cached_document_id:
        cache.store_document_record(base_cached_document_id, {"analysis_id": base_image_analysis_id})

    if output_cached_document_id:
        cache.store_document_record(output_cached_document_id, {"analysis_id": output_image_analysis_id})

    if build_log and not buildlog_analysis_id:
        buildlogs_cache = BuildLogsAnalysesCacheStore()
        buildlogs_cache.connect()
        cached_document_id = _compute_digest_params(build_log)
        buildlogs_cache.store_document_record(
            cached_document_id, {"analysis_id": message_parameters["buildlog_parser_id"]}
        )

    if base_image_analysis or output_image_analysis:
        store = AnalysisResultsStore()
        store.connect()
        if base_image_analysis_id:
            store.store_request(base_image_analysis_id, base_image_analysis)
        if output_image_analysis:
            store.store_request(output_image_analysis_id, output_image_analysis)

    return {
        "base_image_analysis": base_image_analysis,
        "output_image_analysis": output_image_analysis,
        "buildlog_analysis": {
            "analysis_id": buildlog_analysis_id or message_parameters["buildlog_parser_id"],
            "cached": buildlog_analysis_id is not None,
        },
        "buildlog_document_id": buildlog_document_id,
    }, 202


def _store_build_log(
    build_log: typing.Dict[str, typing.Any], force: bool = False
) -> typing.Tuple[str, typing.Optional[str]]:
    """Store the given build log, use cached entry if available."""
    buildlog_analysis_id = None
    if not force:
        cache = BuildLogsAnalysesCacheStore()
        cache.connect()
        cached_document_id = _compute_digest_params(build_log)

        try:
            cache_record = cache.retrieve_document_record(cached_document_id)
            buildlog_analysis_id = cache_record.pop("analysis_id")
        except CacheMiss:
            pass

    adapter = BuildLogsStore()
    adapter.connect()
    document_id = adapter.store_document(build_log)
    return document_id, buildlog_analysis_id


def get_buildlog(document_id: str):
    """Retrieve the given buildlog."""
    return _get_document(BuildLogsStore, document_id)


def schedule_kebechet_webhook(body: typing.Dict[str, typing.Any]):
    """Schedule Kebechet run-webhook on Openshift using Argo Workflow."""
    payload, webhook_payload = {}, {}
    headers = connexion.request.headers

    if "X-GitHub-Event" in headers:
        webhook_payload["event"] = headers["X-GitHub-Event"]
        webhook_payload["payload"] = body
        webhook_payload["service"] = "github"
    elif "X_GitLab_Event" in headers:
        webhook_payload["event"] = headers["X_GitLab_Event"]
        webhook_payload["payload"] = body
        webhook_payload["service"] = "gitlab"
    elif "X_Pagure_Topic" in headers:
        return {"error": "Pagure is currently not supported"}, 501
    else:
        return {"error": "This webhook is not supported"}, 501

    # Handle installation events and check if webhooks are relevant to Kebechet.
    preprocess_payload = PayloadProcess().process(webhook_payload=webhook_payload)
    # Not schedule workload if pre-processed payload is None.
    if preprocess_payload is None:
        return

    payload["webhook_payload"] = webhook_payload
    payload["job_id"] = _OPENSHIFT.generate_id("kebechet-job")  # type: ignore
    return _send_schedule_message(payload, KebechetTriggerMessage)


def schedule_qebhwt_advise(
    input: typing.Dict[str, typing.Any],
):
    """Schedule Thamos Advise for GitHub App."""
    input["host"] = Configuration.THOTH_HOST
    input["job_id"] = _OPENSHIFT.generate_id("qeb-hwt")
    return _send_schedule_message(input, QebHwtTriggerMessage)


def list_buildlogs(page: int = 0):
    """List available build logs."""
    return _do_listing(BuildLogsStore, page)


def get_package_metadata(name: str, version: str, index: str):
    """Retrieve metadata for the given package version."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        return {
            "metadata": GRAPH.get_python_package_version_metadata(
                package_name=name, package_version=version, index_url=index
            ),
            "parameters": parameters,
        }
    except NotFoundError:
        return (
            {
                "error": f"No metadata records for package {name!r} in version {version!r} from index {index!r} found",
                "parameters": parameters,
            },
            404,
        )


def _do_listing(adapter_class, page: int) -> tuple:
    """Perform actual listing of documents available."""
    adapter = adapter_class()
    adapter.connect()
    result = adapter.get_document_listing()
    # TODO: make sure if Ceph returns objects in the same order each time.
    # We will need to abandon this logic later anyway once we will be
    # able to query results on data hub side.
    results = list(islice(result, page * PAGINATION_SIZE, page * PAGINATION_SIZE + PAGINATION_SIZE))
    return (
        {"results": results, "parameters": {"page": page}},
        200,
        {"page": page, "page_size": PAGINATION_SIZE, "results_count": len(results)},
    )


def _construct_status_queued(analysis_id: str) -> typing.Dict[str, typing.Any]:
    """Construct a response for a queued analysis."""
    status = {"finished_at": None, "reason": None, "started_at": None, "state": "pending"}
    return {
        "error": f"Analysis {analysis_id!r} is being queued and scheduled for processing",
        "status": status,
        "parameters": {"analysis_id": analysis_id},
    }


def _get_document(adapter_class, analysis_id: str, name_prefix: str = None, namespace: str = None) -> tuple:
    """Perform actual document retrieval."""
    # Parameters to be reported back to a user of API.
    parameters = {"analysis_id": analysis_id}
    if name_prefix and not analysis_id.startswith(name_prefix):
        return {"error": "Wrong analysis id provided", "parameters": parameters}, 400

    adapter = adapter_class()
    adapter.connect()

    try:
        result = adapter.retrieve_document(analysis_id)
        return result, 200
    except NotFoundError:
        if namespace:
            try:
                status = _OPENSHIFT.get_workflow_status_report(analysis_id, namespace=namespace)
                if status["state"] == "running":
                    return {"error": "Analysis is still in progress", "status": status, "parameters": parameters}, 202
                elif status["state"] in ("failed", "error"):
                    return {"error": "Analysis was not successful", "status": status, "parameters": parameters}, 400
                elif status["state"] == "pending":
                    return {"error": "Analysis is being scheduled", "status": status, "parameters": parameters}, 202
                else:
                    # Can be:
                    #   - return 500 to user as this is our issue
                    raise ValueError(f"Unreachable - unknown workflow state: {status}")
            except OpenShiftNotFound:
                if adapter.request_exists(analysis_id):
                    return _construct_status_queued(analysis_id), 202

        return {"error": f"Requested result for analysis {analysis_id!r} was not found", "parameters": parameters}, 404


def _get_status(node_name: str, analysis_id: str, namespace: str) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
    """Get status for a node in a workflow."""
    result: typing.Dict[str, typing.Any] = {"parameters": {"analysis_id": analysis_id}}
    try:
        status = _OPENSHIFT.get_workflow_node_status(node_name, analysis_id, namespace)
    except OpenShiftNotFound:
        result.update({"error": f"Status for analysis {analysis_id} was not found or it has not started yet"})
        return result, 404
    else:
        result.update({"status": status})
        return result, 200


def _get_status_with_queued(
    adapter: typing.Union[AdvisersResultsStore, ProvenanceResultsStore, AnalysisResultsStore],
    node_name: str,
    analysis_id: str,
    namespace: str,
) -> typing.Tuple[typing.Dict[str, typing.Any,], int]:
    """Get status of an analysis, check queued requests as well."""
    result, status_code = _get_status(node_name=node_name, analysis_id=analysis_id, namespace=namespace)
    if status_code == 404:
        adapter_instance = adapter()
        adapter_instance.connect()
        if adapter_instance.request_exists(analysis_id):
            return _construct_status_queued(analysis_id), 200
    return result, status_code


def _send_schedule_message(message_contents: dict, message_type: MessageBase):
    message_contents["service_version"] = SERVICE_VERSION
    message_contents["component_name"] = COMPONENT_NAME
    message = message_type.MessageContents(**message_contents)
    producer.publish_to_topic(p, message_type(), message)
    if "job_id" in message_contents:
        return (
            {
                "analysis_id": message_contents["job_id"],
                "parameters": message_contents,
                "cached": False,
            },
            202,
        )

    raise ValueError(f"job_id was not set for message sent to {message_type().topic_name}")


def _do_get_image_metadata(
    image: str, registry_user: str = None, registry_password: str = None, verify_tls: bool = True
) -> typing.Tuple[dict, int]:
    """Wrap function call with additional checks."""
    try:
        return (
            get_image_metadata(
                image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
            ),
            200,
        )
    except ImageBadRequestError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageInvalidCredentials as exc:
        status_code = 403
        error_str = str(exc)
    except ImageManifestUnknownError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageAuthenticationRequired as exc:
        status_code = 401
        error_str = str(exc)
    except ImageError as exc:
        status_code = 400
        error_str = str(exc)

    return {"error": error_str, "parameters": locals()}, status_code
