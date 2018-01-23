import os


class Configuration:
    # Please provide explicitly.
    APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
    OPENSHIFT_API_URL = os.environ['OPENSHIFT_API_URL']
    OPENSHIFT_API_TOKEN = os.environ['OPENSHIFT_API_TOKEN']
    OPENSHIFT_PROJECT_NAME = os.environ['OPENSHIFT_PROJECT_NAME']

    APP_SERVICE_PORT = os.getenv('APP_SERVICE_PORT', 34000)
    SWAGGER_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'swagger.yaml')
