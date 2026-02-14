"""File exporter implementation."""

from export.base import PatientExporter
from models.patient import Patient


class FileExporter(PatientExporter):
    """Appends patient summaries to a text file."""

    def __init__(self, filepath: str) -> None:
        """
        Store destination file path.
        
        Args:
            filepath: Output file path for exported patient rows.
        
        Returns:
            None
        """
        self.filepath = filepath

    def export(self, patient: Patient) -> None:
        """
        Append one patient row to the output file.
        
        Args:
            patient: Patient record to append.
        
        Returns:
            None
        """
        with open(self.filepath, "a") as f:
            f.write(f"{patient.patient_id},{patient.name}\n")
