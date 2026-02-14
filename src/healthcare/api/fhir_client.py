"""FHIR API client with retry and timeout handling."""

from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from healthcare.utils import get_logger

logger = get_logger(__name__)


class FhirApiClient:
    """Client responsible for fetching patient resources from a FHIR server."""

    def __init__(
        self,
        base_url: str,
        max_retries: int = 3,
        backoff_factor: int = 3,
        timeout: tuple[float, float] = (3.05, 10),
    ) -> None:
        """
        Initialize HTTP session with retry policy for transient failures.
        
        Args:
            base_url: Base URL of the FHIR API server.
            max_retries: Maximum number of retry attempts for transient failures.
            backoff_factor: Backoff factor used between retry attempts.
            timeout: Connect and read timeout values in seconds.
        
        Returns:
            None
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout

        self.session = requests.Session()
        retry = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch_patients(self, count: int = 10) -> list[dict[str, Any]]:
        """
        Fetch patient entries from the FHIR endpoint.
        
        Args:
            count: Number of patient resources to request.
        
        Returns:
            list[dict[str, Any]]: Patient entry objects returned by the API.
        """
        logger.info(f"Fetching {count} patients from FHIR API...")
        try:
            url = f"{self.base_url}/Patient?_count={count}"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            patients = response.json().get("entry", [])
            logger.info(f"Successfully fetched {len(patients)} patients")
            return patients
        except requests.exceptions.Timeout:
            logger.error("FHIR API timeout - connection took too long")
            return []

        except requests.exceptions.HTTPError as e:
            logger.error(f"FHIR API HTTP error: {e}")
            return []

        except Exception:
            logger.exception("Unexpected API error")
            return []
