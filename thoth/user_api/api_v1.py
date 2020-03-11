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

import os
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
from thoth.storages import BuildLogsAnalysisResultsStore
from thoth.storages import GraphDatabase
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

from .configuration import Configuration
from .image import get_image_metadata
from .exceptions import ImageError
from .exceptions import ImageBadRequestError
from .exceptions import ImageManifestUnknownError
from .exceptions import ImageAuthenticationRequired
from .exceptions import NotFoundException


PAGINATION_SIZE = 100
_LOGGER = logging.getLogger(__name__)
_OPENSHIFT = OpenShift()


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
    metadata = _do_get_image_metadata(
        image, registry_user=registry_user, registry_password=registry_password, verify_tls=verify_tls
    )

    if metadata[1] != 200:
        # There was an error extracting metadata, tuple holds dictionary with error report and HTTP status code.
        return metadata

    metadata = metadata[0]
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

    response, status_code = _do_schedule(
        parameters, _OPENSHIFT.schedule_package_extract, output=Configuration.THOTH_ANALYZER_OUTPUT
    )

    analysis_by_digest_store = AnalysisByDigest()
    analysis_by_digest_store.connect()
    analysis_by_digest_store.store_document(metadata["digest"], response)

    if status_code == 202:
        cache.store_document_record(cached_document_id, {"analysis_id": response["analysis_id"]})

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


def get_analyze_log(analysis_id: str):
    """Get image analysis log."""
    return _get_job_log(locals(), "package-extract-", Configuration.THOTH_MIDDLETIER_NAMESPACE)


def get_analyze_status(analysis_id: str):
    """Get status of an image analysis."""
    return _get_job_status(locals(), "package-extract-", Configuration.THOTH_MIDDLETIER_NAMESPACE)


def post_provenance_python(application_stack: dict, origin: str = None, debug: bool = False, force: bool = False):
    """Check provenance for the given application stack."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        project = Project.from_strings(application_stack["requirements"], application_stack["requirements_lock"])
    except ThothPythonException as exc:
        return {"parameters": parameters, "error": f"Invalid application stack supplied: {str(exc)}"}, 400
    except Exception as exc:
        return {"parameters": parameters, "error": "Invalid application stack supplied"}, 400

    parameters["whitelisted_sources"] = list(GRAPH.get_python_package_index_urls())

    force = parameters.pop("force", False)
    cached_document_id = _compute_digest_params(
        dict(**project.to_dict(), origin=origin, whitelisted_sources=parameters["whitelisted_sources"])
    )

    timestamp_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    cache = ProvenanceCacheStore()
    cache.connect()

    if not force:
        try:
            cache_record = cache.retrieve_document_record(cached_document_id)
            if cache_record["timestamp"] + Configuration.THOTH_CACHE_EXPIRATION > timestamp_now:
                return {"analysis_id": cache_record.pop("analysis_id"), "cached": True, "parameters": parameters}, 202
        except CacheMiss:
            pass

    response, status = _do_schedule(
        parameters, _OPENSHIFT.schedule_provenance_checker, output=Configuration.THOTH_PROVENANCE_CHECKER_OUTPUT
    )
    if status == 202:
        cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

    return response, status


def get_provenance_python(analysis_id: str):
    """Retrieve a provenance check result."""
    return _get_document(
        ProvenanceResultsStore,
        analysis_id,
        name_prefix="provenance-checker-",
        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
    )


def get_provenance_python_log(analysis_id: str):
    """Get provenance-checker logs."""
    return _get_job_log(locals(), "provenance-checker-", Configuration.THOTH_BACKEND_NAMESPACE)


def get_provenance_python_status(analysis_id: str):
    """Get status of a provenance check."""
    return _get_job_status(locals(), "provenance-checker-", Configuration.THOTH_BACKEND_NAMESPACE)


def post_advise_python(
    input: dict,
    recommendation_type: str,
    count: int = None,
    limit: int = None,
    limit_latest_versions: int = None,
    origin: str = None,
    is_s2i: bool = None,
    debug: bool = False,
    force: bool = False,
    github_event_type: typing.Optional[str] = None,
    github_check_run_id: typing.Optional[int] = None,
    github_installation_id: typing.Optional[int] = None,
    github_base_repo_url: typing.Optional[str] = None,
):
    """Compute results for the given package or package stack using adviser."""
    parameters = locals()
    parameters["application_stack"] = parameters["input"].pop("application_stack")

    github_webhook_params = (
        github_event_type is not None,
        github_check_run_id is not None,
        github_installation_id is not None,
        github_base_repo_url is not None,
    )
    github_webhook_params_present = sum(github_webhook_params)
    if github_webhook_params_present != 0 and (github_webhook_params_present != len(github_webhook_params)
                                               or not origin):
        return {"parameters": parameters, "error": "Not all webhook parameters provided for GitHub webhook"}, 400

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

    try:
        project = Project.from_strings(
            parameters["application_stack"]["requirements"],
            parameters["application_stack"].get("requirements_lock"),
            runtime_environment=RuntimeEnvironment.from_dict(parameters["runtime_environment"]),
        )
    except ThothPythonException as exc:
        return {"parameters": parameters, "error": f"Invalid application stack supplied: {str(exc)}"}, 400
    except Exception as exc:
        return {"parameters": parameters, "error": "Invalid application stack supplied"}, 400

    # We could rewrite this to a decorator and make it shared with provenance
    # checks etc, but there are small glitches why the solution would not be
    # generic enough to be used for all POST endpoints.
    adviser_cache = AdvisersCacheStore()
    adviser_cache.connect()

    timestamp_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    cached_document_id = _compute_digest_params(
        dict(
            **project.to_dict(),
            count=parameters["count"],
            limit=parameters["limit"],
            library_usage=parameters["library_usage"],
            limit_latest_versions=parameters["limit_latest_versions"],
            recommendation_type=recommendation_type,
            origin=origin,
            is_s2i=is_s2i,
        )
    )

    if not force:
        try:
            cache_record = adviser_cache.retrieve_document_record(cached_document_id)
            if cache_record["timestamp"] + Configuration.THOTH_CACHE_EXPIRATION > timestamp_now:
                return {"analysis_id": cache_record.pop("analysis_id"), "cached": True, "parameters": parameters}, 202
        except CacheMiss:
            pass

    response, status = _do_schedule(parameters, _OPENSHIFT.schedule_adviser, output=Configuration.THOTH_ADVISER_OUTPUT)
    if status == 202:
        adviser_cache.store_document_record(
            cached_document_id, {"analysis_id": response["analysis_id"], "timestamp": timestamp_now}
        )

    return response, status


def list_advise_python(page: int = 0):
    """List available runtime environments."""
    return _do_listing(AdvisersResultsStore, page)


def get_advise_python(analysis_id):
    """Retrieve the given recommendation based on its id."""
    return _get_document(
        AdvisersResultsStore, analysis_id, name_prefix="adviser-", namespace=Configuration.THOTH_BACKEND_NAMESPACE
    )


def get_advise_python_log(analysis_id: str):
    """Get adviser log."""
    return _get_job_log(locals(), "adviser-", Configuration.THOTH_BACKEND_NAMESPACE)


def get_advise_python_status(analysis_id: str):
    """Get status of an adviser run."""
    status, code = _get_job_status(locals(), "adviser-", Configuration.THOTH_BACKEND_NAMESPACE)
    if "error" in status:
        wf_status = None
        try:
            wf_status = _OPENSHIFT.get_workflow_status(
                name=analysis_id,
                namespace=Configuration.THOTH_BACKEND_NAMESPACE
            )

            # the Job has not started (yet) but the Workflow has been submitted
            # if the Workflow fails, the status will contain the finished
            # time of the workflow
            status["status"], code = {
                "container": None,
                "exit_code": None,
                "finished_at": wf_status.get("finishedAt"),
                "reason": None,
                "started_at": wf_status.get("startedAt"),
                "state": wf_status["phase"]
            }, 200

            status.pop("error")

        except NotFoundException as exc:
            # Handle this since the adviser run can still be scheduled
            # with workload-operator instead, otherwise we could raise here
            _LOGGER.error(status["error"])

    return status, code


def list_runtime_environments():
    """List available runtime environments."""
    environments = []
    for solver_name in _OPENSHIFT.get_solver_names():
        solver_info = GraphDatabase.parse_python_solver_name(solver_name)
        environments.append(solver_info)

    return {"runtime_environments": environments, "parameters": {}}


def list_software_environments_for_build(page: int = 0):
    """List available software environments for build."""
    parameters = locals()
    from .openapi_server import GRAPH

    result = list(sorted(set(GRAPH.get_build_software_environment_all(start_offset=page, count=PAGINATION_SIZE))))
    return (
        {"parameters": parameters, "results": result},
        200,
        {"page": page, "page_size": PAGINATION_SIZE, "results_count": len(result)},
    )


def list_software_environment_analyses_for_build(environment_name: str):
    """List analyses for the given software environment for build."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        result = GRAPH.get_build_software_environment_analyses_all(environment_name, convert_datetime=False)
    except NotFoundError as exc:
        return {"error": str(exc), "parameters": parameters}, 404

    return {"analyses": result, "analyses_count": len(result), "parameters": parameters}, 200


def list_software_environments_for_run(page: int = 0):
    """List available software environments for run."""
    parameters = locals()
    from .openapi_server import GRAPH

    result = list(sorted(set(GRAPH.get_run_software_environment_all(start_offset=page, count=PAGINATION_SIZE))))
    return (
        {"parameters": parameters, "results": result},
        200,
        {"page": page, "page_size": PAGINATION_SIZE, "results_count": len(result)},
    )


def list_software_environment_analyses_for_run(environment_name: str):
    """Get analyses of given software environments for run."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        result = GRAPH.get_run_software_environment_analyses_all(environment_name, convert_datetime=False)
    except NotFoundError as exc:
        return {"error": str(exc), "parameters": parameters}, 404

    return {"analyses": result, "analyses_count": len(result), "parameters": parameters}, 200


def list_python_package_indexes():
    """List registered Python package indexes in the graph database."""
    from .openapi_server import GRAPH

    return GRAPH.get_python_package_index_all()


def get_python_package_dependencies(
    name: str,
    version: str,
    index: str,
    os_name: typing.Optional[str] = None,
    os_version: typing.Optional[str] = None,
    python_version: typing.Optional[str] = None,
    marker_evaluation_result: typing.Optional[bool] = None,
) -> typing.Tuple[typing.Dict[typing.Any, typing.Any], int]:
    """Get dependencies for the given Python package."""
    parameters = locals()

    from .openapi_server import GRAPH

    if (os_name is None and os_version is not None) or (os_name is not None and os_version is None):
        return {
            "error": "Operating system is not fully specified",
            "parameters": parameters,
        }, 400

    if marker_evaluation_result is not None and (os_name is None or os_version is None or python_version is None):
        return {
            "error": "Operating system and Python interpreter version need "
                     "to be specified to obtain dependencies dependent on marker evaluation result",
            "parameters": parameters,
        }, 400

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
        return {
            "error": f"No record found for package {name!r} in version {version!r} from "
                     f"index {index!r} for {os_name!r} in version {os_version!r} using Python "
                     f"version {python_version!r}",
            "parameters": parameters,
        }, 404

    result = []
    for extra, entries in query_result.items():
        for entry in entries:
            result.append({
                "name": entry[0],
                "version": entry[1],
                "extra": extra,
                "environment_marker": None,
            })

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
                    return {
                        "error": f"No environment marker records found for package {name!r} in version "
                                 f"{version!r} from index {index!r} with dependency "
                                 f"on {entry[0]!r} in version {entry[1]!r}",
                        "parameters": parameters,
                    }, 404

    return result


def list_hardware_environments(page: int = 0):
    """List hardware environments in the graph database."""
    from .openapi_server import GRAPH

    return {
        "parameters": {"page": page},
        "hardware_environments": GRAPH.get_hardware_environments_all(is_external=False, start_offset=page),
    }


def list_software_environments(page: int = 0):
    """List software environments in the graph database."""
    from .openapi_server import GRAPH

    return {
        "parameters": {"page": page},
        "software_environments": GRAPH.get_software_environments_all(is_external=False, start_offset=page),
    }


def post_build(
    build_detail: dict,
    debug: bool = False,
    registry_user: str = None,
    registry_password: str = None,
    environment_type: str = None,
    origin: str = None,
    registry_verify_tls: bool = True,
    force: bool = False,
):
    """Run analysis on a build."""
    response = {"base_image_analysis": {}, "output_image_analysis": {}, "build_log_analysis": {}}
    status = 202
    if build_detail.get("output_image"):
        # Run image analysis
        output_image_analyze_response, output_image_analyze_status = post_analyze(
            image=build_detail["output_image"],
            debug=debug,
            registry_user=registry_user,
            registry_password=registry_password,
            environment_type=environment_type,
            origin=origin,
            verify_tls=registry_verify_tls,
            force=force,
        )
        response["output_image_analysis"] = output_image_analyze_response
        if output_image_analyze_status != 202:
            return response, output_image_analyze_status

    if build_detail.get("base_image"):
        # Run base image analysis
        base_image_analyze_response, base_image_analyze_status = post_analyze(
            image=build_detail["base_image"],
            debug=debug,
            environment_type=environment_type,
            origin=origin,
            verify_tls=registry_verify_tls,
            force=force,
        )
        response["base_image_analysis"] = base_image_analyze_response
        if base_image_analyze_status != 202:
            return response, base_image_analyze_status

    if build_detail.get("build_log"):
        # attach image analysis details to build log
        build_detail["output_image_analysis_id"] = response.get("output_image_analysis", {}).get("analysis_id")
        build_detail["base_image_analysis_id"] = response.get("base_image_analysis", {}).get("analysis_id")

        # Run build log analysis
        buildlog_analyze_response, buildlog_analyze_status = post_buildlog_analyze(log_info=build_detail, force=force)
        response["build_log_analysis"] = buildlog_analyze_response
        if buildlog_analyze_status != 202:
            return response, buildlog_analyze_status

    if (
        not build_detail.get("output_image")
        and not build_detail.get("base_image")
        and not build_detail.get("build_log")
    ):
        return {"error": "Bad Request! No information provided"}, 400

    return response, status


def post_buildlog_analyze(log_info: dict, force: bool = False):
    """Run an analyzer on the given build log."""
    parameters = locals()
    cache = BuildLogsAnalysesCacheStore()
    cache.connect()
    cached_document_id = _compute_digest_params(parameters)
    force = parameters.pop("force", False)
    if not force:
        try:
            cache_record = cache.retrieve_document_record(cached_document_id)
            return {"analysis_id": cache_record.pop("analysis_id"), "cached": True, "parameters": parameters}, 202
        except CacheMiss:
            pass
    # Maybe need to utilize the status code of buildlog storage
    stored_log_details, status = post_buildlog(log_info=log_info)
    parameters.update(stored_log_details)
    parameters.pop("log_info", None)
    response, status_code = _do_schedule(
        parameters, _OPENSHIFT.schedule_build_report, output=Configuration.THOTH_BUILDLOG_ANALYZER_OUTPUT
    )

    if status_code == 202:
        cache.store_document_record(cached_document_id, {"analysis_id": response["analysis_id"]})

    return response, status_code


def list_buildlog_analyze(page: int = 0):
    """Retrieve list of build log analysis result."""
    return _do_listing(BuildLogsAnalysisResultsStore, page)


def get_buildlog_analyze(analysis_id: str):
    """Retrieve build log analysis result."""
    return _get_document(
        BuildLogsAnalysisResultsStore,
        analysis_id,
        name_prefix="build-analyze-",
        namespace=Configuration.THOTH_BACKEND_NAMESPACE,
    )


def post_buildlog(log_info: dict):
    """Store the given build log."""
    adapter = BuildLogsStore()
    adapter.connect()
    document_id = adapter.store_document(log_info)

    return {"document_id": document_id}, 202


def get_buildlog(document_id: str):
    """Retrieve the given buildlog."""
    return _get_document(BuildLogsStore, document_id)


def schedule_kebechet(body: dict):
    """Schedule Kebechet on Openshift."""
    # TODO: Update documentation to include creation of environment variables corresponding to git service tokens
    # NOTE: Change for event dependent behaviour
    headers = connexion.request.headers
    if "X-GitHub-Event" in headers:
        service = "github"
        url = body.get("repository", {}).get("html_url")
    elif "X_GitLab_Event" in headers:
        service = "gitlab"
        url = body.get("repository", {}).get("homepage")
    elif "X_Pagure_Topic" in headers:
        service = "pagure"
        return {"error": "Pagure is currently not supported"}, 501
    else:
        return {"error": "This webhook is not supported"}, 501

    if url is None:
        return {"error", f"Failed to parse webhook payload for service {service!r}"}, 501

    parameters = {"service": service, "url": url}
    return _do_schedule(parameters, _OPENSHIFT.schedule_kebechet_run_url)


def schedule_thamos_advise(
    input: typing.Dict[str, typing.Any],
):
    """Schedule Thamos Advise for GitHub App."""
    # TODO: Remove the variable
    os.environ["THOTH_USE_ARGO"] = "1"
    input["host"] = Configuration.THOTH_HOST
    res = _do_schedule(input, _OPENSHIFT.schedule_thamos_workflow)
    os.environ["THOTH_USE_ARGO"] = str(int(_OPENSHIFT.use_argo))

    return res


def list_buildlogs(page: int = 0):
    """List available build logs."""
    return _do_listing(BuildLogsStore, page)


def get_python_package_versions_count():
    """Retrieve number of Python package versions in Thoth Knowledge Graph."""
    from .openapi_server import GRAPH

    return {"count": GRAPH.get_python_package_versions_count_all(distinct=True)}


def get_package_metadata(name: str, version: str, index: str):
    """Retrieve metadata for the given package version."""
    parameters = locals()
    from .openapi_server import GRAPH

    try:
        return GRAPH.get_python_package_version_metadata(package_name=name, package_version=version, index_url=index)
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


def _get_document(adapter_class, analysis_id: str, name_prefix: str = None, namespace: str = None) -> tuple:
    """Perform actual document retrieval."""
    # Parameters to be reported back to a user of API.
    parameters = {"analysis_id": analysis_id}
    if name_prefix and not analysis_id.startswith(name_prefix):
        return {"error": "Wrong analysis id provided", "parameters": parameters}, 400

    try:
        adapter = adapter_class()
        adapter.connect()
        result = adapter.retrieve_document(analysis_id)
        return result, 200
    except NotFoundError:
        if namespace:
            try:
                status = _OPENSHIFT.get_job_status_report(analysis_id, namespace=namespace)
                if status["state"] == "running" or (status["state"] == "terminated" and status["exit_code"] == 0):
                    # In case we hit terminated and exit code equal to 0, the analysis has just finished and
                    # before this call (document retrieval was unsuccessful, pod finished and we asked later
                    # for status). To fix this time-dependent issue, let's user ask again. Do not do pod status
                    # check before document retrieval - this solution is more optimal as we do not ask master
                    # status each time.
                    return {"error": "Analysis is still in progress", "status": status, "parameters": parameters}, 202
                elif status["state"] == "terminated":
                    return {"error": "Analysis was not successful", "status": status, "parameters": parameters}, 400
                elif status["state"] in ("scheduling", "waiting", "registered"):
                    return {"error": "Analysis is being scheduled", "status": status, "parameters": parameters}, 202
                else:
                    # Can be:
                    #   - return 500 to user as this is our issue
                    raise ValueError(f"Unreachable - unknown job state: {status}")
            except OpenShiftNotFound:
                pass
        return {"error": f"Requested result for analysis {analysis_id!r} was not found", "parameters": parameters}, 404


def _get_job_log(parameters: dict, name_prefix: str, namespace: str):
    """Get job log based on analysis id."""
    job_id = parameters.get("analysis_id")
    if not job_id.startswith(name_prefix):
        return {"error": "Wrong analysis id provided", "parameters": parameters}, 400

    try:
        log = _OPENSHIFT.get_job_log(job_id, namespace=namespace)
    except OpenShiftNotFound:
        return {"parameters": parameters, "error": f"No analysis with id {job_id} was found"}, 404

    return {"parameters": parameters, "log": log}, 200


def _get_job_status(parameters: dict, name_prefix: str, namespace: str):
    """Get status for a job."""
    job_id = parameters.get("analysis_id")
    if not job_id.startswith(name_prefix):
        return {"error": "Wrong analysis id provided", "parameters": parameters}, 400

    try:
        status = _OPENSHIFT.get_job_status_report(job_id, namespace=namespace)
    except OpenShiftNotFound:
        return {"parameters": parameters, "error": f"Requested status for analysis {job_id!r} was not found"}, 404

    return {"parameters": parameters, "status": status}, 200


def _do_schedule(parameters: dict, runner: typing.Callable, **runner_kwargs):
    """Schedule the given job - a generic method for running any analyzer, solver, ..."""
    return {"analysis_id": runner(**parameters, **runner_kwargs), "parameters": parameters, "cached": False}, 202


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
    except ImageManifestUnknownError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageAuthenticationRequired as exc:
        status_code = 401
        error_str = str(exc)
    except ImageError as exc:
        status_code = 400
        error_str = str(exc)
    except ImageInvalidCredentials as exc:
        status_code = 403
        error_str = str(exc)

    return {"error": error_str, "parameters": locals()}, status_code
