# Changelog for Thoth's User API Service

## [0.4.0] - 2018-Jun-26 - goern

### Added

Starting with this release we have a Zuul-CI pipeline that:

* lints on Pull Requrest and gate/merge


## [0.3.0] - 2018-Jun-12 - goern

### Added

Set resource limits of BuildConfig and Deployment to reasonable values, this will prevent unpredicted behavior on UpShift.
## Release 0.6.1 (2020-05-11T11:32:36)
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* make coala happy
* fix key error state
* :pushpin: Automatic update of dependency thoth-storages from 0.22.8 to 0.22.9
* Use correct keys
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* Moved serialization to common.
* Added event for gitlab
* Fixed coala err
* Handle Github Webhooks
* condition for argo check before workflow status check
* :pushpin: Automatic update of dependency thoth-storages from 0.22.7 to 0.22.8
* :pushpin: Automatic update of dependency connexion from 2.6.0 to 2.7.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* Consumes whole payload
* Added a route to receive webhook
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* Add platform information to OpenAPI spec
* :pushpin: Automatic update of dependency thoth-python from 0.9.1 to 0.9.2
* Add filters for python packages count
* Pin grpcio to <1.28
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* Remove latest version restriction from .thoth.yaml
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* Increase resources for build even more
* Increase memory requirements for the s2i build
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.2 to 1.28.1
* :pushpin: Automatic update of dependency grpcio from 1.27.2 to 1.28.1
* :pushpin: Automatic update of dependency flask from 1.1.1 to 1.1.2
* Distinguish debug option when accessing the cache for provenance results
* Make GitHub events parameters options to the cache
* :pushpin: Automatic dependency re-locking
* Remove variable not required
* Missing exception import
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.2 to 1.28.0
* :pushpin: Automatic update of dependency grpcio from 1.27.2 to 1.28.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.5 to 0.22.7
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.5
* Introduce adviser's dev flag to consider or not consider dev dependencies
* Configure logging for access log
* :pushpin: Automatic update of dependency thoth-common from 0.12.0 to 0.12.1
* removed these unused files
* fixed a typo
* introduced a service version string that contains the depending module's versions
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.2 to 0.14.3
* :pushpin: Automatic update of dependency thoth-storages from 0.22.3 to 0.22.5
* Changed to fix thamos error
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* Add env variable to use Argo
* Fix for GraphDatabase has no attribute get_python_package_index_urls
* Issue check on not found (404)
* :pushpin: Automatic update of dependency pytest from 5.4.0 to 5.4.1
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.0
* Return Pending state if wf doesn't have a phase set
* Get status of an adviser run from a Workflow
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.2 to 0.13.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.2 to 0.13.0
* Remove check on graph initialization
* Set image pull policy to always
* Add missing import
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.1 to 0.14.2
* Fallback if thoth fails to give advise in bc
* :pushpin: Automatic update of dependency thoth-storages from 0.22.2 to 0.22.3
* fixed coala errors
* changed condition
* Reverted back
* Advise route fix
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* Correct datatype
* :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.1 to 1.27.2
* :pushpin: Automatic update of dependency grpcio from 1.27.1 to 1.27.2
* :pushpin: Automatic update of dependency thoth-storages from 0.22.1 to 0.22.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.0 to 0.22.1
* :pushpin: Automatic update of dependency thoth-storages from 0.21.11 to 0.22.0
* Update .thoth.yaml
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency grpcio-tools from 1.26.0 to 1.27.1
* :pushpin: Automatic update of dependency grpcio from 1.26.0 to 1.27.1
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic dependency re-locking
* Modify post_advise
* remove revision
* Modify parameters for GitHub App
* :pushpin: Automatic update of dependency grpcio-tools from 1.26.0 to 1.27.0
* :pushpin: Automatic update of dependency grpcio from 1.26.0 to 1.27.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* Moved common parameters to components
* Introduce env var for Thoth host
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* Use string for env variable
* POST endpoint accepts input body
* Add missing import
* :pushpin: Automatic update of dependency connexion from 2.5.1 to 2.6.0
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* Add endpoint exposing package dependencies
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* standardize parameters for GitHubApp workflow scheduling
* Add GitHub specific metadata for GitHub integration
* Added handlin to user facing function
* Fixed coala errors
* Added an extra exception catch
* :pushpin: Automatic update of dependency thoth-storages from 0.21.10 to 0.21.11
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* Add responses
* Correct wrong datatype
* Add temporary variable to use Argo workflow
* New Endpoint to schedule Thamos Advise workflow for QebHwt
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.0 to 0.14.1
* :pushpin: Automatic update of dependency thoth-storages from 0.21.9 to 0.21.10
* :pushpin: Automatic update of dependency thoth-storages from 0.21.8 to 0.21.9
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-storages from 0.21.7 to 0.21.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* Added nullables to Runtime Environment properties
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.27 to 0.9.28
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.27
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.7 to 0.1.8
* :pushpin: Automatic update of dependency thoth-storages from 0.21.6 to 0.21.7
* :pushpin: Automatic update of dependency jaeger-client from 4.2.0 to 4.3.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency thoth-storages from 0.21.5 to 0.21.6
* use build-report instead of build-analyze
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency thoth-storages from 0.21.4 to 0.21.5
* :pushpin: Automatic update of dependency thoth-storages from 0.21.3 to 0.21.4
* :pushpin: Automatic update of dependency thoth-storages from 0.21.2 to 0.21.3
* :pushpin: Automatic update of dependency thoth-storages from 0.21.1 to 0.21.2
* :pushpin: Automatic update of dependency thoth-storages from 0.21.0 to 0.21.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* :pushpin: Automatic update of dependency thoth-storages from 0.20.6 to 0.21.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.5 to 0.14.0
* :pushpin: Automatic update of dependency thoth-storages from 0.20.5 to 0.20.6
* Do not run adviser from bc in debug mode
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* :pushpin: Automatic update of dependency thoth-storages from 0.20.4 to 0.20.5
* :pushpin: Automatic update of dependency thoth-python from 0.7.1 to 0.8.0
* :pushpin: Automatic update of dependency thoth-storages from 0.20.3 to 0.20.4
* :pushpin: Automatic update of dependency thoth-storages from 0.20.2 to 0.20.3
* :pushpin: Automatic update of dependency thoth-storages from 0.20.1 to 0.20.2
* Happy new year!
* :pushpin: Automatic update of dependency thoth-storages from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.30 to 0.20.0
* :pushpin: Automatic update of dependency connexion from 2.5.0 to 2.5.1
* :pushpin: Automatic update of dependency grpcio-tools from 1.25.0 to 1.26.0
* :pushpin: Automatic update of dependency grpcio from 1.25.0 to 1.26.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.27 to 0.19.30
* :pushpin: Automatic update of dependency connexion from 2.4.0 to 2.5.0
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.6 to 0.1.7
* Provide is_s2i flag on user API
* Use RHEL instead of UBI
* Update Thoth configuration file and Thoth's s2i configuration
* Connect to database lazily, after fork
* :pushpin: Automatic update of dependency thoth-storages from 0.19.26 to 0.19.27
* :pushpin: Automatic update of dependency thoth-storages from 0.19.25 to 0.19.26
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.5 to 0.1.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* Two new endpoints
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.11.0 to 0.12.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.24 to 0.19.25
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.4 to 0.1.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency jaeger-client from 4.1.0 to 4.2.0
* :pushpin: Automatic update of dependency gunicorn from 20.0.3 to 20.0.4
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency gunicorn from 20.0.2 to 20.0.3
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.2 to 0.13.3
* :pushpin: Automatic update of dependency gunicorn from 20.0.0 to 20.0.2
* :pushpin: Automatic update of dependency thoth-storages from 0.19.23 to 0.19.24
* :green_heart: updated some kinds, apiVersions
* :pushpin: Automatic update of dependency thoth-storages from 0.19.22 to 0.19.23
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* Add sentry-sdk[flask] for Sentry Flask integration
* Add aiocontextvars for sentry-sdk integration with aiohttp
* :green_heart: fixed the type
* Added headers to response
* :pushpin: Automatic update of dependency thoth-storages from 0.19.19 to 0.19.22
* New endpoints for Python packages in Thoth Knowledge Graph
* Correct output for error response for all queries
* Correct error response output
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* Maintain one graph datababase adapter instance also in health checks
* Instantiate one adapter per wsgi worker
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* :pushpin: Automatic update of dependency thoth-storages from 0.19.18 to 0.19.19
* Track only user endpoints
* List only enabled Python package indexes to users
* :pushpin: Automatic update of dependency gunicorn from 19.9.0 to 20.0.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.17 to 0.19.18
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.15 to 0.19.17
* Fix redirect to Swagger UI to make it work
* Always parse runtime environment before submitting to adviser
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.3 to 1.25.0
* :pushpin: Automatic update of dependency grpcio from 1.24.3 to 1.25.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.14 to 0.19.15
* :pushpin: Automatic update of dependency thoth-storages from 0.19.13 to 0.19.14
* :pushpin: Automatic update of dependency thoth-storages from 0.19.12 to 0.19.13
* Update queries according to standardize naming convention
* updated templates with annotations and param thoth-advise-value
* Fix offset to start_offset
* use github webhook variable html_url
* Catch exception when database is not initialized
* :pushpin: Automatic update of dependency thoth-storages from 0.19.11 to 0.19.12
* :pushpin: Automatic update of dependency thoth-storages from 0.19.10 to 0.19.11
* Fix issue when overwriting parameters
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* Do not introduce fatal fail if database schema was removed
* Redirect to HTTPS instead of HTTP if configured so
* Fix entrypoint - remove old entrypoint
* Check if database schema is up2date in readiness probe
* Remove Info
* Remove Dgraph memories
* Make coala happy
* Set is_external to False explicitly
* Remove is_external from api_v1.py
* Removed is_external
* Fix typo
* Return parameters
* Add software & hardware environment listing
* Add missing properties to User API
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.1 to 1.24.3
* :pushpin: Automatic update of dependency grpcio from 1.24.1 to 1.24.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.9 to 0.19.10
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency connexion from 2.3.0 to 2.4.0
* Fix component reference in openapi
* Report 404 if no metadata are found for the given package
* :sparkles: added a PR template
* [Feature] Get metadata for a Python package
* :pushpin: Automatic update of dependency attrs from 19.2.0 to 19.3.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* Provide is_external flag to package-extract runs explictly
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :sparkles: bounce the version to 0.6.0-dev
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.0 to 1.24.1
* :pushpin: Automatic update of dependency grpcio from 1.24.0 to 1.24.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.10.0 to 0.11.0
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.2.0 to 3.2.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* :pushpin: Automatic update of dependency attrs from 19.1.0 to 19.2.0
* add pipfile lock
* Made changes
* fixing cors issue
* :pushpin: Automatic update of dependency thoth-storages from 0.19.8 to 0.19.9
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* Add Thoth version information to each response
* Delete Info
* :pushpin: Automatic update of dependency thoth-storages from 0.19.7 to 0.19.8
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.3 to 0.1.4
* Be more safe when parsing webhook payload
* Remove unused function - log parsing has been moved to async handling
* :pushpin: Automatic update of dependency grpcio-tools from 1.23.0 to 1.24.0
* :pushpin: Automatic update of dependency grpcio from 1.23.0 to 1.24.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.9.1 to 0.10.0
* updated cpu and memory allocation
* :pushpin: Automatic update of dependency thoth-storages from 0.19.6 to 0.19.7
* use postgresql hostname from thoth configmap
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.5 to 0.19.6
* Check PostgreSQL in liveness or readiness probe
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.2 to 0.1.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency thoth-storages from 0.19.4 to 0.19.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* :pushpin: Automatic update of dependency thoth-storages from 0.19.3 to 0.19.4
* :pushpin: Automatic update of dependency thoth-storages from 0.19.2 to 0.19.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.1 to 0.19.2
* :pushpin: Automatic update of dependency thoth-storages from 0.19.0 to 0.19.1
* :pushpin: Automatic update of dependency thoth-storages from 0.18.6 to 0.19.0
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* Use more generic env var names
* Switch from Dgraph to PostgreSQL in deployment
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.1.1 to 3.2.0
* :pushpin: Automatic update of dependency jaeger-client from 4.0.0 to 4.1.0
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* Start using Thoth's s2i base image
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* :pushpin: Automatic update of dependency grpcio-tools from 1.22.0 to 1.23.0
* :pushpin: Automatic update of dependency grpcio from 1.22.1 to 1.23.0
* :pushpin: Automatic update of dependency grpcio from 1.22.0 to 1.22.1
* Use singular to be compatible with other endpoints
* Provide endpoint for listing supported runtime environments
* :pushpin: Automatic update of dependency thoth-storages from 0.18.5 to 0.18.6
* Added config
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* Initial dependency lock
* Runtime environment is now reported on the project instance
* Stop using extras in thoth-common
* Wrong URLs
* :pushpin: Automatic update of dependency thoth-storages from 0.18.4 to 0.18.5
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1
* Remove old .thoth.yaml configuration file
* Change name of Thoth template to make Coala happy
* Start using Thoth in OpenShift's s2i
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-storages from 0.18.3 to 0.18.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* Enforce new invectio version by providing required schema
* Remove anchors and use refs instead
* Add information comming from Jupyter Notebooks
* :pushpin: Automatic update of dependency thoth-storages from 0.18.1 to 0.18.3
* :pushpin: Automatic update of dependency thoth-storages from 0.18.0 to 0.18.1
* :pushpin: Automatic update of dependency thoth-storages from 0.17.0 to 0.18.0
* :pushpin: Automatic update of dependency thoth-storages from 0.16.0 to 0.17.0
* :pushpin: Automatic update of dependency thoth-storages from 0.14.8 to 0.16.0
* :pushpin: Automatic update of dependency thoth-python from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.5
* Removed thoth-build-analyzers dependencies from user-api
* :sunrise: Modified the names to standard convention
* :dolphin: user-api support for build analysis and build log analysis
* Changed based on review
* Explicitly state python type
* :pushpin: Automatic update of dependency thoth-storages from 0.14.7 to 0.14.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* :pushpin: Automatic update of dependency thoth-storages from 0.14.6 to 0.14.7
* Added error return value for pagure
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* :pushpin: Automatic update of dependency thoth-storages from 0.14.5 to 0.14.6
* :pushpin: Automatic update of dependency thoth-storages from 0.14.4 to 0.14.5
* :pushpin: Automatic update of dependency flask from 1.1.0 to 1.1.1
* :star: python black linting and styling fixes
* updated the deprecated version check
* Error code return values
* :pushpin: Automatic update of dependency thoth-storages from 0.14.3 to 0.14.4
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.0.1 to 3.1.1
* :pushpin: Automatic update of dependency flask from 1.0.4 to 1.1.0
* :pushpin: Automatic update of dependency flask from 1.0.3 to 1.0.4
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency thoth-storages from 0.14.1 to 0.14.3
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.8.1 to 0.9.0
* :pushpin: Automatic update of dependency prometheus-client from 0.7.0 to 0.7.1
* :pushpin: Automatic update of dependency grpcio-tools from 1.21.1 to 1.22.0
* :pushpin: Automatic update of dependency grpcio from 1.21.1 to 1.22.0
* Changed variable name
* /kebechet endpoint works
* Addition
* Interface with thoth-common kebechet scheduler
* Update the trigger-build job to use the latest job API
* :pushpin: Automatic update of dependency connexion from 2.2.0 to 2.3.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.8.0 to 0.8.1
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* Metrics are available for Prometheus and grouped by endpoint
* :pushpin: Automatic update of dependency prometheus-client from 0.6.0 to 0.7.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency thoth-storages from 0.14.0 to 0.14.1
* Internal Error Connection due to attributes
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency thoth-storages from 0.11.4 to 0.14.0
* Update Pipfile.lock
* Handle workload registered state
* Migrate parsing API to thoth-build-analysers
* :pushpin: Automatic update of dependency grpcio-tools from 1.20.1 to 1.21.1
* :pushpin: Automatic update of dependency grpcio from 1.20.1 to 1.21.1
* Typos corrected
* Correct metric info
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.4 to 0.8.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.3 to 0.7.4
* Modified endpoints
* Update functions for user API
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.2 to 0.7.3
* :pushpin: Automatic update of dependency flask from 1.0.2 to 1.0.3
* :pushpin: Automatic update of dependency requests from 2.21.0 to 2.22.0
* :wrench: minor fix template for openshift >=3.11
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency thoth-storages from 0.11.3 to 0.11.4
* :pushpin: Automatic update of dependency thoth-storages from 0.11.2 to 0.11.3
* Fix method names, provide image names only once
* Do not convert datetimes, keep them as strings
* Consolidate endpoints for buildtime and runtime analyses
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency thoth-storages from 0.11.1 to 0.11.2
* Implement User API using Stub API template
* Add library usage parameter to adviser's API
* :pushpin: Automatic update of dependency thoth-storages from 0.11.0 to 0.11.1
* :bug: convert set to a list, so that it is json serializable
* Fix env variable name of Dgraph instance in info endpoint
* :pushpin: Automatic update of dependency thoth-storages from 0.10.0 to 0.11.0
* Adjust deployment to respect new Dgraph configuration
* :sparkles: added required ENV
* :sparkles: added mounting the Dgraph TLS secrets
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.1 to 0.7.2
* Switch to Dgraph
* :pushpin: Automatic update of dependency thoth-storages from 0.9.7 to 0.10.0
* :pushpin: Automatic update of dependency pytest from 4.4.0 to 4.4.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* Introduce environment type parameter for image analysis
* Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* Return Bad Request for invalid format request
* Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* Remove pylint zuul job
* Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* Automatic update of dependency prometheus-flask-exporter from 0.7.0 to 0.7.1
* Automatic update of dependency pytest from 4.3.1 to 4.4.0
* Automatic update of dependency prometheus-flask-exporter from 0.6.0 to 0.7.0
* Automatic update of dependency thoth-storages from 0.9.6 to 0.9.7
* Automatic update of dependency thoth-python from 0.4.6 to 0.5.0
* Add Thoth's configuration file
* Automatic update of dependency thoth-common from 0.7.1 to 0.8.1
* Fix requirements so that updates are possible
* :bookmark: bouncing swagger api version to 0.4.0
* reworked the service account part
* remove unused stuff
* Fix wrong pop
* Expose parameter for limiting number of latest versions
* Increase memory requests in deployment
* Set WARNING level before the actual handler function
* Automatic update of dependency pytest from 4.2.1 to 4.3.0
* Automatic update of dependency prometheus-client from 0.5.0 to 0.6.0
* Introduce origin parameter
* Adjust description to respect semantics
* Expose deployment specific configuration to users
* Report unknown errors happening during image extraction
* Fix issues with Pipfile in s2i
* Place runtime environment specification into a standalone model
* Adjustments to respect Thoth configuration
* Use Python 3.6 by default
* It's already 2019
* Fix wrong operator
* Change order of parameters to skopeo
* Skopeo flag for TLS verification has changed
* State hash type in description
* Introduce endpoint for gathering image information based on image digest
* Make image analysis endpoint work again
* Fix typo in method name
* Fix return value in function signature
* Return 404 in status endpoints if the given analysis id was not found
* Rename method to reflect its semantics
* Schedule workload instead of directly running it
* Cache should also distinguish recommendation type
* Pop supplied input
* Fix key error
* Respect signature of function, return a tuple
* Avoid circular JSONs on error response
* Automatic update of dependency requests from 2.20.1 to 2.21.0
* Automatic update of dependency prometheus-flask-exporter from 0.4.0 to 0.4.1
* Automatic update of dependency prometheus-client from 0.4.2 to 0.5.0
* Update thoth-python to avoid attribute errors
* Update thoth-storages to include Amun client dependency
* Dependency locking
* Implement cache for adviser runs
* Update dependencies, let Kebechet do relocking
* Fixes to make things work
* Introduce cache in provenance checks
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency thoth-storages from 0.8.0 to 0.9.0
* added prometheus metric export for all things REST
* added a pyproject.toml to keep black happy
* added prometheus
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Be more precise with swagger model examples
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Expose available Python package indexes on API
* Provide runtime environment as a JSON
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Introduce count and limit on API for advise
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Extras are not markers
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Extras are not markers
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Automatic update of dependency thoth-storages from 0.7.6 to 0.8.0
* Automatic update of dependency connexion from 2.0.1 to 2.0.2
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Extras are not markers
* Markers are not extras
* fixing markers/extra
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* fixing markers/extra
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Extras are not markers
* Automatic update of dependency thoth-storages from 0.7.5 to 0.7.6
* Automatic update of dependency thoth-storages from 0.7.4 to 0.7.5
* Markers are not extras
* Markers are not extras
* Automatic update of dependency connexion from 2.0.0 to 2.0.1
* Update buildConfig-template.yaml
* Automatic update of dependency thoth-storages from 0.7.2 to 0.7.4
* added HistoryLimits to BuildConfig
* fixed
* Update .zuul.yaml
* Update .zuul.yaml
* Update .zuul.yaml
* New connexion requires swagger-ui extras
* Extras are not markers
* updated to use the latest token (recreated after last reprovisioning of thoth)
* updated to use the latest token (recreated after last reprovisioning of thoth)
* actually do --insecure-skip-tls-verify
* fixed errors
* fixed errors
* fixed errors
* OpenShift are not markers but extras
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* OpenShift are not markers but extras
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* working on redeployment
* using skopeo to pull image
* corrected the label name
* ...
* added thoth-ops SA secret
* Fix dependency name
* fixed coala errors
* Markers are not extras
* Add missing attr dependency
* we dont have a nodeset defined for it yet, lets create it here.
* 1. redeploy after build finished, 2. push image to upstream registry
* started a job that will redeploy user-api to a given OpenShift project
* fixed coala errors
* using thoth zuul jobs now
* Amun and dependency monkey is not used by user API
* Remove unused secret
* Remove endpoints that were moved to management API
* Clear unused dependencies
* Frontend namespace is set from configmap
* Move user API under thoth directory
* Update thoth-storages to 0.7.2
* Provenance checks will be cached as well
* Implement caching of package-extract results
* Update thoth-common and thoth-storages
* Fix parameter name
* Extras are not markers
* Fix key error when gathering pod status
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Report issues using status codes
* Implement metadata gathering for images
* Do not propagate force to actual package-extract run
* Do not propagate force to analysis run
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic dependency re-locking
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency thoth-storages from 0.5.4 to 0.6.0
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Amun API is URL not host
* Respect dependency monkey output configuration
* Introduce cached results of analyses
* Revert "Use TLS in route", it resulted in an unavailable Web UI.
* fixing some misformatted lines
* minor fixes
* Automatic update of dependency thoth-storages from 0.5.3 to 0.5.4
* Automatic update of dependency thoth-storages from 0.5.2 to 0.5.3
* Automatic update of dependency thoth-common from 0.3.10 to 0.3.11
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port
* added THOTH_JANUSGRAPH_{HOST|POST} as template parameters
* Automatic update of dependency thoth-common from 0.3.9 to 0.3.10
* Fix typo in argument name
* Logs can be nullable
* Fix CI
* Use TLS in route
* fixed the template name
* split out the imagestream into his own template
* Automatic update of dependency thoth-common from 0.3.8 to 0.3.9
* Automatic update of dependency thoth-common from 0.3.7 to 0.3.8
* Fix status gathering
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.7
* Move from Pods to Jobs
* Fix linter complains
* Introduce dependency monkey endpoints
* Add skopeo binary
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Fix gathering pod status
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Fix CI complains
* State nullable values in swagger
* Fix reStructuredText issues
* fixed linter errors
* now the ImageStreamTag to be deployed can pe configured via a parameter, default is "latest"
* added a badge
* fixed the badge
* Revert "Add a Codacy badge to README.rst"
* Update README file
* Automatic update of dependency pytest from 3.8.0 to 3.8.1
* Gathering status report moved to common
* Remove unused import
* Fix retrieving documents on wrong endpoint
* Remove 400 responses where not needed
* Provide custom error handlers with more information
* Fix analysis listing model
* Fix linter
* Allow empty lock to be submitted
* Automatic update of dependency thoth-common from 0.3.0 to 0.3.1
* Comment out nullable values due to incompatibility
* Container SHA can be null when analysis is pending
* Fix status response definition
* Remove underscore in cotainer name in response
* Fix parameter name
* Add response schemas to swagger definitions
* Automatic update of dependency connexion from 1.5.2 to 1.5.3
* Signalize user if no solvers were run
* Automatic update of dependency pytest from 3.7.4 to 3.8.0
* Rename recommend to advise all over the places
* Enhance reporting issues when gathering documents to user
* Expose provenance debug option on API
* Fix built-in type shadowing
* Automatic update of dependency thoth-common from 0.2.7 to 0.3.0
* Fix parameter name
* Notify user about running analyses if results are not ready yet
* Report user timeout issues with long-running analyses
* Refactor API to reflect current functionality
* better formating
* removed, as we use Zuul for gating
* Add Codacy badge
* Remove accidentally duplicated function
* Add Codacy badge
* Fix method name
* Code refactoring and always replying parameters
* Automatic update of dependency thoth-common from 0.2.6 to 0.2.7
* Implement provenance checker run
* Introduce provenance endpoint
* Automatic update of dependency thoth-common from 0.2.5 to 0.2.6
* better formating
* Automatic update of dependency thoth-storages from 0.5.1 to 0.5.2
* better formating
* nano fixed
* change the queue
* Provide frontend namespace configuration
* Automatic update of dependency attrs from 18.1.0 to 18.2.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.2.5
* Automatic update of dependency pytest from 3.7.3 to 3.7.4
* Initial dependency lock
* Let Kebechet lock dependencies
* OpenShift and K8s are no longer direct deps
* Automatic update of dependency thoth-storages from 0.5.0 to 0.5.1
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Automatic update of dependency pytest from 3.7.1 to 3.7.3
* Automatic update of dependency kubernetes from 6.0.0 to 7.0.0
* Automatic update of dependency thoth-storages from 0.4.0 to 0.5.0
* Automatic update of dependency thoth-storages from 0.3.0 to 0.4.0
* Automatic update of dependency thoth-storages from 0.2.0 to 0.3.0
* Automatic update of dependency thoth-storages from 0.1.1 to 0.2.0
* Configuration is now available via env vars
* Remove unused entries from configuration
* Use OpenShift object from thoth-common
* Tweak running adviser
* Automatic update of dependency pylint from 2.1.0 to 2.1.1
* Initial dependency lock
* @sesheta please relock
* Add endpoint for listing adviser results
* Label graph sync job triggered by user
* Use OpenShift as a naming service
* Increase memory for user-api
* Automatic update of dependency pylint from 2.0.1 to 2.1.0
* Automatic update of dependency pytest from 3.6.4 to 3.7.0
* Increase memory otherwise container exits on os error 14
* Disable HTTP request logs (#168)
* Automatic update of dependency thoth-common from 0.2.1 to 0.2.2
* Automatic update of dependency pytest from 3.6.3 to 3.6.4
* Automatic update of dependency thoth-storages from 0.1.0 to 0.1.1
* Automatic update of dependency connexion from 1.5.1 to 1.5.2
* Fix label 2
* Fix label
* Adjust template labels (#166)
* new templates
* Automatic update of dependency pytest-timeout from 1.3.0 to 1.3.1
* Automatic update of dependency pylint from 2.0.0 to 2.0.1
* Automatic update of dependency connexion from 1.4.2 to 1.5.1
* increasing the requested resources
* Use default port for services
* modified message in example to correct format
* Adjust python recommendation endpoint (#161)
* Linter  solutions
* Linter error solutions
* Linter error solution
* Automatic update of dependency thoth-storages from 0.0.33 to 0.1.0
* Including all the possible artifacts and corrected space checks
* Including all the possible artifacts
* adding more values to log_info param
* Introduce initial recommendation endpoints (#114)
* Do not restrict logging of user endpoints (#158)
* Automatic update of dependency pylint from 1.9.2 to 2.0.0
* Use Prometheus host and port environment variables when running analyzer
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* relocked
* Automatic update of dependency pytest from 3.6.2 to 3.6.3
* Update .zuul.yaml
* Automatic update of dependency thoth-common from 0.0.9 to 0.1.0
* removed pydocstyle
* relocked
* Update deployment-template.yaml
* Use service account token function from thoth-common
* Update .zuul.yaml
* removed some E501, as the max line lenght is 120 now!
* Automatic update of dependency thoth-storages from 0.0.32 to 0.0.33
* Extended Generic log Wrappers
* Do not query OpenShift API in readiness/liveness probes
* fixes #137
* relocked
* Automatic update of dependency thoth-storages from 0.0.29 to 0.0.32
* Automatic update of dependency thoth-common from 0.0.7 to 0.0.9
* Update .zuul.yaml
* Added minlength to swagger.yaml
* Added min lenghth to swagger.yaml
* Update .coafile
* Variable THOTH_CEPH_HOST was renamed
* Move resource definition for buildconfig to proper entry
* added the gate pipeline to the core queue
* fixing a parser error...
* fixing E252
* fixed template names
* bounced version to 0.4.0
* adding linting-only zuul project definition
* fixing coala issues
* added all the stuff we need for coala
* rename ceph_host to s3_endpoint_url
* set resource limits of BC, DC
* Added pagination info in response header
* Changed wrongname in logmodule init
* Rename THOTH_MIDDLEEND_NAMESPACE to THOTH_MIDDLETIER_NAMESPACE
* re-locked Pipenv
* Do not restrict Thoth packages
* Update thoth-common for rsyslog logging
* Propagate rsyslog configuration to pods run
* Add rsyslog logging
* Update issue templates
* Extend liveness probe with Ceph connection check
* Update thoth-storages
* Test to trigger CI
* Test to trigger CI
* Run coala in non-interactive mode
* Run Coala in CI
* Use coala for code checks
* Update thoth-storages
* Remove accidentally committed __pycache__
* we dont use travis-ci at this moment
* Do not restrict image names on API
* Remove the /run endpoint
* Fix wrong argument for pagination
* Bump thoth-storages with new methods
* Introduce listing of analyses for the given runtime environment
* Provide also information about analyzes
* Update thoth-storages
* Handle not found results in the graph database
* Handle forward slashes in image names
* Update thoth-storages
* Get packages found inside a runtime environment
* List runtime environments endpoint
* Fix graph sync endpoint
* Add license headers
* Add proper LICENSE file
* Use capitals in tags
* Use path parameters instead of query where appropriate
* Remove thoth- prefix
* adding the OWNERS file
* humans: let's reclaim our mattermost channelgit st
* Add missing argument for transitive dependencies scan
* Provide an option to disable TLS cert verification in analyzer
* reset ImageStreamTag to :stable, so that we should land in a deployable configuration
* Return 404 if the given document was not found
* humans: let's reclaim our mattermost channelgit st
* APP_MODULE is an ENV of deployment and not buildconfig
* just define imagestream once, moved s2i config into buildconfig rather than .s2i/environment
* adding version string to /readiness and /liveness
* Remove dependencies.yaml
* Introduce force sync options
* Place /sync endpoint to admin section
* HOTIFX :)
* moving more parts from core to user-api
* using same tag...
* Unify output handling
* Service name has changed
* using CentOS7 Python3.6 as a base now, pushing to :latest tag
* fixing image names
* fixed the Jenkins Environment Variable Name to be used for CI namespace
* Respect transition to a new org
* Do not update pip to latest for now
* Assign env vars to the correct container
* Fix parameter naming
* Provide a way to specify registry user and registry password
* Remove setup.py, we use s2i
* last minute fixes
* Remove requirements.txt
* reenabled Mattermost notification on failure
* Git Source Ref must not contain slashes
* ImageStreamTag must not contain slashes
* [WIP] do not trigger build if buildconfig changes, jenkins pipeline is going to reconfigure buildconfigs
* [WIP] initial Jenkinsfile and OpenShift BuildConfig template
* Log POST content on errors
* Update thoth-storages to place files into new Ceph location
* Use common logging facilities
* Remove PV leftover
* Show dropdown with available solvers and analyzers
* Fix wrong variable name naming
* Add secret to the sync job
* Add endpoint for erasing graph database
* Show result count in responses
* Log exceptions
* Instantiate class in try-catch block to capture errors in constructor
* Refactoring, build logs retrieval endpoint
* Expose page parameters in Swagger
* Fix pagination computing
* Submit build logs to Ceph
* Paginate results listings
* Update thoth-storages package with new adapters
* Add endpoints for Ceph access
* Provide a way to request syncing observations
* Fix function name collisions
* Be consistent with pod id naming in responses
* Do not shadow already existing function
* Rename Requirements to Packages in swagger definitions
* Adjust resource and operation ids
* Dummy change to test github webhooks
* Check for kubernetes master response in liveness probe
* Submit adviser results based on URL to other namespace
* Implement logic around running adviser pod
* Create initial dependencies.yml config
* Fix casting to bool
* Use thoth-common for shared logic
* Rename _do_run() to _do_run_pod() to respect semantics
* Make TLS cert verification for k8s configurable
* Add empty Travis CI configuration
* Rename ANALYZER_NAMESPACE to MIDDLEEND_NAMESPACE
* Implement logic around syncing graph database
* Add function for retrieving cronjobs
* Fix example package name
* Omit "pod" from endpoint names
* Respect new lines in input, encode them for solver
* Adjust solver output endpoint
* Fix packages supplying
* Implement endpoint for running solvers
* Introduce endpoints for manipulating with buildlogs
* Parametrize endpoint hitting with results
* Do not let users browse result-storing API logs
* Add TODO comments
* Add README file
* Introduce pod status endpoint
* Unify pod labeling
* There is no puller container
* Create endpoint for running raw pods
* Define endpoint tags
* Fix resources specification
* Restrict user's access to the pod logs
* Add CPU and memory requests for analyzers
* Rename analysis-log endpoint
* Fix wrong key reference
* Code refactoring
* Be able to supply API token to pod via env variables
* Set CPY and memory limits for spawned pods
* Add .gitignore
* Add TODO comment
* Supply result API hostname to analyzers
* Add endpoint for retrieving analysis logs
* Add endpoint for parsing build logs
* Return pod name as analysis name
* Label thoth analyzers
* Use readiness probe for analyzer hard timeout
* Do not restrict to one image
* Rename supplied env variable
* Replace jobs with pods
* Replace build with a job
* Remove unused configuration entry
* Initial project import

## Release 0.6.2 (2020-06-05T08:56:40)
* Add null check
* Use frozenset for constants
* Be more specific with method signatures
* :green_heart: coala fix
* :ambulance: Ignore kebechet run on push event on bot branch
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* Filter out deprecated event's
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* Changed docstring
* :pushpin: Automatic update of dependency prometheus-client from 0.7.1 to 0.8.0
* Added filter methods and installation methods
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency thoth-storages from 0.22.10 to 0.22.11
* Make integration enum lower-case on endpoints
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* Remove logic
* Adjust typing
* Introduce source_type flag
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.3 to 0.14.4
* :pushpin: Automatic update of dependency thoth-storages from 0.22.9 to 0.22.10
* Remove unused environment variable

## Release 0.6.3 (2020-06-24T17:04:51)
* Adding sesheta as a maintainer
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.2.1 to 3.3.1
* :arrow_up: update github project templates
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.4 to 0.15.1
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency thoth-storages from 0.23.0 to 0.23.2
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.11 to 0.13.12
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.13.0 to 0.14.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.23.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.10 to 0.13.11
* :pushpin: Automatic update of dependency thoth-common from 0.13.9 to 0.13.10
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.9
* Fix serialization issues
* Lower letters
* Also listen to installation events

## Release 0.6.4 (2020-06-24T20:00:39)
* :pushpin: Automatic update of dependency thoth-storages from 0.23.2 to 0.24.0

## Release 0.6.5 (2020-06-25T18:00:15)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* User upper
* User-API response requires string not enum

## Release 0.6.6 (2020-07-02T22:44:18)
* Fixed pre-commit errors
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.0
* Update OWNERS
* Remove OpenShift related files as they are part of thoth-application
* Invalid credentials are a special type of image error
* Drop result-api bits
* switching to pre-commit (#943)
* Update OWNERS
* Update OWNERS

## Release 0.6.7 (2020-07-14T07:50:20)
* :pushpin: Automatic update of dependency sentry-sdk from 0.15.1 to 0.16.1
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.3
* :pushpin: Automatic update of dependency thoth-common from 0.14.0 to 0.14.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.14.1 to 0.15.0

## Release 0.6.8 (2020-07-15T15:45:38)
* Release of version 0.6.7 (#960)
* :pushpin: Automatic update of dependency sentry-sdk from 0.15.1 to 0.16.1
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.3
* :pushpin: Automatic update of dependency thoth-common from 0.14.0 to 0.14.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.14.1 to 0.15.0
* Release of version 0.6.6
* Fixed pre-commit errors
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.0
* Update OWNERS
* Remove OpenShift related files as they are part of thoth-application
* Invalid credentials are a special type of image error
* Drop result-api bits
* switching to pre-commit (#943)
* Update OWNERS
* Update OWNERS
* Release of version 0.6.5
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* User upper
* User-API response requires string not enum
* Release of version 0.6.4
* :pushpin: Automatic update of dependency thoth-storages from 0.23.2 to 0.24.0
* Release of version 0.6.3
* Adding sesheta as a maintainer
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.2.1 to 3.3.1
* :arrow_up: update github project templates
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.4 to 0.15.1
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency thoth-storages from 0.23.0 to 0.23.2
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.11 to 0.13.12
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.13.0 to 0.14.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.23.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.10 to 0.13.11
* :pushpin: Automatic update of dependency thoth-common from 0.13.9 to 0.13.10
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.9
* Fix serialization issues
* Lower letters
* Also listen to installation events
* Release of version 0.6.2
* Add null check
* Use frozenset for constants
* Be more specific with method signatures
* :green_heart: coala fix
* :ambulance: Ignore kebechet run on push event on bot branch
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* Filter out deprecated event's
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* Changed docstring
* :pushpin: Automatic update of dependency prometheus-client from 0.7.1 to 0.8.0
* Added filter methods and installation methods
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency thoth-storages from 0.22.10 to 0.22.11
* Make integration enum lower-case on endpoints
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* Remove logic
* Adjust typing
* Introduce source_type flag
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.3 to 0.14.4
* :pushpin: Automatic update of dependency thoth-storages from 0.22.9 to 0.22.10
* Release of version 0.6.1
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* make coala happy
* fix key error state
* Remove unused environment variable
* :pushpin: Automatic update of dependency thoth-storages from 0.22.8 to 0.22.9
* Use correct keys
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* Moved serialization to common.
* Added event for gitlab
* Fixed coala err
* Handle Github Webhooks
* condition for argo check before workflow status check
* :pushpin: Automatic update of dependency thoth-storages from 0.22.7 to 0.22.8
* :pushpin: Automatic update of dependency connexion from 2.6.0 to 2.7.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* Consumes whole payload
* Added a route to receive webhook
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* Add platform information to OpenAPI spec
* :pushpin: Automatic update of dependency thoth-python from 0.9.1 to 0.9.2
* Add filters for python packages count
* Pin grpcio to <1.28
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* Remove latest version restriction from .thoth.yaml
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* Increase resources for build even more
* Increase memory requirements for the s2i build
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.2 to 1.28.1
* :pushpin: Automatic update of dependency grpcio from 1.27.2 to 1.28.1
* :pushpin: Automatic update of dependency flask from 1.1.1 to 1.1.2
* Distinguish debug option when accessing the cache for provenance results
* Make GitHub events parameters options to the cache
* :pushpin: Automatic dependency re-locking
* Remove variable not required
* Missing exception import
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.2 to 1.28.0
* :pushpin: Automatic update of dependency grpcio from 1.27.2 to 1.28.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.5 to 0.22.7
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.5
* Introduce adviser's dev flag to consider or not consider dev dependencies
* Configure logging for access log
* :pushpin: Automatic update of dependency thoth-common from 0.12.0 to 0.12.1
* removed these unused files
* fixed a typo
* introduced a service version string that contains the depending module's versions
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.2 to 0.14.3
* :pushpin: Automatic update of dependency thoth-storages from 0.22.3 to 0.22.5
* Changed to fix thamos error
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* Add env variable to use Argo
* Fix for GraphDatabase has no attribute get_python_package_index_urls
* Issue check on not found (404)
* :pushpin: Automatic update of dependency pytest from 5.4.0 to 5.4.1
* :pushpin: Automatic update of dependency pytest from 5.3.5 to 5.4.0
* Return Pending state if wf doesn't have a phase set
* Get status of an adviser run from a Workflow
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.2 to 0.13.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.2 to 0.13.0
* Remove check on graph initialization
* Set image pull policy to always
* Add missing import
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.1 to 0.14.2
* Fallback if thoth fails to give advise in bc
* :pushpin: Automatic update of dependency thoth-storages from 0.22.2 to 0.22.3
* fixed coala errors
* changed condition
* Reverted back
* Advise route fix
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* Correct datatype
* :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency grpcio-tools from 1.27.1 to 1.27.2
* :pushpin: Automatic update of dependency grpcio from 1.27.1 to 1.27.2
* :pushpin: Automatic update of dependency thoth-storages from 0.22.1 to 0.22.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.0 to 0.22.1
* :pushpin: Automatic update of dependency thoth-storages from 0.21.11 to 0.22.0
* Update .thoth.yaml
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency grpcio-tools from 1.26.0 to 1.27.1
* :pushpin: Automatic update of dependency grpcio from 1.26.0 to 1.27.1
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic dependency re-locking
* Modify post_advise
* remove revision
* Modify parameters for GitHub App
* :pushpin: Automatic update of dependency grpcio-tools from 1.26.0 to 1.27.0
* :pushpin: Automatic update of dependency grpcio from 1.26.0 to 1.27.0
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* Moved common parameters to components
* Introduce env var for Thoth host
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* Use string for env variable
* POST endpoint accepts input body
* Add missing import
* :pushpin: Automatic update of dependency connexion from 2.5.1 to 2.6.0
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* Add endpoint exposing package dependencies
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* standardize parameters for GitHubApp workflow scheduling
* Add GitHub specific metadata for GitHub integration
* Added handlin to user facing function
* Fixed coala errors
* Added an extra exception catch
* :pushpin: Automatic update of dependency thoth-storages from 0.21.10 to 0.21.11
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* Add responses
* Correct wrong datatype
* Add temporary variable to use Argo workflow
* New Endpoint to schedule Thamos Advise workflow for QebHwt
* :pushpin: Automatic update of dependency sentry-sdk from 0.14.0 to 0.14.1
* :pushpin: Automatic update of dependency thoth-storages from 0.21.9 to 0.21.10
* :pushpin: Automatic update of dependency thoth-storages from 0.21.8 to 0.21.9
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-storages from 0.21.7 to 0.21.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* Added nullables to Runtime Environment properties
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.27 to 0.9.28
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.27
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.7 to 0.1.8
* :pushpin: Automatic update of dependency thoth-storages from 0.21.6 to 0.21.7
* :pushpin: Automatic update of dependency jaeger-client from 4.2.0 to 4.3.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency thoth-storages from 0.21.5 to 0.21.6
* use build-report instead of build-analyze
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency thoth-storages from 0.21.4 to 0.21.5
* :pushpin: Automatic update of dependency thoth-storages from 0.21.3 to 0.21.4
* :pushpin: Automatic update of dependency thoth-storages from 0.21.2 to 0.21.3
* :pushpin: Automatic update of dependency thoth-storages from 0.21.1 to 0.21.2
* :pushpin: Automatic update of dependency thoth-storages from 0.21.0 to 0.21.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* :pushpin: Automatic update of dependency thoth-storages from 0.20.6 to 0.21.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-python from 0.8.0 to 0.9.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.5 to 0.14.0
* :pushpin: Automatic update of dependency thoth-storages from 0.20.5 to 0.20.6
* Do not run adviser from bc in debug mode
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* :pushpin: Automatic update of dependency thoth-storages from 0.20.4 to 0.20.5
* :pushpin: Automatic update of dependency thoth-python from 0.7.1 to 0.8.0
* :pushpin: Automatic update of dependency thoth-storages from 0.20.3 to 0.20.4
* :pushpin: Automatic update of dependency thoth-storages from 0.20.2 to 0.20.3
* :pushpin: Automatic update of dependency thoth-storages from 0.20.1 to 0.20.2
* Happy new year!
* :pushpin: Automatic update of dependency thoth-storages from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.30 to 0.20.0
* :pushpin: Automatic update of dependency connexion from 2.5.0 to 2.5.1
* :pushpin: Automatic update of dependency grpcio-tools from 1.25.0 to 1.26.0
* :pushpin: Automatic update of dependency grpcio from 1.25.0 to 1.26.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.27 to 0.19.30
* :pushpin: Automatic update of dependency connexion from 2.4.0 to 2.5.0
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.6 to 0.1.7
* Provide is_s2i flag on user API
* Use RHEL instead of UBI
* Update Thoth configuration file and Thoth's s2i configuration
* Connect to database lazily, after fork
* :pushpin: Automatic update of dependency thoth-storages from 0.19.26 to 0.19.27
* :pushpin: Automatic update of dependency thoth-storages from 0.19.25 to 0.19.26
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.5 to 0.1.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* Two new endpoints
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.11.0 to 0.12.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.24 to 0.19.25
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.19
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.4 to 0.1.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency jaeger-client from 4.1.0 to 4.2.0
* :pushpin: Automatic update of dependency gunicorn from 20.0.3 to 20.0.4
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency gunicorn from 20.0.2 to 20.0.3
* :pushpin: Automatic update of dependency sentry-sdk from 0.13.2 to 0.13.3
* :pushpin: Automatic update of dependency gunicorn from 20.0.0 to 20.0.2
* :pushpin: Automatic update of dependency thoth-storages from 0.19.23 to 0.19.24
* :green_heart: updated some kinds, apiVersions
* :pushpin: Automatic update of dependency thoth-storages from 0.19.22 to 0.19.23
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* Add sentry-sdk[flask] for Sentry Flask integration
* Add aiocontextvars for sentry-sdk integration with aiohttp
* :green_heart: fixed the type
* Added headers to response
* :pushpin: Automatic update of dependency thoth-storages from 0.19.19 to 0.19.22
* New endpoints for Python packages in Thoth Knowledge Graph
* Correct output for error response for all queries
* Correct error response output
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* Maintain one graph datababase adapter instance also in health checks
* Instantiate one adapter per wsgi worker
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* :pushpin: Automatic update of dependency thoth-storages from 0.19.18 to 0.19.19
* Track only user endpoints
* List only enabled Python package indexes to users
* :pushpin: Automatic update of dependency gunicorn from 19.9.0 to 20.0.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.17 to 0.19.18
* :pushpin: Automatic update of dependency thoth-python from 0.6.5 to 0.7.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.15 to 0.19.17
* Fix redirect to Swagger UI to make it work
* Always parse runtime environment before submitting to adviser
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.3 to 1.25.0
* :pushpin: Automatic update of dependency grpcio from 1.24.3 to 1.25.0
* :pushpin: Automatic update of dependency thoth-storages from 0.19.14 to 0.19.15
* :pushpin: Automatic update of dependency thoth-storages from 0.19.13 to 0.19.14
* :pushpin: Automatic update of dependency thoth-storages from 0.19.12 to 0.19.13
* Update queries according to standardize naming convention
* updated templates with annotations and param thoth-advise-value
* Fix offset to start_offset
* use github webhook variable html_url
* Catch exception when database is not initialized
* :pushpin: Automatic update of dependency thoth-storages from 0.19.11 to 0.19.12
* :pushpin: Automatic update of dependency thoth-storages from 0.19.10 to 0.19.11
* Fix issue when overwriting parameters
* :pushpin: Automatic update of dependency pytest from 5.2.1 to 5.2.2
* Do not introduce fatal fail if database schema was removed
* Redirect to HTTPS instead of HTTP if configured so
* Fix entrypoint - remove old entrypoint
* Check if database schema is up2date in readiness probe
* Remove Info
* Remove Dgraph memories
* Make coala happy
* Set is_external to False explicitly
* Remove is_external from api_v1.py
* Removed is_external
* Fix typo
* Return parameters
* Add software & hardware environment listing
* Add missing properties to User API
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.1 to 1.24.3
* :pushpin: Automatic update of dependency grpcio from 1.24.1 to 1.24.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.9 to 0.19.10
* :pushpin: Automatic update of dependency thoth-python from 0.6.4 to 0.6.5
* :pushpin: Automatic update of dependency connexion from 2.3.0 to 2.4.0
* Fix component reference in openapi
* Report 404 if no metadata are found for the given package
* :sparkles: added a PR template
* [Feature] Get metadata for a Python package
* :pushpin: Automatic update of dependency attrs from 19.2.0 to 19.3.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-python from 0.6.3 to 0.6.4
* Provide is_external flag to package-extract runs explictly
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* :pushpin: Automatic update of dependency pytest from 5.2.0 to 5.2.1
* :sparkles: bounce the version to 0.6.0-dev
* :pushpin: Automatic update of dependency grpcio-tools from 1.24.0 to 1.24.1
* :pushpin: Automatic update of dependency grpcio from 1.24.0 to 1.24.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.10.0 to 0.11.0
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.2.0 to 3.2.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* :pushpin: Automatic update of dependency attrs from 19.1.0 to 19.2.0
* add pipfile lock
* Made changes
* fixing cors issue
* :pushpin: Automatic update of dependency thoth-storages from 0.19.8 to 0.19.9
* :pushpin: Automatic update of dependency pytest from 5.1.3 to 5.2.0
* Add Thoth version information to each response
* Delete Info
* :pushpin: Automatic update of dependency thoth-storages from 0.19.7 to 0.19.8
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.3 to 0.1.4
* Be more safe when parsing webhook payload
* Remove unused function - log parsing has been moved to async handling
* :pushpin: Automatic update of dependency grpcio-tools from 1.23.0 to 1.24.0
* :pushpin: Automatic update of dependency grpcio from 1.23.0 to 1.24.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.9.1 to 0.10.0
* updated cpu and memory allocation
* :pushpin: Automatic update of dependency thoth-storages from 0.19.6 to 0.19.7
* use postgresql hostname from thoth configmap
* :pushpin: Automatic update of dependency thoth-python from 0.6.2 to 0.6.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.5 to 0.19.6
* Check PostgreSQL in liveness or readiness probe
* :pushpin: Automatic update of dependency pytest from 5.1.2 to 5.1.3
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.2 to 0.1.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency thoth-storages from 0.19.4 to 0.19.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* :pushpin: Automatic update of dependency thoth-storages from 0.19.3 to 0.19.4
* :pushpin: Automatic update of dependency thoth-storages from 0.19.2 to 0.19.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.1 to 0.19.2
* :pushpin: Automatic update of dependency thoth-storages from 0.19.0 to 0.19.1
* :pushpin: Automatic update of dependency thoth-storages from 0.18.6 to 0.19.0
* :pushpin: Automatic update of dependency thoth-python from 0.6.1 to 0.6.2
* Use more generic env var names
* Switch from Dgraph to PostgreSQL in deployment
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.1.1 to 3.2.0
* :pushpin: Automatic update of dependency jaeger-client from 4.0.0 to 4.1.0
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* Start using Thoth's s2i base image
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* :pushpin: Automatic update of dependency grpcio-tools from 1.22.0 to 1.23.0
* :pushpin: Automatic update of dependency grpcio from 1.22.1 to 1.23.0
* :pushpin: Automatic update of dependency grpcio from 1.22.0 to 1.22.1
* Use singular to be compatible with other endpoints
* Provide endpoint for listing supported runtime environments
* :pushpin: Automatic update of dependency thoth-storages from 0.18.5 to 0.18.6
* Added config
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* Initial dependency lock
* Runtime environment is now reported on the project instance
* Stop using extras in thoth-common
* Wrong URLs
* :pushpin: Automatic update of dependency thoth-storages from 0.18.4 to 0.18.5
* :pushpin: Automatic update of dependency thoth-python from 0.6.0 to 0.6.1
* Remove old .thoth.yaml configuration file
* Change name of Thoth template to make Coala happy
* Start using Thoth in OpenShift's s2i
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-storages from 0.18.3 to 0.18.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* Enforce new invectio version by providing required schema
* Remove anchors and use refs instead
* Add information comming from Jupyter Notebooks
* :pushpin: Automatic update of dependency thoth-storages from 0.18.1 to 0.18.3
* :pushpin: Automatic update of dependency thoth-storages from 0.18.0 to 0.18.1
* :pushpin: Automatic update of dependency thoth-storages from 0.17.0 to 0.18.0
* :pushpin: Automatic update of dependency thoth-storages from 0.16.0 to 0.17.0
* :pushpin: Automatic update of dependency thoth-storages from 0.14.8 to 0.16.0
* :pushpin: Automatic update of dependency thoth-python from 0.5.0 to 0.6.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.5
* Removed thoth-build-analyzers dependencies from user-api
* :sunrise: Modified the names to standard convention
* :dolphin: user-api support for build analysis and build log analysis
* Changed based on review
* Explicitly state python type
* :pushpin: Automatic update of dependency thoth-storages from 0.14.7 to 0.14.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* :pushpin: Automatic update of dependency thoth-storages from 0.14.6 to 0.14.7
* Added error return value for pagure
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* :pushpin: Automatic update of dependency thoth-storages from 0.14.5 to 0.14.6
* :pushpin: Automatic update of dependency thoth-storages from 0.14.4 to 0.14.5
* :pushpin: Automatic update of dependency flask from 1.1.0 to 1.1.1
* :star: python black linting and styling fixes
* updated the deprecated version check
* Error code return values
* :pushpin: Automatic update of dependency thoth-storages from 0.14.3 to 0.14.4
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency opentracing-instrumentation from 3.0.1 to 3.1.1
* :pushpin: Automatic update of dependency flask from 1.0.4 to 1.1.0
* :pushpin: Automatic update of dependency flask from 1.0.3 to 1.0.4
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency thoth-storages from 0.14.1 to 0.14.3
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.1
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.8.1 to 0.9.0
* :pushpin: Automatic update of dependency prometheus-client from 0.7.0 to 0.7.1
* :pushpin: Automatic update of dependency grpcio-tools from 1.21.1 to 1.22.0
* :pushpin: Automatic update of dependency grpcio from 1.21.1 to 1.22.0
* Changed variable name
* /kebechet endpoint works
* Addition
* Interface with thoth-common kebechet scheduler
* Update the trigger-build job to use the latest job API
* :pushpin: Automatic update of dependency connexion from 2.2.0 to 2.3.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.8.0 to 0.8.1
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* Metrics are available for Prometheus and grouped by endpoint
* :pushpin: Automatic update of dependency prometheus-client from 0.6.0 to 0.7.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency thoth-storages from 0.14.0 to 0.14.1
* Internal Error Connection due to attributes
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency thoth-storages from 0.11.4 to 0.14.0
* Update Pipfile.lock
* Handle workload registered state
* Migrate parsing API to thoth-build-analysers
* :pushpin: Automatic update of dependency grpcio-tools from 1.20.1 to 1.21.1
* :pushpin: Automatic update of dependency grpcio from 1.20.1 to 1.21.1
* Typos corrected
* Correct metric info
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.4 to 0.8.0
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.3 to 0.7.4
* Modified endpoints
* Update functions for user API
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.2 to 0.7.3
* :pushpin: Automatic update of dependency flask from 1.0.2 to 1.0.3
* :pushpin: Automatic update of dependency requests from 2.21.0 to 2.22.0
* :wrench: minor fix template for openshift >=3.11
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency thoth-storages from 0.11.3 to 0.11.4
* :pushpin: Automatic update of dependency thoth-storages from 0.11.2 to 0.11.3
* Fix method names, provide image names only once
* Do not convert datetimes, keep them as strings
* Consolidate endpoints for buildtime and runtime analyses
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency thoth-storages from 0.11.1 to 0.11.2
* Implement User API using Stub API template
* Add library usage parameter to adviser's API
* :pushpin: Automatic update of dependency thoth-storages from 0.11.0 to 0.11.1
* :bug: convert set to a list, so that it is json serializable
* Fix env variable name of Dgraph instance in info endpoint
* :pushpin: Automatic update of dependency thoth-storages from 0.10.0 to 0.11.0
* Adjust deployment to respect new Dgraph configuration
* :sparkles: added required ENV
* :sparkles: added mounting the Dgraph TLS secrets
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.7.1 to 0.7.2
* Switch to Dgraph
* :pushpin: Automatic update of dependency thoth-storages from 0.9.7 to 0.10.0
* :pushpin: Automatic update of dependency pytest from 4.4.0 to 4.4.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* Introduce environment type parameter for image analysis
* Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* Return Bad Request for invalid format request
* Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* Remove pylint zuul job
* Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* Automatic update of dependency prometheus-flask-exporter from 0.7.0 to 0.7.1
* Automatic update of dependency pytest from 4.3.1 to 4.4.0
* Automatic update of dependency prometheus-flask-exporter from 0.6.0 to 0.7.0
* Automatic update of dependency thoth-storages from 0.9.6 to 0.9.7
* Automatic update of dependency thoth-python from 0.4.6 to 0.5.0
* Add Thoth's configuration file
* Automatic update of dependency thoth-common from 0.7.1 to 0.8.1
* Fix requirements so that updates are possible
* :bookmark: bouncing swagger api version to 0.4.0
* reworked the service account part
* remove unused stuff
* Fix wrong pop
* Expose parameter for limiting number of latest versions
* Increase memory requests in deployment
* Set WARNING level before the actual handler function
* Automatic update of dependency pytest from 4.2.1 to 4.3.0
* Automatic update of dependency prometheus-client from 0.5.0 to 0.6.0
* Introduce origin parameter
* Adjust description to respect semantics
* Expose deployment specific configuration to users
* Report unknown errors happening during image extraction
* Fix issues with Pipfile in s2i
* Place runtime environment specification into a standalone model
* Adjustments to respect Thoth configuration
* Use Python 3.6 by default
* It's already 2019
* Fix wrong operator
* Change order of parameters to skopeo
* Skopeo flag for TLS verification has changed
* State hash type in description
* Introduce endpoint for gathering image information based on image digest
* Make image analysis endpoint work again
* Fix typo in method name
* Fix return value in function signature
* Return 404 in status endpoints if the given analysis id was not found
* Rename method to reflect its semantics
* Schedule workload instead of directly running it
* Cache should also distinguish recommendation type
* Pop supplied input
* Fix key error
* Respect signature of function, return a tuple
* Avoid circular JSONs on error response
* Automatic update of dependency requests from 2.20.1 to 2.21.0
* Automatic update of dependency prometheus-flask-exporter from 0.4.0 to 0.4.1
* Automatic update of dependency prometheus-client from 0.4.2 to 0.5.0
* Update thoth-python to avoid attribute errors
* Update thoth-storages to include Amun client dependency
* Dependency locking
* Implement cache for adviser runs
* Update dependencies, let Kebechet do relocking
* Fixes to make things work
* Introduce cache in provenance checks
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency thoth-storages from 0.8.0 to 0.9.0
* added prometheus metric export for all things REST
* added a pyproject.toml to keep black happy
* added prometheus
* Automatic update of dependency pytest from 4.0.0 to 4.0.1
* Be more precise with swagger model examples
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Expose available Python package indexes on API
* Provide runtime environment as a JSON
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Introduce count and limit on API for advise
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Extras are not markers
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Extras are not markers
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Automatic update of dependency thoth-storages from 0.7.6 to 0.8.0
* Automatic update of dependency connexion from 2.0.1 to 2.0.2
* Automatic update of dependency pytest from 3.10.1 to 4.0.0
* Extras are not markers
* Markers are not extras
* fixing markers/extra
* Automatic update of dependency pytest from 3.10.0 to 3.10.1
* fixing markers/extra
* Automatic update of dependency requests from 2.20.0 to 2.20.1
* Extras are not markers
* Automatic update of dependency thoth-storages from 0.7.5 to 0.7.6
* Automatic update of dependency thoth-storages from 0.7.4 to 0.7.5
* Markers are not extras
* Markers are not extras
* Automatic update of dependency connexion from 2.0.0 to 2.0.1
* Update buildConfig-template.yaml
* Automatic update of dependency thoth-storages from 0.7.2 to 0.7.4
* added HistoryLimits to BuildConfig
* fixed
* Update .zuul.yaml
* Update .zuul.yaml
* Update .zuul.yaml
* New connexion requires swagger-ui extras
* Extras are not markers
* updated to use the latest token (recreated after last reprovisioning of thoth)
* updated to use the latest token (recreated after last reprovisioning of thoth)
* actually do --insecure-skip-tls-verify
* fixed errors
* fixed errors
* fixed errors
* OpenShift are not markers but extras
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* OpenShift are not markers but extras
* Automatic update of dependency pytest from 3.9.3 to 3.10.0
* working on redeployment
* using skopeo to pull image
* corrected the label name
* ...
* added thoth-ops SA secret
* Fix dependency name
* fixed coala errors
* Markers are not extras
* Add missing attr dependency
* we dont have a nodeset defined for it yet, lets create it here.
* 1. redeploy after build finished, 2. push image to upstream registry
* started a job that will redeploy user-api to a given OpenShift project
* fixed coala errors
* using thoth zuul jobs now
* Amun and dependency monkey is not used by user API
* Remove unused secret
* Remove endpoints that were moved to management API
* Clear unused dependencies
* Frontend namespace is set from configmap
* Move user API under thoth directory
* Update thoth-storages to 0.7.2
* Provenance checks will be cached as well
* Implement caching of package-extract results
* Update thoth-common and thoth-storages
* Fix parameter name
* Extras are not markers
* Fix key error when gathering pod status
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Report issues using status codes
* Implement metadata gathering for images
* Do not propagate force to actual package-extract run
* Do not propagate force to analysis run
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Automatic dependency re-locking
* Automatic update of dependency pytest from 3.9.1 to 3.9.2
* Automatic update of dependency thoth-storages from 0.5.4 to 0.6.0
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* Automatic update of dependency requests from 2.19.1 to 2.20.0
* Automatic update of dependency pytest from 3.8.2 to 3.9.1
* Amun API is URL not host
* Respect dependency monkey output configuration
* Introduce cached results of analyses
* Revert "Use TLS in route", it resulted in an unavailable Web UI.
* fixing some misformatted lines
* minor fixes
* Automatic update of dependency thoth-storages from 0.5.3 to 0.5.4
* Automatic update of dependency thoth-storages from 0.5.2 to 0.5.3
* Automatic update of dependency thoth-common from 0.3.10 to 0.3.11
* using envvar that are injected by OpenShift to discover janusgraph servcie host and port
* added THOTH_JANUSGRAPH_{HOST|POST} as template parameters
* Automatic update of dependency thoth-common from 0.3.9 to 0.3.10
* Fix typo in argument name
* Logs can be nullable
* Fix CI
* Use TLS in route
* fixed the template name
* split out the imagestream into his own template
* Automatic update of dependency thoth-common from 0.3.8 to 0.3.9
* Automatic update of dependency thoth-common from 0.3.7 to 0.3.8
* Fix status gathering
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.7
* Move from Pods to Jobs
* Fix linter complains
* Introduce dependency monkey endpoints
* Add skopeo binary
* Automatic update of dependency pytest from 3.8.1 to 3.8.2
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Fix gathering pod status
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Fix CI complains
* State nullable values in swagger
* Fix reStructuredText issues
* fixed linter errors
* now the ImageStreamTag to be deployed can pe configured via a parameter, default is "latest"
* added a badge
* fixed the badge
* Revert "Add a Codacy badge to README.rst"
* Update README file
* Automatic update of dependency pytest from 3.8.0 to 3.8.1
* Gathering status report moved to common
* Remove unused import
* Fix retrieving documents on wrong endpoint
* Remove 400 responses where not needed
* Provide custom error handlers with more information
* Fix analysis listing model
* Fix linter
* Allow empty lock to be submitted
* Automatic update of dependency thoth-common from 0.3.0 to 0.3.1
* Comment out nullable values due to incompatibility
* Container SHA can be null when analysis is pending
* Fix status response definition
* Remove underscore in cotainer name in response
* Fix parameter name
* Add response schemas to swagger definitions
* Automatic update of dependency connexion from 1.5.2 to 1.5.3
* Signalize user if no solvers were run
* Automatic update of dependency pytest from 3.7.4 to 3.8.0
* Rename recommend to advise all over the places
* Enhance reporting issues when gathering documents to user
* Expose provenance debug option on API
* Fix built-in type shadowing
* Automatic update of dependency thoth-common from 0.2.7 to 0.3.0
* Fix parameter name
* Notify user about running analyses if results are not ready yet
* Report user timeout issues with long-running analyses
* Refactor API to reflect current functionality
* better formating
* removed, as we use Zuul for gating
* Add Codacy badge
* Remove accidentally duplicated function
* Add Codacy badge
* Fix method name
* Code refactoring and always replying parameters
* Automatic update of dependency thoth-common from 0.2.6 to 0.2.7
* Implement provenance checker run
* Introduce provenance endpoint
* Automatic update of dependency thoth-common from 0.2.5 to 0.2.6
* better formating
* Automatic update of dependency thoth-storages from 0.5.1 to 0.5.2
* better formating
* nano fixed
* change the queue
* Provide frontend namespace configuration
* Automatic update of dependency attrs from 18.1.0 to 18.2.0
* Automatic update of dependency thoth-common from 0.2.4 to 0.2.5
* Automatic update of dependency pytest from 3.7.3 to 3.7.4
* Initial dependency lock
* Let Kebechet lock dependencies
* OpenShift and K8s are no longer direct deps
* Automatic update of dependency thoth-storages from 0.5.0 to 0.5.1
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Automatic update of dependency pytest from 3.7.1 to 3.7.3
* Automatic update of dependency kubernetes from 6.0.0 to 7.0.0
* Automatic update of dependency thoth-storages from 0.4.0 to 0.5.0
* Automatic update of dependency thoth-storages from 0.3.0 to 0.4.0
* Automatic update of dependency thoth-storages from 0.2.0 to 0.3.0
* Automatic update of dependency thoth-storages from 0.1.1 to 0.2.0
* Configuration is now available via env vars
* Remove unused entries from configuration
* Use OpenShift object from thoth-common
* Tweak running adviser
* Automatic update of dependency pylint from 2.1.0 to 2.1.1
* Initial dependency lock
* @sesheta please relock
* Add endpoint for listing adviser results
* Label graph sync job triggered by user
* Use OpenShift as a naming service
* Increase memory for user-api
* Automatic update of dependency pylint from 2.0.1 to 2.1.0
* Automatic update of dependency pytest from 3.6.4 to 3.7.0
* Increase memory otherwise container exits on os error 14
* Disable HTTP request logs (#168)
* Automatic update of dependency thoth-common from 0.2.1 to 0.2.2
* Automatic update of dependency pytest from 3.6.3 to 3.6.4
* Automatic update of dependency thoth-storages from 0.1.0 to 0.1.1
* Automatic update of dependency connexion from 1.5.1 to 1.5.2
* Fix label 2
* Fix label
* Adjust template labels (#166)
* new templates
* Automatic update of dependency pytest-timeout from 1.3.0 to 1.3.1
* Automatic update of dependency pylint from 2.0.0 to 2.0.1
* Automatic update of dependency connexion from 1.4.2 to 1.5.1
* increasing the requested resources
* Use default port for services
* modified message in example to correct format
* Adjust python recommendation endpoint (#161)
* Linter  solutions
* Linter error solutions
* Linter error solution
* Automatic update of dependency thoth-storages from 0.0.33 to 0.1.0
* Including all the possible artifacts and corrected space checks
* Including all the possible artifacts
* adding more values to log_info param
* Introduce initial recommendation endpoints (#114)
* Do not restrict logging of user endpoints (#158)
* Automatic update of dependency pylint from 1.9.2 to 2.0.0
* Use Prometheus host and port environment variables when running analyzer
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* relocked
* Automatic update of dependency pytest from 3.6.2 to 3.6.3
* Update .zuul.yaml
* Automatic update of dependency thoth-common from 0.0.9 to 0.1.0
* removed pydocstyle
* relocked
* Update deployment-template.yaml
* Use service account token function from thoth-common
* Update .zuul.yaml
* removed some E501, as the max line lenght is 120 now!
* Automatic update of dependency thoth-storages from 0.0.32 to 0.0.33
* Extended Generic log Wrappers
* Do not query OpenShift API in readiness/liveness probes
* fixes #137
* relocked
* Automatic update of dependency thoth-storages from 0.0.29 to 0.0.32
* Automatic update of dependency thoth-common from 0.0.7 to 0.0.9
* Update .zuul.yaml
* Added minlength to swagger.yaml
* Added min lenghth to swagger.yaml
* Update .coafile
* Variable THOTH_CEPH_HOST was renamed
* Move resource definition for buildconfig to proper entry
* added the gate pipeline to the core queue
* fixing a parser error...
* fixing E252
* fixed template names
* bounced version to 0.4.0
* adding linting-only zuul project definition
* fixing coala issues
* added all the stuff we need for coala
* rename ceph_host to s3_endpoint_url
* set resource limits of BC, DC
* Added pagination info in response header
* Changed wrongname in logmodule init
* Rename THOTH_MIDDLEEND_NAMESPACE to THOTH_MIDDLETIER_NAMESPACE
* re-locked Pipenv
* Do not restrict Thoth packages
* Update thoth-common for rsyslog logging
* Propagate rsyslog configuration to pods run
* Add rsyslog logging
* Update issue templates
* Extend liveness probe with Ceph connection check
* Update thoth-storages
* Test to trigger CI
* Test to trigger CI
* Run coala in non-interactive mode
* Run Coala in CI
* Use coala for code checks
* Update thoth-storages
* Remove accidentally committed __pycache__
* we dont use travis-ci at this moment
* Do not restrict image names on API
* Remove the /run endpoint
* Fix wrong argument for pagination
* Bump thoth-storages with new methods
* Introduce listing of analyses for the given runtime environment
* Provide also information about analyzes
* Update thoth-storages
* Handle not found results in the graph database
* Handle forward slashes in image names
* Update thoth-storages
* Get packages found inside a runtime environment
* List runtime environments endpoint
* Fix graph sync endpoint
* Add license headers
* Add proper LICENSE file
* Use capitals in tags
* Use path parameters instead of query where appropriate
* Remove thoth- prefix
* adding the OWNERS file
* humans: let's reclaim our mattermost channelgit st
* Add missing argument for transitive dependencies scan
* Provide an option to disable TLS cert verification in analyzer
* reset ImageStreamTag to :stable, so that we should land in a deployable configuration
* Return 404 if the given document was not found
* humans: let's reclaim our mattermost channelgit st
* APP_MODULE is an ENV of deployment and not buildconfig
* just define imagestream once, moved s2i config into buildconfig rather than .s2i/environment
* adding version string to /readiness and /liveness
* Remove dependencies.yaml
* Introduce force sync options
* Place /sync endpoint to admin section
* HOTIFX :)
* moving more parts from core to user-api
* using same tag...
* Unify output handling
* Service name has changed
* using CentOS7 Python3.6 as a base now, pushing to :latest tag
* fixing image names
* fixed the Jenkins Environment Variable Name to be used for CI namespace
* Respect transition to a new org
* Do not update pip to latest for now
* Assign env vars to the correct container
* Fix parameter naming
* Provide a way to specify registry user and registry password
* Remove setup.py, we use s2i
* last minute fixes
* Remove requirements.txt
* reenabled Mattermost notification on failure
* Git Source Ref must not contain slashes
* ImageStreamTag must not contain slashes
* [WIP] do not trigger build if buildconfig changes, jenkins pipeline is going to reconfigure buildconfigs
* [WIP] initial Jenkinsfile and OpenShift BuildConfig template
* Log POST content on errors
* Update thoth-storages to place files into new Ceph location
* Use common logging facilities
* Remove PV leftover
* Show dropdown with available solvers and analyzers
* Fix wrong variable name naming
* Add secret to the sync job
* Add endpoint for erasing graph database
* Show result count in responses
* Log exceptions
* Instantiate class in try-catch block to capture errors in constructor
* Refactoring, build logs retrieval endpoint
* Expose page parameters in Swagger
* Fix pagination computing
* Submit build logs to Ceph
* Paginate results listings
* Update thoth-storages package with new adapters
* Add endpoints for Ceph access
* Provide a way to request syncing observations
* Fix function name collisions
* Be consistent with pod id naming in responses
* Do not shadow already existing function
* Rename Requirements to Packages in swagger definitions
* Adjust resource and operation ids
* Dummy change to test github webhooks
* Check for kubernetes master response in liveness probe
* Submit adviser results based on URL to other namespace
* Implement logic around running adviser pod
* Create initial dependencies.yml config
* Fix casting to bool
* Use thoth-common for shared logic
* Rename _do_run() to _do_run_pod() to respect semantics
* Make TLS cert verification for k8s configurable
* Add empty Travis CI configuration
* Rename ANALYZER_NAMESPACE to MIDDLEEND_NAMESPACE
* Implement logic around syncing graph database
* Add function for retrieving cronjobs
* Fix example package name
* Omit "pod" from endpoint names
* Respect new lines in input, encode them for solver
* Adjust solver output endpoint
* Fix packages supplying
* Implement endpoint for running solvers
* Introduce endpoints for manipulating with buildlogs
* Parametrize endpoint hitting with results
* Do not let users browse result-storing API logs
* Add TODO comments
* Add README file
* Introduce pod status endpoint
* Unify pod labeling
* There is no puller container
* Create endpoint for running raw pods
* Define endpoint tags
* Fix resources specification
* Restrict user's access to the pod logs
* Add CPU and memory requests for analyzers
* Rename analysis-log endpoint
* Fix wrong key reference
* Code refactoring
* Be able to supply API token to pod via env variables
* Set CPY and memory limits for spawned pods
* Add .gitignore
* Add TODO comment
* Supply result API hostname to analyzers
* Add endpoint for retrieving analysis logs
* Add endpoint for parsing build logs
* Return pod name as analysis name
* Label thoth analyzers
* Use readiness probe for analyzer hard timeout
* Do not restrict to one image
* Rename supplied env variable
* Replace jobs with pods
* Replace build with a job
* Remove unused configuration entry
* Initial project import

## Release 0.6.9 (2020-07-29T21:25:49)
* Fix (#987)
* Source type is nullable (#981)
* Moving changed function (#980)
* Extend recommendation types (#970)
* Changed to new workflow status (#971)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0 (#979)
* :pushpin: Automatic update of dependency sentry-sdk from 0.16.1 to 0.16.2 (#978)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#977)
* :pushpin: Automatic update of dependency sentry-sdk from 0.16.1 to 0.16.2 (#976)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#975)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.15.0 (#974)
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.15.0 to 0.15.4 (#973)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.3 to 0.24.4 (#969)
* Remove limit_latest_versions from API (#968)
* Remove latest versions limitation (#967)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#966)
* Removed un-necessary variable (#964)

## Release 0.6.10 (2020-08-22T16:55:37)
* :pushpin: Automatic update of dependency sentry-sdk from 0.16.2 to 0.16.5 (#1003)
* :pushpin: Automatic update of dependency sentry-sdk from 0.16.2 to 0.16.5 (#1001)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.3 (#1000)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#999)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#998)
* :pushpin: Automatic update of dependency attrs from 19.3.0 to 20.1.0 (#997)
* :pushpin: Automatic update of dependency thoth-common from 0.15.0 to 0.16.0 (#992)
* :pushpin: Automatic update of dependency pytest from 6.0.0 to 6.0.1 (#994)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#993)
* Wrong exception caught (#991)

## Release 0.6.11 (2020-08-26T11:58:30)
* Fix unhandled workflow state in responses (#1009)
* Fix variable reference
* :pushpin: Automatic update of dependency sentry-sdk from 0.16.5 to 0.17.0 (#1008)

## Release 0.6.12 (2020-08-26T13:24:46)
### Features
* Turn on smart changelog to group messages using AI/ML
* Add endpoint for listing supported platforms

## Release 0.6.13 (2020-08-27T20:08:08)
### Features
* Fix mypy complains about typing
* Make black happy again
* Fix obtaining logs when Argo workflows are used
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.0

## Release 0.6.14 (2020-08-29T10:19:11)
### Features
* :arrow_up: relocked
* :sparkles: standard pre-commit-config
### Bug Fixes
* :white_check_mark: some fixes for pre-commit
* Relock dependencies due to Pipenv/Kebechet bug
### Improvements
* :arrow_down: removed the files as they are no longer required

## Release 0.6.15 (2020-08-31T12:03:55)
### Features
* Include service version in response headers (#1034)
### Bug Fixes
* :bug: fixed  pre-commit config file
* Revert ":white_check_mark: some fixes for pre-commit"
### Automatic Updates
* :pushpin: Automatic update of dependency flask-cors from 3.0.8 to 3.0.9 (#1033)

## Release 0.6.16 (2020-09-09T13:12:44)
### Features
* Empty commit to trigger a release
### Automatic Updates
* :pushpin: Automatic update of dependency attrs from 20.1.0 to 20.2.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.2 to 0.17.3
* :pushpin: Automatic update of dependency thoth-common from 0.17.2 to 0.17.3
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.16.4 to 0.17.0
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.1 to 0.17.2 (#1043)
* :pushpin: Automatic update of dependency thoth-common from 0.17.0 to 0.17.2 (#1042)
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.16.0 to 0.16.4 (#1041)

## Release 0.6.17 (2020-09-16T07:50:38)
### Features
* Correct exception type handled
### Improvements
* semantically correct name for qebhwt function (#1057)
### Automatic Updates
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.3 to 0.17.4 (#1056)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.6 (#1055)

## Release 0.6.18 (2020-09-24T17:01:19)
### Automatic Updates
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.6 to 0.17.8 (#1078)
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.6 to 0.17.8 (#1074)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#1076)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#1075)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.9 to 0.25.11 (#1073)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#1072)
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.17.0 to 0.18.0 (#1071)

## Release 0.6.19 (2020-09-29T14:06:21)
### Features
* Catch missing exception (#1087)
* Feature/user api message prod (#1063)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.11 to 0.25.13 (#1089)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#1086)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.2 to 0.7.6 (#1084)

## Release 0.6.20 (2020-10-09T17:16:37)
### Features
* Update README file
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1 (#1100)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.10 (#1097)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#1096)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.10 (#1095)
* :pushpin: Automatic update of dependency sentry-sdk from 0.17.8 to 0.18.0 (#1094)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.15 (#1093)

## Release 0.7.0 (2020-11-06T08:26:50)
### Features
* Fix 404 for queued requests (#1124)
* Place dependencies under package to conform other endpoints (#1120)
* Place metadata info into Python packages section (#1119)
* Expose all packages (#1104)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.17 to 0.26.0 (#1129)
* :pushpin: Automatic update of dependency attrs from 20.2.0 to 20.3.0 (#1128)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.16 to 0.25.17 (#1126)
* :pushpin: Automatic update of dependency sentry-sdk from 0.19.1 to 0.19.2 (#1118)
* :pushpin: Automatic update of dependency sentry-sdk from 0.19.1 to 0.19.2 (#1117)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.25.16 (#1116)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#1114)
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#1113)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.13 to 0.8.2 (#1111)
* :pushpin: Automatic update of dependency sentry-sdk from 0.18.0 to 0.19.1 (#1107)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.11 to 0.7.13 (#1108)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#1106)
* :pushpin: Automatic update of dependency prometheus-flask-exporter from 0.18.0 to 0.18.1 (#1105)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#1103)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#1101)

## Release 0.8.0 (2020-11-10T12:11:22)
### Features
* Messaging 0.7.13 (#1136)
### Bug Fixes
* Make sure the advise endpoint is available when becoming ready (#1134)

## Release 0.9.0 (2020-11-18T15:01:47)
### Features
* Removed list endpoints (#1143)
### Automatic Updates
* :pushpin: Automatic update of dependency sentry-sdk from 0.19.2 to 0.19.3 (#1148)
* :pushpin: Automatic update of dependency thoth-storages from 0.26.1 to 0.27.0 (#1146)
* :pushpin: Automatic update of dependency sentry-sdk from 0.19.2 to 0.19.3 (#1147)
* :pushpin: Automatic update of dependency prometheus-client from 0.8.0 to 0.9.0 (#1145)
* :pushpin: Automatic update of dependency thoth-storages from 0.26.0 to 0.26.1 (#1142)
* :pushpin: Automatic update of dependency thoth-storages from 0.26.0 to 0.26.1 (#1141)
* :pushpin: Automatic update of dependency requests from 2.24.0 to 2.25.0 (#1140)

## Release 0.10.0 (2021-01-14T16:43:50)
### Features
* Trigger buildlog analysis workflow (#1171)
* Add Kebechet update template (#1178)
* :arrow_up: Automatic update of dependencies by kebechet. (#1177)
* dd Kebechet info template (#1179)
* Adjust response schema of build analysis endpoint (#1176)
* Do not propagate message topic in responses (#1168)
* :arrow_up: Automatic update of dependencies by kebechet. (#1173)
* :arrow_up: Automatic update of dependencies by kebechet. (#1170)
* Bump black version
* :arrow_up: Automatic update of dependencies by kebechet. (#1166)
* bump python version (#1165)
* :arrow_up: Automatic update of dependencies by kebechet. (#1162)
* :arrow_up: Automatic update of dependencies by kebechet. (#1156)
* get workflow node status (#1144)
### Bug Fixes
* re-locking pipfile lock for typing extension fix (#1175)
* pre-commit fixes for the user-api (#1174)
### Improvements
* removed bissenbay, thanks for your contributions!
* gitignore and pre-commit updates (#1115)

## Release 0.11.0 (2021-01-18T07:01:53)
### Features
* update to latest messaging (#1195)
* Remove legacy build analysis result endpoints (#1187)
* :arrow_up: Automatic update of dependencies by kebechet. (#1184)

## Release 0.11.1 (2021-01-19T16:35:47)
### Features
* Allow nullable responses in post-build endpoint (#1199)
* Fix new lines in the example input (#1198)

## Release 0.12.0 (2021-01-20T18:21:15)
### Features
* Expose schema metric (#1206)
* :sparkles: add kind/ labels to feature and bug template (#1205)
* :arrow_up: Automatic update of dependencies by kebechet. (#1204)
* :arrow_up: Automatic update of dependencies by kebechet. (#1201)

## Release 0.13.0 (2021-01-21T17:15:54)
### Features
* Set 1 by default when the revision is up (#1215)
* Extend configuration to capture versions of other libraries (#1212)
* :arrow_up: Automatic update of dependencies by kebechet. (#1213)

## Release 0.13.1 (2021-01-26T08:54:22)
### Features
* Standardize metric for schema check (#1218)

## Release 0.14.0 (2021-02-01T20:33:53)
### Features
* Introduce endpoints for listing available Thoth s2i bae container images
* :arrow_up: Automatic update of dependencies by kebechet. (#1227)
* Add missing title to Kebechet update template (#1226)
* :arrow_up: Automatic update of dependencies by kebechet. (#1222)
* :arrow_up: Automatic update of dependencies by kebechet. (#1220)
### Bug Fixes
* Report an error if the given S2I container image analysis was not done (#1229)

## Release 0.15.0 (2021-02-02T07:24:01)
### Features
* Unify endpoint response with the remaining endpoints
* Remove legacy runtime environment endpoint
* Remove handlers of obsolete endpoints
* Remove obsolete endpoints

## Release 0.16.0 (2021-02-02T08:33:33)
### Features
* Remove software environment endpoint (#1236)

## Release 0.17.0 (2021-02-02T11:23:14)
### Features
* Allow nullable entries in the hardware section
### Improvements
* Move hardware endoint under Hardware section and adjust nullables

## Release 0.18.0 (2021-02-09T11:01:16)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#1245)

## Release 0.19.0 (2021-02-12T09:44:42)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#1256)
* Unify responses of endpoints (#1255)
* Provide an option to validate responses (#1254)
* Remove endpoint exposing number of Python packages (#1251)
* Fix platform response schema (#1250)

## Release 0.19.1 (2021-02-17T14:24:17)
### Features
* Limit maximum content length that can be submitted via POST request (#1261)
* :arrow_up: Automatic update of dependencies by Kebechet (#1263)
* :arrow_up: Automatic update of dependencies by Kebechet (#1262)
* Backend does not support requirements, serialization is done on client side (#1260)

## Release 0.19.2 (2021-02-23T16:13:39)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet (#1268)
* Allow additional properties in status response (#1267)
* Fix openapi schema discovered by schema validation (#1266)
### Bug Fixes
* Correctly fix credentials quoting

## Release 0.19.3 (2021-02-24T13:28:16)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* Package platform is an array

## Release 0.19.4 (2021-02-25T13:22:52)
### Features
* Fix naming in Thoth s2i endpoint

## Release 0.20.0 (2021-02-25T18:34:36)
### Features
* Adjust message passing for data passed via Ceph (#1259)

## Release 0.20.1 (2021-02-25T19:54:11)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Manual dependency update

## Release 0.20.2 (2021-02-25T22:04:57)
### Features
* Fix message content (#1308)

## Release 0.20.3 (2021-03-01T20:50:05)
### Features
* Fix schema for requires_dist in Python package metadata

## Release 0.21.0 (2021-03-10T10:56:45)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Introduced endpoint for container images
* :arrow_up: Automatic update of dependencies by Kebechet (#1326)
* :arrow_up: Automatic update of dependencies by Kebechet (#1322)
* Sort library usage to properly hit cache on user-api on advise (#1325)
* Update OWNERS
### Improvements
* :sparkles: reconfgured CI/CD to use prow and aicoe-ci (#1323)

## Release 0.22.0 (2021-03-21T20:52:33)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#1338)
* add new params to be parallel to thoth-common (#1337)
* adjust function type hint (#1333)
* Report exceptions if configured
* specify contents of kebechet metadata
* add kebechet meta to post advise

## Release 0.22.1 (2021-03-28T05:32:18)
### Features
* constrain thoth-messaging (#1346)
* :arrow_up: Automatic update of dependencies by Kebechet (#1344)
* python types in spec :facepalm: (#1343)

## Release 0.23.0 (2021-03-31T22:41:57)
### Features
* Store information even for unauthenticated requests
* conditionally include params in hash computation
* Update thoth-messaging to v0.13.0 (#1361)
* :arrow_up: Automatic update of dependencies by Kebechet (#1357)
* Add missing else branch
* Always pop token from parameters
* Pass authenticated parameters to messages
* Inform if bad token is supplied
* Instantiate protected field listing once
* protect fields for post provenance and advise (#1336)
* :arrow_up: Automatic update of dependencies by Kebechet (#1352)

## Release 0.24.0 (2021-04-09T14:41:05)
### Features
* Check if analysis_id is present (#1378)
* remove input for post_provenance (#1377)
* :arrow_up: Automatic update of dependencies by Kebechet (#1376)
* Generalize _send_schedule_message method to consider authentication (#1372)
* Do cache hit only for accepted requests (#1373)
* :arrow_up: Automatic update of dependencies by Kebechet (#1374)
* Do not provide objects as query parameters (#1365)
* :arrow_up: Automatic update of dependencies by Kebechet (#1371)
* Move metrics creation (#1369)
* Provide information about queued analyses on status endpoints (#1368)
* Introduce cache hit metric (#1350)
### Bug Fixes
* Manipulate with cache metrics only if not force was supplied (#1379)
* Drop any metadata associated with the request when providing results (#1363)
### Improvements
* Remove unused function (#1366)

## Release 0.24.1 (2021-04-13T09:26:07)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#1383)
* Add unauthorized reponse schema (#1382)

## Release 0.24.2 (2021-04-13T20:59:46)
### Features
* Remove check on force (#1386)

## Release 0.24.3 (2021-04-14T13:47:01)
### Features
* Kebechet metadata is no longer query parameter (#1390)

## Release 0.24.4 (2021-04-27T11:05:49)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Remove unused dev dependencies (#1396)
* :arrow_up: Automatic update of dependencies by Kebechet (#1395)
### Improvements
* Remove old comment (#1394)

## Release 0.25.0 (2021-04-27T20:34:29)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Accept constraints on advise endpoint
### Bug Fixes
* Fix internal error HTTP status code when exception reporting is on

## Release 0.25.1 (2021-04-28T11:24:29)
### Bug Fixes
* metric fix (#1408)

## Release 0.25.2 (2021-06-02T19:59:43)
### Features
* Fix module not found error for flask._compat
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet (#1418)
* :hatched_chick: update the prow resource limits (#1417)
* :arrow_up: Automatic update of dependencies by Kebechet (#1415)
* :arrow_up: Automatic update of dependencies by Kebechet (#1412)

## Release 0.26.0 (2021-06-07T13:42:33)
### Features
* Obtain logs from Ceph as Argo Workflows places them there
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.26.1 (2021-06-14T20:01:42)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: updated labels of issue templates
* Introduce labels on advise endpoint

## Release 0.26.2 (2021-06-17T20:51:09)
### Features
* update to pydantic calling convention for messaging
* add priority/critical-urgent label to all bot related issue templates
* :arrow_up: Automatic update of dependencies by Kebechet
* Adjust copyright in headers

## Release 0.26.3 (2021-06-21T16:37:10)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.26.4 (2021-06-30T02:51:34)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :game_die: flush all pending messages
* :medal_sports: set badges for easy access to content

## Release 0.26.5 (2021-07-02T06:46:51)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* Remove qeb-hwt endpoint

## Release 0.26.6 (2021-07-30T10:08:37)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* Fix import statement
* Use directly env var
* Expose cache expiration configuration
* Make pre-commit happy
* initialize producer in similar way to database
### Improvements
* minor CI/CD config updates :arrow_up:
### Other
* remove github app parameters
