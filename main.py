"""Application entry point for the healthcare patient import workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.healthcare.api.fhir_client import FhirApiClient
from src.healthcare.config.settings import Settings
from src.healthcare.exporters.console_exporter import ConsoleExporter
from src.healthcare.exporters.file_exporter import FileExporter
from src.healthcare.parsers.patient_parser import PatientParser
from src.healthcare.repository.patient_repository import PatientRepository
from src.healthcare.services.patient_service import PatientService
from src.healthcare.utils import setup_logger

logger = setup_logger(__name__)


def main() -> None:
    """Run the full patient processing pipeline."""
    logger.info(f"Starting healthcare app - Environment: {Settings.ENV}")

    api_client = FhirApiClient(Settings.FHIR_BASE_URL)
    parser = PatientParser()
    repository = PatientRepository(Settings.DB_PATH)
    console_exporter = ConsoleExporter()
    file_exporter = FileExporter(Settings.FILE_PATH)

    service = PatientService(
        api_client, parser, repository, console_exporter, file_exporter
    )
    service.process(count=10)

    logger.info("Healthcare app completed successfully")


if __name__ == "__main__":
    main()
