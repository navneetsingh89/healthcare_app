import sqlite3

import pytest

from healthcare.api.fhir_client import FhirApiClient
from healthcare.exporters.console_exporter import ConsoleExporter
from healthcare.exporters.file_exporter import FileExporter
from healthcare.parsers.patient_parser import PatientParser
from healthcare.repository.patient_repository import PatientRepository
from healthcare.services.patient_service import PatientService


@pytest.fixture
def temp_repository(tmp_path):
    db_path = tmp_path / "patients_test.db"
    return PatientRepository(str(db_path))


@pytest.fixture
def parser():
    return PatientParser()


@pytest.fixture
def api_client_mocked(monkeypatch):
    client = FhirApiClient("https://fakeapi.com")

    fake_entries = [
        {
            "resource": {
                "id": "1",
                "name": [{"given": ["Alice"], "family": "Brown"}],
                "birthDate": "1985",
                "gender": "female",
            }
        },
        {
            "resource": {
                "id": "2",
                "name": [{"given": ["Bob"], "family": "Smith"}],
                "birthDate": "1990",
                "gender": "male",
            }
        },
        {"resource": {"id": "3"}},
    ]

    def fake_fetch_patients(count=10):
        return fake_entries[:count]

    monkeypatch.setattr(client, "fetch_patients", fake_fetch_patients)
    return client


@pytest.fixture
def service(api_client_mocked, parser, temp_repository, tmp_path):
    console_exporter = ConsoleExporter()
    file_exporter = FileExporter(str(tmp_path / "patients_test.txt"))
    return PatientService(
        api_client_mocked,
        parser,
        temp_repository,
        console_exporter,
        file_exporter,
    )


def test_full_pipeline(service, temp_repository):
    service.process(count=3)

    conn = sqlite3.connect(temp_repository.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY patient_id")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 3

    assert rows[0][0] == "1"
    assert rows[0][1] == "Alice Brown"
    assert rows[0][2] == "1985"
    assert rows[0][3] == "female"

    assert rows[2][1] in ["UNKNOWN_NAME", "Unknown"]
    assert rows[2][2] == "UNKNOWN_DOB"
    assert rows[2][3] == "UNKNOWN_GENDER"
