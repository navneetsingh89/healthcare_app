from export.base import PatientExporter
from utils import get_logger

logger = get_logger(__name__)

class ConsoleExporter(PatientExporter):
    def export(self, patient):
        logger.info(
            f"[ID={patient.patient_id}] "
            f"[Name={patient.name}] "
            f"[DOB={patient.dob}] "
            f"[Gender={patient.gender}]"
        )
