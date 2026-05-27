from urllib.parse import parse_qs, urlparse

from zendesk_toolkit.help_center import search


def _query(url: str) -> dict:
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


def test_search_articles_drops_none_filters(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/articles/search.json",
        json={"results": []},
        status=200,
    )
    search.search_articles(client, query="password", locale="en-us", category=None, brand_id=42)
    q = _query(mocked.calls[0].request.url)
    assert q == {"query": "password", "locale": "en-us", "brand_id": "42"}


def test_search_articles_no_query_only_filters(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/articles/search.json",
        json={"results": []},
        status=200,
    )
    search.search_articles(client, category=12, label_names="onboarding")
    q = _query(mocked.calls[0].request.url)
    assert q == {"category": "12", "label_names": "onboarding"}


def test_unified_search_hits_guide_endpoint(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/guide/search.json", json={"results": []}, status=200)
    search.unified_search(client, query="foo")
    assert mocked.calls[0].request.url.startswith(f"{base_url}/guide/search.json")
