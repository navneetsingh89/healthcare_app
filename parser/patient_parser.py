from models.patient import Patient
import logging


class PatientParser:
    def parse(self, patient_json):
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
            logging.exception("Parsing error")
            return Patient("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")