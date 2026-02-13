from api.fhir_client import FhirApiClient
from parser.patient_parser import PatientParser
from repository.patient_repository import PatientRepository
from service.patient_service import PatientService
from export.console_exporter import ConsoleExporter
from export.file_exporter import FileExporter
from utils import setup_logger
from config.settings import Settings

logger = setup_logger(__name__)


if __name__ == "__main__":
    logger.info(f"Starting healthcare app - Environment: {Settings.ENV}")
    
    api_client = FhirApiClient(Settings.FHIR_BASE_URL,)
    parser = PatientParser()
    repository = PatientRepository(Settings.DB_PATH)
    console_exporter = ConsoleExporter()
    file_exporter = FileExporter(Settings.FILE_PATH)

    service = PatientService(api_client, parser, repository, console_exporter, file_exporter)
    service.process(count=10)
    
    logger.info("Healthcare app completed successfully")
