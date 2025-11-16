"""
API Client module.

Wraps requests.Session with configurable base URL, timeouts, and retry mechanism.
Follows Single Responsibility Principle - handles only HTTP communication.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any
from utils.logger import get_logger


class APIClient:
    """
    HTTP client wrapper for making API requests.

    Features:
    - Configurable base URL and timeout
    - Automatic retry mechanism with exponential backoff
    - Request/response logging
    """

    def __init__(
                    self,
                    base_url: str,
                    timeout: int = 10,
                    max_retries: int = 3,
                    backoff_factor: float = 0.3
                ):
        """
            Initialize API client.

            Args:
                base_url: Base URL for API requests
                timeout: Request timeout in seconds
                max_retries: Maximum number of retry attempts
                backoff_factor: Backoff factor for retries
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.logger = get_logger(__name__)

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.logger.info(f"APIClient initialized with base_url: {self.base_url}")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details (without sensitive data)."""
        params = kwargs.get('params', {})
        self.logger.debug(f"Request: {method} {url} | Params: {params}")

    def _log_response(self, response: requests.Response) -> None:
        """Log response details."""
        self.logger.debug(
            f"Response: {response.status_code} | "
            f"URL: {response.url} | "
            f"Time: {response.elapsed.total_seconds():.2f}s"
        )

    def get(
                self,
                endpoint: str,
                params: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                **kwargs
            ) -> requests.Response:
        """
        Perform GET request.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: HTTP headers
            **kwargs: Additional requests arguments

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request("GET", url, params=params)

        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def post(
                self,
                endpoint: str,
                json: Optional[Dict[str, Any]] = None,
                data: Optional[Any] = None,
                headers: Optional[Dict[str, str]] = None,
                **kwargs
            ) -> requests.Response:
        """
        Perform POST request.

        Args:
            endpoint: API endpoint path
            json: JSON payload
            data: Form data payload
            headers: HTTP headers
            **kwargs: Additional requests arguments

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request("POST", url)

        response = self.session.post(
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def put(
                self,
                endpoint: str,
                json: Optional[Dict[str, Any]] = None,
                data: Optional[Any] = None,
                headers: Optional[Dict[str, str]] = None,
                **kwargs
            ) -> requests.Response:
        """
        Perform PUT request.

        Args:
            endpoint: API endpoint path
            json: JSON payload
            data: Form data payload
            headers: HTTP headers
            **kwargs: Additional requests arguments

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request("PUT", url)

        response = self.session.put(
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def delete(
                self,
                endpoint: str,
                headers: Optional[Dict[str, str]] = None,
                **kwargs
            ) -> requests.Response:
        """
        Perform DELETE request.

        Args:
            endpoint: API endpoint path
            headers: HTTP headers
            **kwargs: Additional requests arguments

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request("DELETE", url)

        response = self.session.delete(
            url,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def close(self) -> None:
        """Close the session."""
        self.session.close()
        self.logger.info("APIClient session closed")

