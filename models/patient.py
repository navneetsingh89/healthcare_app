class Patient:
    def __init__(self, patient_id: str, name: str, dob: str, gender: str):
        self.patient_id = self._validate_id(patient_id)
        self.name = self._validate_name(name)
        self.dob = self._validate_dob(dob)
        self.gender = self._validate_gender(gender)

    def _validate_id(self, value: str) -> str:
        return value if value else "UNKNOWN_ID"

    def _validate_name(self, value: str) -> str:
        return value if value else "UNKNOWN_NAME"

    def _validate_dob(self, value: str) -> str:
        return value if value else "UNKNOWN_DOB"

    def _validate_gender(self, value: str) -> str:
        allowed = {"male", "female", "other", "unknown"}
        return value if value in allowed else "UNKNOWN_GENDER"
