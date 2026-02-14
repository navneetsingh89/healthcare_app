"""Parser that converts raw FHIR JSON into Patient domain objects."""

from typing import Any

from models.patient import Patient
from utils import get_logger

logger = get_logger(__name__)


class PatientParser:
    """Builds Patient instances from FHIR resource dictionaries."""

    def parse(self, patient_json: dict[str, Any]) -> Patient:
        """
        Parse a FHIR patient resource into a validated Patient object.
        
        Args:
            patient_json: Raw FHIR patient resource payload.
        
        Returns:
            Patient: Parsed and validated patient domain object.
        """
        try:
            name = "Unknown"
            names = patient_json.get("name", [])
            if names:
                given = names[0].get("given", [""])[0]
                family = names[0].get("family", "")
                name = f"{given} {family}".strip() or "Unknown"

            return Patient(
                patient_id=patient_json.get("id"),
                name=name,
                dob=patient_json.get("birthDate"),
                gender=patient_json.get("gender"),
            )
        except Exception:
            logger.exception("Error parsing patient JSON")
            return Patient("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")
