import os

class Settings:
    # Environment
    ENV = os.getenv("ENV", "dev")

    # API
    FHIR_BASE_URL = os.getenv(
        "FHIR_BASE_URL",
        "https://r4.smarthealthit.org"
    )
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))
    API_RETRIES = int(os.getenv("API_RETRIES", 3))

    # Database
    DB_PATH = os.getenv("DB_PATH", "patients.db")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # file_path
    FILE_PATH = os.getenv("FILE_PATH", "patients.txt")