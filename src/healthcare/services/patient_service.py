"""Application service that orchestrates fetch, parse, save, and export."""

from healthcare.api.fhir_client import FhirApiClient
from healthcare.parsers.patient_parser import PatientParser
from healthcare.repository.patient_repository import PatientRepository
from healthcare.exporters.base import PatientExporter
from healthcare.exporters.file_exporter import FileExporter


class PatientService:
    """Coordinates the end-to-end patient processing workflow."""

    def __init__(
        self,
        api_client: FhirApiClient,
        parser: PatientParser,
        repository: PatientRepository,
        console_exporter: PatientExporter,
        file_exporter: FileExporter,
    ) -> None:
        """
        Inject workflow dependencies.
        
        Args:
            api_client: FHIR API client instance.
            parser: Parser that converts raw JSON into Patient objects.
            repository: Repository for patient persistence.
            console_exporter: Exporter for console/log output.
            file_exporter: Exporter for file output.
        
        Returns:
            None
        """
        self.api_client = api_client
        self.parser = parser
        self.repository = repository
        self.console_exporter = console_exporter
        self.file_exporter = file_exporter

    def process(self, count: int = 10) -> None:
        """
        Process a batch of patients from API to outputs.
        
        Args:
            count: Number of patient records to process.
        
        Returns:
            None
        """
        entries = self.api_client.fetch_patients(count)

        for entry in entries:
            patient_json = entry.get("resource", {})
            patient = self.parser.parse(patient_json)
            self.repository.save(patient)
            self.console_exporter.export(patient)
            self.file_exporter.export(patient)
