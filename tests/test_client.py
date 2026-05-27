import base64

import pytest

from zendesk_toolkit import ZendeskClient, ZendeskError


def test_basic_auth_header(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/users/me.json", json={"user": {"id": 1}}, status=200)
    client.get("users/me.json")
    sent_auth = mocked.calls[0].request.headers["Authorization"]
    assert sent_auth.startswith("Basic ")
    decoded = base64.b64decode(sent_auth.split(" ", 1)[1]).decode()
    assert decoded == "agent@acme.com/token:t0k3n"


def test_oauth_bearer_header(oauth_client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/users/me.json", json={"user": {}}, status=200)
    oauth_client.get("users/me.json")
    assert mocked.calls[0].request.headers["Authorization"] == "Bearer bearer-abc"


def test_requires_some_auth():
    with pytest.raises(ValueError):
        ZendeskClient(subdomain="acme")


def test_relative_endpoint_builds_full_url(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/tickets/1.json", json={"ticket": {"id": 1}}, status=200)
    result = client.get("tickets/1.json")
    assert result == {"ticket": {"id": 1}}
    assert mocked.calls[0].request.url == f"{base_url}/tickets/1.json"


def test_absolute_endpoint_passes_through(client, mocked):
    full = "https://other.example.com/foo.json"
    mocked.add(mocked.GET, full, json={"ok": True}, status=200)
    result = client.get(full)
    assert result == {"ok": True}
    assert mocked.calls[0].request.url == full


def test_non_2xx_raises_zendesk_error(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/tickets/999.json",
        json={"error": "RecordNotFound", "description": "Not found"},
        status=404,
        headers={"X-Request-Id": "req-123"},
    )
    with pytest.raises(ZendeskError) as exc_info:
        client.get("tickets/999.json")
    err = exc_info.value
    assert err.status == 404
    assert err.request_id == "req-123"
    assert err.payload["error"] == "RecordNotFound"
    assert "RecordNotFound" in str(err)


def test_non_2xx_non_json_body_still_raises(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/x.json", body="upstream broke", status=502)
    with pytest.raises(ZendeskError) as exc_info:
        client.get("x.json")
    assert exc_info.value.status == 502
    assert exc_info.value.payload == {}


def test_empty_2xx_body_returns_none(client, base_url, mocked):
    mocked.add(mocked.DELETE, f"{base_url}/tickets/1.json", body="", status=204)
    assert client.delete("tickets/1.json") is None


def test_429_then_success_loops_with_backoff(client, base_url, mocked, monkeypatch):
    """The explicit 429 loop in _request should sleep then retry. We bypass the urllib3
    Retry adapter by giving Retry-After=0 and stubbing time.sleep."""
    sleeps = []
    monkeypatch.setattr("zendesk_toolkit.client.time.sleep", lambda s: sleeps.append(s))

    mocked.add(
        mocked.GET,
        f"{base_url}/tickets/1.json",
        body="rate limited",
        status=429,
        headers={"Retry-After": "0"},
    )
    mocked.add(mocked.GET, f"{base_url}/tickets/1.json", json={"ticket": {"id": 1}}, status=200)

    result = client.get("tickets/1.json")
    assert result == {"ticket": {"id": 1}}
    assert sleeps == [0]
    assert len(mocked.calls) == 2


def test_post_envelope_serialised(client, base_url, mocked):
    mocked.add(mocked.POST, f"{base_url}/tickets.json", json={"ticket": {"id": 99}}, status=201)
    client.post("tickets.json", json={"ticket": {"subject": "x"}})
    body = mocked.calls[0].request.body
    assert b'"subject": "x"' in body or b'"subject":"x"' in body


def test_post_with_files_drops_json_content_type(client, base_url, mocked):
    mocked.add(mocked.POST, f"{base_url}/uploads.json", json={"upload": {"token": "abc"}}, status=201)
    client.post("uploads.json", files={"file": ("x.bin", b"hello", "application/octet-stream")})
    sent_ct = mocked.calls[0].request.headers.get("Content-Type", "")
    assert "multipart/form-data" in sent_ct
