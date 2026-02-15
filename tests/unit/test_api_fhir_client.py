from unittest.mock import Mock, patch

import requests

from healthcare.api.fhir_client import FhirApiClient


BASE_URL = "https://test.com"

# ----------------------------
# Success case
# ----------------------------
@patch("healthcare.api.fhir_client.requests.Session.get")
def test_fetch_patients_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"entry": [{"resource": {"id": "1"}}]}
    mock_get.return_value = mock_response

    client = FhirApiClient(BASE_URL)
    result = client.fetch_patients(5)

    assert len(result) == 1
    assert result[0]["resource"]["id"] == "1"
    mock_get.assert_called_once()

# ----------------------------
# HTTP error
# ----------------------------
@patch("healthcare.api.fhir_client.requests.Session.get")
def test_fetch_patients_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
    mock_get.return_value = mock_response

    client = FhirApiClient(BASE_URL)
    result = client.fetch_patients()

    assert result == []

# ----------------------------
# Timeout
# ----------------------------
@patch("healthcare.api.fhir_client.requests.Session.get")
def test_fetch_patients_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("Timeout")

    client = FhirApiClient(BASE_URL)
    result = client.fetch_patients()

    assert result == []

# ----------------------------
# No entry key
# ----------------------------
@patch("healthcare.api.fhir_client.requests.Session.get")
def test_fetch_patients_no_entry(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    client = FhirApiClient(BASE_URL)
    result = client.fetch_patients()

    assert result == []
