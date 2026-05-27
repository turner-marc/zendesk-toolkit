import json

from zendesk_toolkit.support import tickets, uploads


def test_create_ticket_wraps_envelope(client, base_url, mocked):
    mocked.add(mocked.POST, f"{base_url}/tickets.json", json={"ticket": {"id": 7}}, status=201)
    tickets.create_ticket(client, {"subject": "hi", "comment": {"body": "x"}})
    body = json.loads(mocked.calls[0].request.body)
    assert body == {"ticket": {"subject": "hi", "comment": {"body": "x"}}}


def test_add_comment_with_uploads_combines_all_fields(client, base_url, mocked):
    mocked.add(mocked.PUT, f"{base_url}/tickets/42.json", json={"ticket": {"id": 42}}, status=200)
    tickets.add_comment_with_uploads(
        client,
        ticket_id=42,
        body="see attached",
        upload_tokens=["tok1", "tok2"],
        public=False,
        custom_fields=[{"id": 1, "value": "v"}],
        extra_updates={"status": "open", "priority": "high"},
    )
    body = json.loads(mocked.calls[0].request.body)
    assert body == {
        "ticket": {
            "comment": {"body": "see attached", "public": False, "uploads": ["tok1", "tok2"]},
            "custom_fields": [{"id": 1, "value": "v"}],
            "status": "open",
            "priority": "high",
        }
    }


def test_bulk_update_serialises_ids_as_csv(client, base_url, mocked):
    mocked.add(mocked.PUT, f"{base_url}/tickets/update_many.json", json={"job_status": {}}, status=200)
    tickets.bulk_update(client, ids=[1, 2, 3], changes={"status": "solved"})
    body = json.loads(mocked.calls[0].request.body)
    assert body["ids"] == "1,2,3"
    assert body["ticket"] == {"status": "solved"}


def test_incremental_tickets_cursor_uses_start_time(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/incremental/tickets/cursor.json",
        json={"tickets": []},
        status=200,
    )
    tickets.incremental_tickets_cursor(client, start_time=1700000000)
    assert "start_time=1700000000" in mocked.calls[0].request.url


def test_incremental_tickets_cursor_uses_cursor(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/incremental/tickets/cursor.json",
        json={"tickets": []},
        status=200,
    )
    tickets.incremental_tickets_cursor(client, cursor="xyz")
    assert "cursor=xyz" in mocked.calls[0].request.url


def test_upload_file_is_multipart(client, base_url, mocked):
    mocked.add(
        mocked.POST,
        f"{base_url}/uploads.json",
        json={"upload": {"token": "tok"}},
        status=201,
    )
    uploads.upload_file(client, filename="r.pdf", file_bytes=b"data", content_type="application/pdf")
    ct = mocked.calls[0].request.headers.get("Content-Type", "")
    assert "multipart/form-data" in ct
    assert "filename=r.pdf" in mocked.calls[0].request.url
