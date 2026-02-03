import requests
import time
from typing import Dict, Optional


def check_website_http(
    url: str, timeout: int = 10, retries: int = 1, retry_delay: int = 2
) -> Dict[str, Optional[str]]:
    """Perform HTTP availability check.
    Returns structured result for decision layer"""

    attempt = 0
    start_time = time.time()

    while attempt < retries + 1:  # looks cleaner then attempt <= retries
        try:
            response = requests.get(
                url, timeout=timeout, headers={"User-Agent": "WebsiteMonitor/1.0"}
            )
            response_time = round(time.time() - start_time, 2)

            if 200 <= response.status_code < 400:
            
                return {
                    "status": "UP",
                    "status_code": response.status_code,
                    "error": None,
                    "response_time": response_time,
                }

            # Suspicious or failure responses → verify

            return {
                "status": "verify",
                "status_code": response.status_code,
                "error": None,
                "response_time": response_time,
            }

        except requests.exceptions.RequestException as exc:
            attempt += 1
            if attempt > retries:
                return {
                    "status": "verify",
                    "status_code": None,
                    "error": str(exc),
                    "response_time": None,
                }

            time.sleep(retry_delay)
