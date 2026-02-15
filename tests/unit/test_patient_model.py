import pytest

from healthcare.models.patient import Patient


@pytest.mark.parametrize("gender", ["male", "female", "other", "unknown"])
def test_patient_accepts_allowed_gender_values(gender):
    patient = Patient("p1", "John Doe", "1980-01-01", gender)

    assert patient.patient_id == "p1"
    assert patient.name == "John Doe"
    assert patient.dob == "1980-01-01"
    assert patient.gender == gender

@pytest.mark.parametrize(
    "patient_id,name,dob,expected_id,expected_name,expected_dob",
    [
        ("", "Jane", "1990-02-03", "UNKNOWN_ID", "Jane", "1990-02-03"),
        ("p2", "", "1990-02-03", "p2", "UNKNOWN_NAME", "1990-02-03"),
        ("p3", "Jane", "", "p3", "Jane", "UNKNOWN_DOB"),
        (None, None, None, "UNKNOWN_ID", "UNKNOWN_NAME", "UNKNOWN_DOB"),
    ],
)
def test_patient_missing_core_fields_use_fallback_values(
    patient_id, name, dob, expected_id, expected_name, expected_dob
):
    patient = Patient(patient_id, name, dob, "male")

    assert patient.patient_id == expected_id
    assert patient.name == expected_name
    assert patient.dob == expected_dob
    assert patient.gender == "male"
