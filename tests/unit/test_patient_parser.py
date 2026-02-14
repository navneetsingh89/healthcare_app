import pytest
from healthcare.parsers.patient_parser import PatientParser


def test_parse_valid_patient():

    raw_data = {
        "id": "123",
        "name": [
            {
                "given": ["John"],
                "family": "Doe"
            }
        ],
        "gender": "male",
        "birthDate": "1980-01-01"
    }

    # parser = PatientParser()
    patient = PatientParser().parse(raw_data)

    assert patient.patient_id == "123"
    assert patient.name == "John Doe"
    assert patient.gender == "male"
    assert patient.dob == "1980-01-01"