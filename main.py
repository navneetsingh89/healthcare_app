from api.fhir_client import FhirApiClient
from parser.patient_parser import PatientParser
from repository.patient_repository import PatientRepository
from service.patient_service import PatientService
from export.console_exporter import ConsoleExporter
from export.file_exporter import FileExporter
import logging
from config.settings import Settings



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logging.info("message")
logging.error("message")


if __name__ == "__main__":
    api_client = FhirApiClient(Settings.FHIR_BASE_URL,)
    parser = PatientParser()
    repository = PatientRepository(Settings.DB_PATH)
    console_exporter = ConsoleExporter()
    file_exporter = FileExporter(Settings.FILE_PATH)

    service = PatientService(api_client, parser, repository, console_exporter, file_exporter)
    service.process(count=10)
