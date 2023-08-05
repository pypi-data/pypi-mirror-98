"""
HttpClient based on requests, that takes care of setting up:
- The base url for the API
- Default headers
- And a retry policy

The returned client, has same interface as the requests module.
"""
from http import HTTPStatus

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient(requests.Session):
    def __init__(self, api_base_url, default_headers=None):
        super().__init__()

        retry_policy = self._get_retry_policy()
        adapter = HTTPAdapter(max_retries=retry_policy)
        self.mount('http://', adapter)
        self.mount('https://', adapter)

        if default_headers:
            self.headers.update(default_headers)
        self.api_base_url = api_base_url

        if self.api_base_url.endswith("/"):
            raise ValueError("Dont end the api_base_url with a '/' please.")

    def request(self, method, url, *args, **kwargs):
        url = self._prepend_base_url(url)
        return super().request(method, url, *args, **kwargs)

    def _prepend_base_url(self, url):
        if not url.startswith("/"):
            raise ValueError("Start with a '/' please.")

        # Hack to be able to access the qlattice information on 'http:/.../api/v1/qlattice'.
        # Public facing api paths should be revisited to remove this hack.
        if url == "/":
            url = ""

        return self.api_base_url + url

    def _get_retry_policy(self):
        return Retry(
            total=2,
            backoff_factor=2,
            raise_on_status=False,
            allowed_methods=['GET', 'PUT', 'POST', 'DELETE'],
            status_forcelist=[
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT
            ],
        )


class QLatticeHttpClient(HttpClient):
    """
    Adds id={qlattice_id} as querystring parameter to all requests.
    Temporary, while we are migrating to a new URL scheme.
    """

    def __init__(self, qlattice_id, qlattice_server, default_headers=None):
        qlattice_server = qlattice_server.rstrip("/")

        if 'qlattice.abzu.ai' in qlattice_server or 'qlattice.stage.abzu.ai' in qlattice_server:
            api_base_url = f"{qlattice_server}/qlattice-{qlattice_id}/api/v1/qlattice"
        else:
            # Docker as a service, or localhost running
            api_base_url = f"{qlattice_server}/api/v1/qlattice"

        super().__init__(api_base_url, default_headers)
        self.qlattice_id = qlattice_id

    def request(self, method, url, *args, **kwargs):
        if 'params' not in kwargs:
            kwargs.update(params={})

        kwargs['params']["qlattice_id"] = self.qlattice_id

        return super().request(method, url, *args, **kwargs)
