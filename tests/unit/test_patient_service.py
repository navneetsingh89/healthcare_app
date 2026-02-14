from unittest.mock import MagicMock, call

from healthcare.services.patient_service import PatientService


def _build_service_with_mocks():
    api_client = MagicMock()
    parser = MagicMock()
    repository = MagicMock()
    console_exporter = MagicMock()
    file_exporter = MagicMock()

    service = PatientService(
        api_client=api_client,
        parser=parser,
        repository=repository,
        console_exporter=console_exporter,
        file_exporter=file_exporter,
    )
    return service, api_client, parser, repository, console_exporter, file_exporter


def test_process_calls_dependencies_for_each_entry():
    service, api_client, parser, repository, console_exporter, file_exporter = (
        _build_service_with_mocks()
    )

    entries = [{"resource": {"id": "1"}}, {"resource": {"id": "2"}}]
    patient_1 = object()
    patient_2 = object()

    api_client.fetch_patients.return_value = entries
    parser.parse.side_effect = [patient_1, patient_2]

    service.process(count=2)

    api_client.fetch_patients.assert_called_once_with(2)
    parser.parse.assert_has_calls([call({"id": "1"}), call({"id": "2"})])
    repository.save.assert_has_calls([call(patient_1), call(patient_2)])
    console_exporter.export.assert_has_calls([call(patient_1), call(patient_2)])
    file_exporter.export.assert_has_calls([call(patient_1), call(patient_2)])


def test_process_uses_empty_resource_when_missing():
    service, api_client, parser, repository, console_exporter, file_exporter = (
        _build_service_with_mocks()
    )

    patient = object()
    api_client.fetch_patients.return_value = [{}]
    parser.parse.return_value = patient

    service.process(count=1)

    parser.parse.assert_called_once_with({})
    repository.save.assert_called_once_with(patient)
    console_exporter.export.assert_called_once_with(patient)
    file_exporter.export.assert_called_once_with(patient)


def test_process_does_nothing_when_api_returns_no_entries():
    service, api_client, parser, repository, console_exporter, file_exporter = (
        _build_service_with_mocks()
    )

    api_client.fetch_patients.return_value = []

    service.process(count=5)

    api_client.fetch_patients.assert_called_once_with(5)
    parser.parse.assert_not_called()
    repository.save.assert_not_called()
    console_exporter.export.assert_not_called()
    file_exporter.export.assert_not_called()
