from api.fhir_client import FhirApiClient
from parser.patient_parser import PatientParser
from repository.patient_repository import PatientRepository
from export.base import PatientExporter
from export.file_exporter import FileExporter

class PatientService:
    def __init__(self, 
                 api_client: FhirApiClient, 
                 parser: PatientParser, 
                 repository: PatientRepository, 
                 console_exporter: PatientExporter,
                 file_exporter: FileExporter):
        self.api_client = api_client
        self.parser = parser
        self.repository = repository
        self.console_exporter = console_exporter
        self.file_exporter = file_exporter

    def process(self, count=10):
        entries = self.api_client.fetch_patients(count)

        for entry in entries:
            patient_json = entry.get("resource", {})
            patient = self.parser.parse(patient_json)
            self.repository.save(patient)
            self.console_exporter.export(patient)
            self.file_exporter.export(patient)
