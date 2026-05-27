import time
from collections.abc import Mapping
from typing import Any, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry

from .errors import ZendeskError

JsonDict = dict[str, Any]
ParamsType = Union[Mapping[str, Any], list[tuple[str, Any]]]


class ZendeskClient:
    def __init__(
        self,
        subdomain: str,
        email: Optional[str] = None,
        token: Optional[str] = None,
        oauth_token: Optional[str] = None,
        timeout: int = 30,
        user_agent: str = "zendesk-toolkit/0.0.1",
        max_retries: int = 5,
    ) -> None:
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.timeout = timeout
        self.session = requests.Session()

        retry = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504] if max_retries > 0 else [],
            allowed_methods=frozenset(["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]),
            respect_retry_after_header=True,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        if oauth_token:
            self.session.headers.update({"Authorization": f"Bearer {oauth_token}"})
        elif email and token:
            self.session.auth = HTTPBasicAuth(f"{email}/token", token)
        else:
            raise ValueError("Provide oauth_token or (email and token).")

        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": user_agent,
            }
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Optional[JsonDict]:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}/{endpoint.lstrip('/')}"
        while True:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", "1"))
                time.sleep(retry_after)
                continue
            if not (200 <= resp.status_code < 300):
                request_id = resp.headers.get("X-Request-Id")
                try:
                    payload = resp.json()
                    message = payload.get("error") or payload.get("description") or resp.text
                except Exception:
                    payload = {}
                    message = resp.text
                raise ZendeskError(
                    message=message, status=resp.status_code, request_id=request_id, payload=payload
                )
            if resp.content and "application/json" in resp.headers.get("Content-Type", ""):
                return resp.json()
            return None

    def get(self, endpoint: str, params: Optional[ParamsType] = None) -> Optional[JsonDict]:
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        json: Optional[JsonDict] = None,
        files: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[JsonDict]:
        h: dict[str, Any] = {}
        if headers:
            h.update(headers)
        if files is not None:
            # Suppress the session-level application/json so requests can set
            # the correct multipart/form-data boundary itself.
            h["Content-Type"] = None
        return self._request("POST", endpoint, json=json, files=files, headers=h or None)

    def put(self, endpoint: str, json: Optional[JsonDict] = None) -> Optional[JsonDict]:
        return self._request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: Optional[JsonDict] = None) -> Optional[JsonDict]:
        return self._request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> Optional[JsonDict]:
        return self._request("DELETE", endpoint)
