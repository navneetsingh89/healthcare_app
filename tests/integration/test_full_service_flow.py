import sqlite3
from unittest.mock import Mock

from healthcare.exporters.console_exporter import ConsoleExporter
from healthcare.exporters.file_exporter import FileExporter
from healthcare.parsers.patient_parser import PatientParser
from healthcare.repository.patient_repository import PatientRepository
from healthcare.services.patient_service import PatientService


def test_full_service_flow_real_parser_real_repository_mock_api_only(tmp_path):
    db_path = tmp_path / "patients_full_flow.db"
    out_path = tmp_path / "patients_full_flow.txt"

    repository = PatientRepository(str(db_path))
    parser = PatientParser()
    console_exporter = ConsoleExporter()
    file_exporter = FileExporter(str(out_path))

    api_client = Mock()
    api_client.fetch_patients.return_value = [
        {
            "resource": {
                "id": "10",
                "name": [{"given": ["Nina"], "family": "Patel"}],
                "birthDate": "1988-04-01",
                "gender": "female",
            }
        },
        {"resource": {"id": "11"}},
    ]

    service = PatientService(
        api_client=api_client,
        parser=parser,
        repository=repository,
        console_exporter=console_exporter,
        file_exporter=file_exporter,
    )

    service.process(count=2)

    api_client.fetch_patients.assert_called_once_with(2)

    conn = sqlite3.connect(str(db_path))
    rows = conn.execute(
        "SELECT patient_id, name, dob, gender FROM patients ORDER BY patient_id"
    ).fetchall()
    conn.close()

    assert rows == [
        ("10", "Nina Patel", "1988-04-01", "female"),
        ("11", "Unknown", "UNKNOWN_DOB", "UNKNOWN_GENDER"),
    ]
