import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils import get_logger

logger = get_logger(__name__)


class FhirApiClient:
    def __init__( self, base_url, max_retries=3, backoff_factor=3, timeout=(3.05, 10),):
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

    def fetch_patients(self, count=10):
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

        except Exception as e:
            logger.exception("Unexpected API error")
            return []
