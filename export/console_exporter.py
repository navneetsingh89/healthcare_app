"""Console exporter implementation."""

from export.base import PatientExporter
from models.patient import Patient
from utils import get_logger

logger = get_logger(__name__)


class ConsoleExporter(PatientExporter):
    """Writes patient summaries to application logs."""

    def export(self, patient: Patient) -> None:
        """
        Log one patient summary line.
        
        Args:
            patient: Patient record to print in summary format.
        
        Returns:
            None
        """
        logger.info(
            f"[ID={patient.patient_id}] "
            f"[Name={patient.name}] "
            f"[DOB={patient.dob}] "
            f"[Gender={patient.gender}]"
        )
