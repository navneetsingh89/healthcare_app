import pytest
from healthcare.parsers.patient_parser import PatientParser


 

def test_parse_valid_patient():
    raw_data = {
        "id": "123",
        "name": [{"given": ["John"], "family": "Doe"}],
        "gender": "male",
        "birthDate": "1980-01-01",
    }

    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "123"
    assert patient.name == "John Doe"
    assert patient.gender == "male"
    assert patient.dob == "1980-01-01"


def test_parse_missing_name_uses_unknown_name():
    raw_data = {
        "id": "123",
        "gender": "female",
        "birthDate": "1990-02-03",
    }

    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "123"
    assert patient.name == "Unknown"
    assert patient.gender == "female"
    assert patient.dob == "1990-02-03"


def test_parse_missing_given_and_family_falls_back_to_unknown_name():
    raw_data = {
        "id": "123",
        "name": [{}],
        "gender": "male",
        "birthDate": "1980-01-01",
    }

    patient = PatientParser().parse(raw_data)

    assert patient.name == "Unknown"


def test_parse_missing_id_dob_gender_uses_model_defaults():
    raw_data = {
        "name": [{"given": ["Ana"], "family": "Smith"}],
    }

    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "UNKNOWN_ID"
    assert patient.name == "Ana Smith"
    assert patient.dob == "UNKNOWN_DOB"
    assert patient.gender == "UNKNOWN_GENDER"


def test_parse_invalid_gender_maps_to_unknown_gender():
    raw_data = {
        "id": "777",
        "name": [{"given": ["Sam"], "family": "Taylor"}],
        "gender": "invalid",
        "birthDate": "2001-12-12",
    }

    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "777"
    assert patient.name == "Sam Taylor"
    assert patient.dob == "2001-12-12"
    assert patient.gender == "UNKNOWN_GENDER"


def test_parse_malformed_name_payload_uses_parser_exception_fallback():
    raw_data = {
        "id": "123",
        "name": ["bad-name-shape"],
        "gender": "male",
        "birthDate": "1980-01-01",
    }

    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "UNKNOWN"
    assert patient.name == "UNKNOWN"
    assert patient.dob == "UNKNOWN"
    assert patient.gender == "UNKNOWN_GENDER"


# -----------------------
# Completely empty JSON
# -----------------------

@pytest.fixture
def parser():
    return PatientParser()


def test_empty_json(parser):
    patient = parser.parse({})
    assert patient.name == "Unknown"
    assert patient.patient_id == "UNKNOWN_ID"
