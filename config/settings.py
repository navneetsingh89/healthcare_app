import os
import yaml
from pathlib import Path

# We are consuming config.yml file here to set variable names.
# These variables can also be overridden by setting OS environment variables.
# The priority order is: OS environment variables > config.yml values

# Load YAML configuration
config_path = Path(__file__).parent / "config.yml"
with open(config_path, 'r') as f:
    _config = yaml.safe_load(f)

class Settings:
    # Application
    APP_NAME = _config["app"]["name"]
    ENV = _config["app"]["environment"]

    # API
    FHIR_BASE_URL = _config["api"]["fhir_base_url"]
    API_TIMEOUT = _config["api"]["timeout"]
    API_RETRIES = _config["api"]["retries"]

    # Database
    DB_PATH = _config["database"]["path"]

    # Logging
    LOG_LEVEL = _config["logging"]["level"]
    LOG_FORMAT = _config["logging"]["format"]

    # file_path
    FILE_PATH = os.getenv("FILE_PATH", "patients.txt")