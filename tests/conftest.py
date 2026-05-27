import pytest
import responses as responses_lib

from zendesk_toolkit import ZendeskClient

SUBDOMAIN = "acme"
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def client() -> ZendeskClient:
    # max_retries=0 so the urllib3 Retry adapter doesn't intercept 429/5xx —
    # tests need to exercise the explicit 429 loop and the ZendeskError path.
    return ZendeskClient(subdomain=SUBDOMAIN, email="agent@acme.com", token="t0k3n", max_retries=0)


@pytest.fixture
def oauth_client() -> ZendeskClient:
    return ZendeskClient(subdomain=SUBDOMAIN, oauth_token="bearer-abc", max_retries=0)


@pytest.fixture
def mocked():
    with responses_lib.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps
