"""Base exporter contract for patient output targets."""

from healthcare.models.patient import Patient


class PatientExporter:
    """Abstract exporter interface."""

    def export(self, patient: Patient) -> None:
        """
        Export a single patient record.
        
        Args:
            patient: Patient record to export.
        
        Returns:
            None
        """
        raise NotImplementedError
