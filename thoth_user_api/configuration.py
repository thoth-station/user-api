import os
import datetime


def _get_api_token():
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc


class Configuration:
    # Please provide explicitly.
    APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
    KUBERNETES_API_URL = os.getenv('KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
    KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN', _get_api_token())
    THOTH_ANALYZER_NAMESPACE = os.environ['THOTH_ANALYZER_NAMESPACE']
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'swagger.yaml')
    THOTH_ANALYZER_HARD_TIMEOUT = int(os.getenv('THOTH_ANALYZER_HARD_TIMEOUT',
                                                datetime.timedelta(hours=24).total_seconds()))
