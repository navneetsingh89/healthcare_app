"""Patient domain model with basic field validation."""


class Patient:
    """Represents a normalized patient record."""

    def __init__(self, patient_id: str, name: str, dob: str, gender: str):
        """
        Initialize a Patient with validated field values.

        Args:
            patient_id: Unique patient identifier.
            name: Patient display name.
            dob: Date of birth string.
            gender: Patient gender string.

        Returns:
            None
        """
        self.patient_id = self._validate_id(patient_id)
        self.name = self._validate_name(name)
        self.dob = self._validate_dob(dob)
        self.gender = self._validate_gender(gender)

    def _validate_id(self, value: str) -> str:
        """
        Return a valid patient id or fallback value.

        Args:
            value: Candidate patient id.

        Returns:
            str: Validated patient id.
        """
        return value if value else "UNKNOWN_ID"

    def _validate_name(self, value: str) -> str:
        """
        Return a valid name or fallback value.

        Args:
            value: Candidate patient name.

        Returns:
            str: Validated patient name.
        """
        return value if value else "UNKNOWN_NAME"

    def _validate_dob(self, value: str) -> str:
        """
        Return a valid date of birth or fallback value.

        Args:
            value: Candidate date of birth.

        Returns:
            str: Validated date of birth.
        """
        return value if value else "UNKNOWN_DOB"

    def _validate_gender(self, value: str) -> str:
        """
        Allow only known FHIR gender values.

        Args:
            value: Candidate gender value.

        Returns:
            str: Validated gender value.
        """
        allowed = {"male", "female", "other", "unknown"}
        return value if value in allowed else "UNKNOWN_GENDER"
