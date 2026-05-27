from zendesk_toolkit.pagination import paginate_cursor, paginate_offset


def test_offset_pagination_iterates_until_no_next_page(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/tickets.json",
        json={"tickets": [1, 2], "next_page": "anything"},
        status=200,
    )
    mocked.add(mocked.GET, f"{base_url}/tickets.json", json={"tickets": [3], "next_page": None}, status=200)

    pages = list(paginate_offset(client, "tickets.json"))
    assert [p["tickets"] for p in pages] == [[1, 2], [3]]
    # page counter must increment
    assert "page=1" in mocked.calls[0].request.url
    assert "page=2" in mocked.calls[1].request.url


def test_offset_pagination_stops_immediately_when_first_page_has_no_next(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/tickets.json", json={"tickets": [1]}, status=200)
    pages = list(paginate_offset(client, "tickets.json"))
    assert len(pages) == 1


def test_cursor_pagination_follows_links_next(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/incremental/tickets/cursor.json",
        json={"tickets": [1], "links": {"next": f"{base_url}/incremental/tickets/cursor.json?cursor=abc"}},
        status=200,
    )
    mocked.add(
        mocked.GET,
        f"{base_url}/incremental/tickets/cursor.json",
        match=[lambda req: ("cursor=abc" in req.url, "expected cursor=abc")],
        json={"tickets": [2], "links": {"next": None}},
        status=200,
    )

    pages = list(paginate_cursor(client, "incremental/tickets/cursor.json"))
    assert [p["tickets"] for p in pages] == [[1], [2]]
