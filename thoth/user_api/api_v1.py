#!/usr/bin/env python3
# thoth-user-api
# Copyright(C) 2018 - 2021 Fridolin Pokorny
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

import connexion
import datetime
import hashlib
import json
import logging
import os
import time
from urllib import parse as url_parse
from math import ceil
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
import random
import string
import base64

from flask import request
from kubernetes import kubernetes as k8
import requests

from thoth.common.exceptions import NotFoundExceptionError as OpenShiftNotFound
from thoth.common import OpenShift
from thoth.common import RuntimeEnvironment
from thoth.common import map_os_name
from thoth.common import normalize_os_version
from thoth.python.exceptions import ThothPythonExceptionError
from thoth.python import Constraints
from thoth.python import Project
from thoth.python import PackageVersion
from thoth.storages.exceptions import CacheMiss
from thoth.storages.exceptions import NotFoundError
from thoth.storages import AdvisersCacheStore
from thoth.storages import AdvisersResultsStore
from thoth.storages import AnalysesCacheStore
from thoth.storages import AnalysisByDigest
from thoth.storages import AnalysisResultsStore
from thoth.storages import BuildLogsAnalysesCacheStore
from thoth.storages import BuildLogsStore
from thoth.storages import ProvenanceCacheStore
from thoth.storages import ProvenanceResultsStore
from thoth.storages import WorkflowLogsStore
from thoth.storages import SolverResultsStore
from thoth.user_api.payload_filter import PayloadProcess

import thoth.messaging.producer as producer
from thoth.messaging import MessageBase
from thoth.messaging import BaseMessageContents
from thoth.messaging import (
    adviser_trigger_message,
    kebechet_trigger_message,
    build_analysis_trigger_message,
    package_extract_trigger_message,
    provenance_checker_trigger_message,
    thoth_repo_init_message,
)
from thoth.messaging.adviser_trigger import MessageContents as AdviserTriggerContent
from thoth.messaging.kebechet_trigger import MessageContents as KebechetTriggerContent
from thoth.messaging.build_analysis_trigger import MessageContents as BuildAnalysisTriggerContent
from thoth.messaging.package_extract_trigger import MessageContents as PackageExtractTriggerContent
from thoth.messaging.provenance_checker_trigger import MessageContents as ProvenanceCheckerTriggerContent
from thoth.messaging.thoth_repo_init import MessageContents as ThothRepoInitContent

from .configuration import Configuration
from .image import get_image_metadata
from .exceptions import ImageError
from .exceptions import ImageBadRequestError
from .exceptions import ImageManifestUnknownError
from .exceptions import ImageAuthenticationRequiredError
from .exceptions import ImageInvalidCredentialsError
from . import __version__ as SERVICE_VERSION  # noqa
from . import __name__ as COMPONENT_NAME  # noqa


PAGINATION_SIZE_MAX = int(os.getenv("THOTH_USER_API_PAGE_SIZE_MAX", 100))
PAGINATION_SIZE_DEFAULT = int(os.getenv("THOTH_USER_API_PAGE_SIZE_DEFAULT", 25))

_LOGGER = logging.getLogger(__name__)
_OPENSHIFT = OpenShift()

_ADVISE_PROTECTED_FIELDS = frozenset(
    {
        "kebechet_metadata",
    }
)

_PROVENANCE_CHECK_PROTECTED_FIELDS = frozenset({"kebechet_metadata"})

k8.config.load_kube_config()
k8_core_api = k8.client.CoreV1Api()
CALLBACK_SECRET_NAME_TEMPLATE = "callback-{document_id}"


def _add_entry_or_create_callback_secret(
    document_id: str, callbackurl: str, auth_header: Optional[str] = None, client_data: Optional[dict] = None
):
    if _callback_secret_exists(document_id=document_id):
        _add_item_to_callback_secret_entry(
            document_id=document_id,
            callbackurl=callbackurl,
            auth_header=auth_header,
            client_data=client_data,
        )
    else:
        _create_initial_callback_secret(
            document_id=document_id,
            callbackurl=callbackurl,
            auth_header=auth_header,
            client_data=client_data,
        )


def _add_item_to_callback_secret_entry(
    document_id: str, callbackurl: str, auth_header: Optional[str] = None, client_data: Optional[dict] = None
):
    entry_name, value = _gen_callback_secret_entry(callbackurl, auth_header, client_data)
    body = [{"op": "add", "path": f"/data/{entry_name}", "value": value}]
    k8_core_api.patch_namespaced_secret(
        name=CALLBACK_SECRET_NAME_TEMPLATE.format(document_id=document_id),
        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
        body=body,
    )


def _callback_secret_exists(document_id):
    try:
        k8_core_api.read_namespaced_secret(
            name=CALLBACK_SECRET_NAME_TEMPLATE.format(document_id=document_id),
            namespace=Configuration.THOTH_BACKEND_NAMESPACE,
        )
    except k8.client.rest.ApiException as e:
        if e.status == 404:
            return False
        raise e  # all other status are reraised
    return True


def _gen_callback_secret_entry(callbackurl, auth_header, client_data):
    value = base64.b64encode(
        json.dumps({"callbackurl": callbackurl, "Authorization": auth_header, "client_data": client_data}).encode(
            "ascii"
        )
    )
    value = str(value, "ascii")
    entry_name = "".join(random.choices(string.ascii_letters, k=16))
    return entry_name, value


def _create_initial_callback_secret(document_id, callbackurl, auth_header, client_data):
    meta = k8.client.V1ObjectMeta(
        name=CALLBACK_SECRET_NAME_TEMPLATE.format(document_id=document_id),
    )
    entry_name, value = _gen_callback_secret_entry(
        callbackurl=callbackurl, auth_header=auth_header, client_data=client_data
    )
    k8_core_api.create_namespaced_secret(
        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
        body=k8.client.V1Secret(
            api_version="v1",
            data={entry_name: value},
            type="Opaque",
            metadata=meta,
        ),
    )


def _compute_digest_params(parameters: Dict[Any, Any]) -> str:
    """Compute digest on parameters passed."""
    return hashlib.sha256(json.dumps(parameters, sort_keys=True).encode()).hexdigest()


def _compute_prev_next_page(page: int, page_count: int) -> Tuple[Optional[str], Optional[str]]:
    """Compute next and prev returned in headers for paginated endpoints."""
    next_page, prev_page = None, None
    if page != 0:
        prev_parameters: Dict[str, Any] = dict(request.args)
        prev_parameters["page"] = min(page - 1, page_count - 1)
        prev_page = f"{request.path}?{url_parse.urlencode(prev_parameters)}"
    if page < page_count - 1:
        next_parameters: Dict[str, Any] = dict(request.args)
        next_parameters["page"] = min(page + 1, page_count - 1)
        next_page = f"{request.path}?{url_parse.urlencode(next_parameters)}"

    return prev_page, next_page


def _compute_offset(*, page: int, page_count: int, per_page: int) -> int:
    """Compute offset respecting negative indexing."""
    if page_count == 0:
        return 0

    if page < 0:
        page = (-page - 1) % page_count
        return (page_count - page - 1) * per_page
    else:
        return page * per_page


def post_analyze(
    image: str,
    debug: bool = False,
    registry_user: Optional[str] = None,
    registry_password: Optional[str] = None,
    environment_type: Optional[str] = None,
    origin: Optional[str] = None,
    verify_tls: bool = True,
    force: bool = False,
) -> Tuple[Dict[str, Any], int]:
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
    response, status_code = _send_schedule_message(
        parameters, package_extract_trigger_message, PackageExtractTriggerContent
    )
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
    image: str, registry_user: Optional[str] = None, registry_password: Optional[str] = None, verify_tls: bool = True
) -> Tuple[Dict[str, Any], int]:
    """Get image metadata."""
    return _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )


def get_analyze(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Retrieve image analyzer result."""
    return _get_document(
        AnalysisResultsStore,
        analysis_id,
        name_prefix="package-extract-",
        namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE,
    )


def list_thoth_container_images(
    page: int = 0,
    per_page: int = PAGINATION_SIZE_DEFAULT,
    os_name: Optional[str] = None,
    os_version: Optional[str] = None,
    python_version: Optional[str] = None,
    cuda_version: Optional[str] = None,
    image_name: Optional[str] = None,
    library_name: Optional[str] = None,
    symbol: Optional[str] = None,
    package_name: Optional[str] = None,
    rpm_package_name: Optional[str] = None,
) -> Tuple[Dict[str, Any], int, Dict[str, Any]]:
    """List registered Thoth container images."""
    per_page = min(per_page, PAGINATION_SIZE_MAX)
    parameters = locals()

    from .openapi_server import GRAPH

    entries_count = GRAPH.get_software_environments_count_all(
        is_external=False,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
        cuda_version=cuda_version,
        image_name=image_name,
        library_name=library_name,
        symbol=symbol,
        package_name=package_name,
        rpm_package_name=rpm_package_name,
    )

    page_count = ceil(entries_count / per_page)
    start_offset = _compute_offset(page=page, page_count=page_count, per_page=per_page)

    entries = []
    for item in GRAPH.get_software_environments_all(
        is_external=False,
        start_offset=start_offset,
        count=per_page,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
        cuda_version=cuda_version,
        image_name=image_name,
        library_name=library_name,
        symbol=symbol,
        package_name=package_name,
        rpm_package_name=rpm_package_name,
    ):
        if item.get("env_image_name") and item.get("env_image_tag"):
            item["thoth_image_name"] = item.pop("env_image_name", None)
            item["thoth_image_version"] = item.pop("env_image_tag", None)
        else:
            item["thoth_image_name"] = item.pop("thoth_s2i_image_name", None)
            item["thoth_image_version"] = item.pop("thoth_s2i_image_version", None)

        if item.get("environment_name") and item["environment_name"].startswith("quay.io"):
            item["quay_repo_url"] = "https://%s" % item.get("environment_name")
        else:
            item["quay_repo_url"] = None

        if item.get("package_extract_document_id"):
            item["image_analysis_url"] = f"{request.script_root}/analyze/{item.get('package_extract_document_id')}"
        else:
            item["image_analysis_url"] = None

        entries.append(item)

    prev_page, next_page = _compute_prev_next_page(page, per_page)
    return (
        {
            "container_images": entries,
            "parameters": parameters,
        },
        200,
        {
            "page": page,
            "per_page": per_page,
            "page_count": page_count,
            "entries_count": entries_count,
            "next": next_page,
            "prev": prev_page,
        },
    )


def get_analyze_by_hash(image_hash: str) -> Tuple[Dict[str, Any], int]:
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


def get_analyze_log(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get image analysis log."""
    return _get_log("extract-packages", analysis_id, namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_analyze_status(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get status of an image analysis."""
    return _get_status_with_queued(
        AnalysisResultsStore, "extract-packages", analysis_id, namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE
    )


def post_provenance_python(
    input: Dict[str, Any],
    debug: bool = False,
    force: bool = False,
    origin: Optional[str] = None,
    token: Optional[str] = None,
) -> Tuple[Dict[str, Any], int]:
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
    except ThothPythonExceptionError as exc:
        return {"parameters": parameters, "error": f"Invalid application stack supplied: {str(exc)}"}, 400
    except Exception:
        return {"parameters": parameters, "error": "Invalid application stack supplied"}, 400

    parameters["whitelisted_sources"] = list(GRAPH.get_python_package_index_urls_all())

    parameters.pop("input")
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
                return (
                    {
                        "analysis_id": cache_record.pop("analysis_id"),
                        "cached": True,
                        "authenticated": authenticated,
                        "parameters": parameters,
                    },
                    202,
                )
        except CacheMiss:
            pass

    parameters["job_id"] = _OPENSHIFT.generate_id("provenance-checker")
    message = dict(**parameters, authenticated=authenticated)
    message.pop("application_stack")  # Passed via Ceph.
    response, status = _send_schedule_message(
        message,
        provenance_checker_trigger_message,
        ProvenanceCheckerTriggerContent,
        with_authentication=True,
        authenticated=authenticated,
    )

    if status == 202:
        cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

        # Store the request for traceability.
        store = ProvenanceResultsStore()
        store.connect()
        store.store_request(parameters["job_id"], parameters)

    return response, status


def get_provenance_python(analysis_id: str) -> Tuple[Dict[str, Any], int]:
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


def get_provenance_python_log(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get provenance-checker logs."""
    return _get_log("provenance-check", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE)


def get_provenance_python_status(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get status of a provenance check."""
    return _get_status_with_queued(
        ProvenanceResultsStore, "provenance-check", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def post_advise_python(
    input: Dict[str, Any],
    recommendation_type: Optional[str] = None,
    source_type: Optional[str] = None,
    debug: bool = False,
    force: bool = False,
    dev: bool = False,
    origin: Optional[str] = None,
    token: Optional[str] = None,
) -> Tuple[Dict[str, Any], int]:
    """Compute results for the given package or package stack using adviser."""
    parameters = locals()
    # Translate request body parameters.
    parameters["application_stack"] = parameters["input"].pop("application_stack", None)
    parameters["justification"] = parameters["input"].pop("justification", None)
    parameters["stack_info"] = parameters["input"].pop("stack_info", None)
    parameters["kebechet_metadata"] = parameters["input"].pop("kebechet_metadata", None)
    parameters["labels"] = parameters["input"].pop("labels", None)
    parameters["callback_info"] = parameters["input"].pop("callback_info", None)

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
        return {"parameters": parameters, "error": f"Failed to parse runtime environment: {str(exc)}"}, 400

    try:
        constraints = Constraints.from_string(parameters["input"].pop("constraints", None) or "")
    except Exception as exc:
        return {"parameters": parameters, "error": f"Invalid constraints supplied: {str(exc)}"}, 400

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
            constraints=constraints,
        )
    except ThothPythonExceptionError as exc:
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
                library_usage=parameters["library_usage"],
                recommendation_type=recommendation_type,
                origin=origin,
                source_type=source_type.upper() if source_type else None,
                dev=dev,
                debug=parameters["debug"],
                kebechet_metadata=parameters["kebechet_metadata"],
                labels=parameters["labels"],
            )
        )
    else:
        cached_document_id = _compute_digest_params(
            dict(
                **project.to_dict(),
                library_usage=parameters["library_usage"],
                recommendation_type=recommendation_type,
                dev=dev,
                debug=parameters["debug"],
                labels=parameters["labels"],
            )
        )

    if not force:
        try:
            cache_record = adviser_cache.retrieve_document_record(cached_document_id)
            if cache_record["timestamp"] + Configuration.THOTH_CACHE_EXPIRATION > timestamp_now:
                if parameters["callback_info"]:
                    result, status_code = _get_document(
                        AdvisersResultsStore,
                        cache_record["analysis_id"],
                        name_prefix="adviser-",
                        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
                    )
                    if status_code == 202:  # workflow scheduled/in progress
                        _add_entry_or_create_callback_secret(
                            document_id=cache_record["analysis_id"],
                            callbackurl=parameters["callback_info"]["url"],
                            auth_header=parameters["callback_info"].get("authorization"),
                            client_data=parameters["callback_info"].get("client_data"),
                        )
                    else:
                        if status_code == 200:
                            result["metadata"]["arguments"]["thoth-adviser"].pop("metadata", None)  # rmv sensitive data
                        body = {"result": result, "client_data": parameters["callback_info"].get("client_data")}
                        headers = dict()
                        if auth := parameters["callback_info"].get("authorization"):
                            headers["Authorization"] = auth
                        requests.post(url=parameters["callback_info"]["url"], data=body, headers=headers)
                return (
                    {
                        "analysis_id": cache_record.pop("analysis_id"),
                        "cached": True,
                        "authenticated": authenticated,
                        "parameters": parameters,
                    },
                    202,
                )

        except CacheMiss:
            pass

    # Enum type is checked on thoth-common side to avoid serialization issue in user-api side when providing response
    parameters["source_type"] = source_type.upper() if source_type else None
    parameters["constraints"] = constraints.to_dict()
    parameters["job_id"] = _OPENSHIFT.generate_id("adviser")
    # Remove data passed via Ceph.
    message = dict(**parameters, authenticated=authenticated)
    message.pop("application_stack")
    message.pop("runtime_environment")
    message.pop("library_usage")
    message.pop("labels")
    message.pop("constraints")
    response, status = _send_schedule_message(
        message, adviser_trigger_message, AdviserTriggerContent, with_authentication=True, authenticated=authenticated
    )

    if status == 202:
        adviser_cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

        if parameters["callback_info"]:
            _create_initial_callback_secret(
                document_id=response["analysis_id"],
                callbackurl=parameters["callback_info"]["url"],
                auth_header=parameters["callback_info"].get("authorization"),
                client_data=parameters["callback_info"].get("client_data"),
            )

        # Store the request for traceability.
        store = AdvisersResultsStore()
        store.connect()
        store.store_request(parameters["job_id"], parameters)

    return response, status


def get_advise_python(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Retrieve the given recommendation based on its id."""
    result, status_code = _get_document(
        AdvisersResultsStore, analysis_id, name_prefix="adviser-", namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )
    if status_code == 200:
        # Drop any metadata associated with the request (such as origin, GitHub application info, ...)
        result["metadata"]["arguments"]["thoth-adviser"].pop("metadata", None)
    return result, status_code


def get_advise_python_log(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get adviser log."""
    return _get_log("advise", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE)


def _get_log(node_name: str, analysis_id: str, namespace: str) -> Tuple[Dict[str, Any], int]:
    """Get log for a node in a workflow."""
    result: Dict[str, Any] = {"parameters": {"analysis_id": analysis_id}}
    try:
        log = _OPENSHIFT.get_workflow_node_log(node_name, analysis_id, namespace)
    except OpenShiftNotFound:
        logs = WorkflowLogsStore()
        logs.connect()
        try:
            log = logs.get_log(analysis_id)
        except NotFoundError:
            result.update({"error": f"Log for analysis {analysis_id} was not found or it has not started yet"})
            return result, 404
        else:
            result.update({"log": log})
            return result, 200
    else:
        result.update({"log": log})
        return result, 200


def get_advise_python_status(analysis_id: str) -> Tuple[Dict[str, Any], int]:
    """Get status of an adviser run."""
    return _get_status_with_queued(
        AdvisersResultsStore, "advise", analysis_id, namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def list_python_package_indexes() -> Tuple[Dict[str, Any], int]:
    """List registered Python package indexes in the graph database."""
    from .openapi_server import GRAPH

    return {"indexes": GRAPH.get_python_package_index_all()}, 200


def get_python_platform() -> Tuple[Dict[str, List[str]], int]:
    """List available platforms for the Python ecosystem."""
    from .openapi_server import GRAPH

    return {"platform": GRAPH.get_python_package_version_platform_all()}, 200


def list_python_packages(
    page: int = 0,
    per_page: int = PAGINATION_SIZE_DEFAULT,
    os_name: Optional[str] = None,
    os_version: Optional[str] = None,
    python_version: Optional[str] = None,
    like: Optional[str] = None,
) -> Tuple[Dict[str, Any], int, Dict[str, Any]]:
    """Get listing of solved package names."""
    per_page = min(per_page, PAGINATION_SIZE_MAX)
    parameters = locals()

    from .openapi_server import GRAPH

    entries_count = GRAPH.get_python_package_version_names_count_all(
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
        distinct=True,
        like=like,
    )

    page_count = ceil(entries_count / per_page)
    start_offset = _compute_offset(page=page, page_count=page_count, per_page=per_page)

    query_result = GRAPH.get_python_package_version_names_all(
        sort=True,
        distinct=True,
        start_offset=start_offset,
        count=per_page,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
        like=like,
    )

    prev_page, next_page = _compute_prev_next_page(page, page_count)
    return (
        {"packages": [{"package_name": i} for i in query_result], "parameters": parameters},
        200,
        {
            "page": page,
            "per_page": per_page,
            "page_count": page_count,
            "entries_count": entries_count,
            "next": next_page,
            "prev": prev_page,
        },
    )


def list_python_package_versions(
    name: str,
    order_by: Optional[str] = None,
    os_name: Optional[str] = None,
    os_version: Optional[str] = None,
    python_version: Optional[str] = None,
) -> Tuple[Dict[str, Any], int]:
    """Get information about versions available."""
    parameters = locals()

    from .openapi_server import GRAPH

    entries_count = GRAPH.get_solved_python_package_versions_count_all(
        package_name=name,
        distinct=True,
        is_missing=False,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
    )

    if entries_count == 0:
        return {"error": f"Package {name!r} not found", "parameters": parameters}, 404

    query_result = GRAPH.get_solved_python_package_versions_all(
        package_name=name,
        distinct=True,
        is_missing=False,
        start_offset=0,
        count=None,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
    )

    if order_by and order_by in ["ASC", "DESC"]:
        query_result.sort(key=lambda x: PackageVersion.parse_semantic_version(x[1]), reverse=order_by == "DESC")

    return (
        {
            "versions": [{"package_name": i[0], "package_version": i[1], "index_url": i[2]} for i in query_result],
            "parameters": parameters,
        },
        200,
    )


def list_python_package_version_environments(
    name: str,
    version: str,
    index: str,
) -> Tuple[Dict[str, Any], int]:
    """List environments for which the given package was solved."""
    parameters = locals()

    from .openapi_server import GRAPH

    query_result = GRAPH.get_solved_python_package_version_environments_all(
        name,
        version,
        index,
        start_offset=0,
        count=None,  # The number of results queried will be low.
        distinct=True,
    )

    return {"environments": query_result}, 200


def get_python_package_dependencies(
    name: str,
    version: str,
    index: str,
    os_name: Optional[str] = None,
    os_version: Optional[str] = None,
    python_version: Optional[str] = None,
    marker_evaluation_result: Optional[bool] = None,
) -> Tuple[Dict[str, Any], int]:
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


def post_build(
    build_detail: Dict[str, Any],
    *,
    base_registry_password: Optional[str] = None,
    base_registry_user: Optional[str] = None,
    base_registry_verify_tls: bool = True,
    output_registry_password: Optional[str] = None,
    output_registry_user: Optional[str] = None,
    output_registry_verify_tls: bool = True,
    debug: bool = False,
    environment_type: Optional[str] = None,
    force: bool = False,
    origin: Optional[str] = None,
) -> Tuple[Dict[str, Any], int]:
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

    response, status = _send_schedule_message(
        message_parameters, build_analysis_trigger_message, BuildAnalysisTriggerContent
    )
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

    return (
        {
            "base_image_analysis": base_image_analysis,
            "output_image_analysis": output_image_analysis,
            "buildlog_analysis": {
                "analysis_id": buildlog_analysis_id or message_parameters["buildlog_parser_id"],
                "cached": buildlog_analysis_id is not None,
            },
            "buildlog_document_id": buildlog_document_id,
        },
        202,
    )


def _store_build_log(build_log: Dict[str, Any], force: bool = False) -> Tuple[str, Optional[str]]:
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


def get_buildlog(document_id: str) -> Tuple[Dict[str, Any], int]:
    """Retrieve the given buildlog."""
    return _get_document(BuildLogsStore, document_id)


def schedule_kebechet_webhook(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
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
        # No action made - eg. ignored payload or invalid payload.
        return {}, 200

    payload["webhook_payload"] = webhook_payload
    payload["job_id"] = _OPENSHIFT.generate_id("kebechet-job")  # type: ignore
    return _send_schedule_message(payload, kebechet_trigger_message, KebechetTriggerContent)


def initialize_repo(body: Dict[str, str]):
    """Schedule thoth init repo workflow, which creates a PR on the passed repository."""
    valid_github_domains = ["github.com", "www.github.com"]
    project_url = body["project_url"].strip("/")  # remove trailing f-slash if present
    try:
        url_obj = url_parse.urlparse(project_url)
    except ValueError:
        return {"error": "Error processing project_url"}, 400
    if len(url_obj.path[1:].split("/")) != 2:
        return {"error": "project_url path does not have a length of 2"}, 400
    elif url_obj.netloc not in valid_github_domains:
        return {"error": "project url is not from github.com"}, 400

    message_parameters = {
        "project_url": project_url,
        "job_id": _OPENSHIFT.generate_id("thoth-repo-init"),
    }

    return _send_schedule_message(message_parameters, thoth_repo_init_message, ThothRepoInitContent)


def get_python_package_version_metadata(
    name: str, version: str, index: str, os_name: str, os_version: str, python_version: str
) -> Tuple[Dict[str, Any], int]:
    """Obtain metadata for the given package."""
    name = PackageVersion.normalize_python_package_name(name)
    version = PackageVersion.normalize_python_package_version(version)
    os_name = map_os_name(os_name) or os_name  # "or" to keep typing happy
    os_version = normalize_os_version(os_name, os_version) or os_version  # "or" to keep typing happy

    parameters = locals()
    from .openapi_server import GRAPH

    solver_documents = GRAPH.get_solver_document_id_all(
        name, version, index, os_name=os_name, os_version=os_version, python_version=python_version, sort=True
    )
    if not solver_documents:
        return {"parameters": parameters, "error": "No records found for the given request"}, 404

    solver_store = SolverResultsStore()
    solver_store.connect()
    try:
        solver_document = solver_store.retrieve_document(solver_documents[0])
    except NotFoundError:
        return {
            "parameters": parameters,
            "error": "Solver document not found - solver documents are not in sync with database records, "
            f"please contact administrator with the provided information: {solver_documents[0]}",
        }, 500

    solver_name = "-".join(solver_document["metadata"]["document_id"].split("-")[:4])
    solver = OpenShift.parse_python_solver_name(solver_name)

    for solver_entry in solver_document["result"]["tree"]:
        if (
            PackageVersion.normalize_python_package_name(solver_entry["package_name"]) == name
            and solver_entry["package_version"] == version
            and solver_entry["index_url"] == index
        ):
            break
    else:
        # This should not happen as data synced to the database should be based on the solver document content.
        _LOGGER.error(
            "Solver document %r has no records for %r in version %r from %r",
            solver_documents[0],
            name,
            version,
            index,
        )
        return {
            "parameters": parameters,
            "error": "Solver documents are not in sync with database records, please contact administrator "
            f"with the provided information: {solver_documents[0]}",
        }, 500

    package_name = solver_entry["package_name"]
    package_version = solver_entry["package_version"]
    index_url = solver_entry["index_url"]

    deps = {}
    for dependency_entry in solver_entry["dependencies"]:
        dependency_name = dependency_entry.pop("normalized_package_name")
        dependency_entry.pop("package_name", None)
        dependency_entry.pop("resolved_versions", None)

        dependency_entry["versions"] = []
        deps[dependency_name] = dependency_entry

    dependency_info = GRAPH.get_depends_on(
        name,
        version,
        index,
        os_name=solver["os_name"],
        os_version=solver["os_version"],
        python_version=solver["python_version"],
        extras=None,
        marker_evaluation_result=None,
        is_missing=None,
    )

    for extra, dependencies in dependency_info.items():
        for dependency_name, dependency_version in dependencies:
            deps[dependency_name].setdefault("versions", []).append(dependency_version)

    for dependency_info in deps.values():
        dependency_info["versions"].sort(key=lambda v: PackageVersion.parse_semantic_version(v), reverse=False)

    solver_entry["dependencies"] = deps

    # Remove entries that should not be exposed.
    solver_entry.pop("package_version_requested", None)
    solver_entry.pop("sha256", None)

    return {"metadata": solver_entry, "parameters": parameters}, 200


def _construct_status_queued(analysis_id: str) -> Dict[str, Any]:
    """Construct a response for a queued analysis."""
    status = {"finished_at": None, "reason": None, "started_at": None, "state": "pending"}
    return {
        "error": f"Analysis {analysis_id!r} is being queued and scheduled for processing",
        "status": status,
        "parameters": {"analysis_id": analysis_id},
    }


def _get_document(
    adapter_class, analysis_id: str, name_prefix: Optional[str] = None, namespace: Optional[str] = None
) -> Tuple[Dict[str, Any], int]:
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


def _get_status(node_name: str, analysis_id: str, namespace: str) -> Tuple[Dict[str, Any], int]:
    """Get status for a node in a workflow."""
    result: Dict[str, Any] = {"parameters": {"analysis_id": analysis_id}}
    try:
        status = _OPENSHIFT.get_workflow_node_status(node_name, analysis_id, namespace)
    except OpenShiftNotFound:
        result.update({"error": f"Status for analysis {analysis_id} was not found or it has not started yet"})
        return result, 404
    else:
        result.update({"status": status})
        return result, 200


def _get_status_with_queued(
    adapter: Union[AdvisersResultsStore, ProvenanceResultsStore, AnalysisResultsStore],
    node_name: str,
    analysis_id: str,
    namespace: str,
) -> Tuple[Dict[str, Any,], int]:
    """Get status of an analysis, check queued requests as well."""
    result, status_code = _get_status(node_name=node_name, analysis_id=analysis_id, namespace=namespace)
    if status_code == 404:
        adapter_instance = adapter()
        adapter_instance.connect()
        if adapter_instance.request_exists(analysis_id):
            return _construct_status_queued(analysis_id), 200
    return result, status_code


def _send_schedule_message(
    message_contents: Dict[str, Any],
    message_type: MessageBase,
    content: Type[BaseMessageContents],
    with_authentication: bool = False,
    authenticated: bool = False,
) -> Tuple[Dict[str, Any], int]:
    from .openapi_server import PRODUCER

    message_contents["service_version"] = SERVICE_VERSION
    message_contents["component_name"] = COMPONENT_NAME
    message = content(**message_contents)
    producer.publish_to_topic(PRODUCER, message_type, message)
    if "job_id" in message_contents:

        if with_authentication:
            return (
                {
                    "analysis_id": message_contents["job_id"],
                    "cached": False,
                    "authenticated": authenticated,
                    "parameters": message_contents,
                },
                202,
            )

        return (
            {
                "analysis_id": message_contents["job_id"],
                "parameters": message_contents,
                "cached": False,
            },
            202,
        )

    raise ValueError(f"job_id was not set for message sent to {message_type.topic_name}")


def _do_get_image_metadata(
    image: str, registry_user: Optional[str] = None, registry_password: Optional[str] = None, verify_tls: bool = True
) -> Tuple[Dict[str, Any], int]:
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
    except ImageInvalidCredentialsError as exc:
        status_code = 403
        error_str = str(exc)
    except ImageManifestUnknownError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageAuthenticationRequiredError as exc:
        status_code = 401
        error_str = str(exc)
    except ImageError as exc:
        status_code = 400
        error_str = str(exc)

    return {"error": error_str, "parameters": locals()}, status_code


def get_package_from_imported_packages(import_name: str) -> Tuple[Dict[str, Any], int]:
    """Retrieve Python package name for the given import package name."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        result = GRAPH.get_python_package_version_import_packages_all(import_name=import_name, distinct=True)

        # Remap "import" to "package_import" as it causes troubles when generating client.
        for item in result:
            item["package_import"] = item.pop("import")

        return {
            "package_names": result,
            "parameters": parameters,
        }, 200
    except NotFoundError:
        return (
            {
                "error": f"No package name records for package {import_name!r} in database",
                "parameters": parameters,
            },
            404,
        )


def list_python_environments() -> Dict[str, List[Dict[str, str]]]:
    """Get environments available based on solvers installed."""
    result = []
    for solver in _OPENSHIFT.get_solver_names():
        item = _OPENSHIFT.parse_python_solver_name(solver)
        result.append(item)

        if item["os_name"] == "rhel":
            # Duplicate entry as we can also guide on the same UBI environment. UBI and RHEL are binary compatible.
            other_item = dict(item)
            other_item["os_name"] = "ubi"
            result.append(other_item)

    result.sort(key=lambda i: (i.get("os_name"), i.get("os_version"), i.get("python_version")))
    return {"environment": result}
