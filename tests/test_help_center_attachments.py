from zendesk_toolkit.help_center import attachments


def test_create_article_attachment_is_multipart(client, base_url, mocked):
    mocked.add(
        mocked.POST,
        f"{base_url}/help_center/articles/55/attachments.json",
        json={"article_attachment": {"id": 1}},
        status=201,
    )
    attachments.create_article_attachment(client, article_id=55, guide_media_id=999, inline=True)
    ct = mocked.calls[0].request.headers.get("Content-Type", "")
    assert "multipart/form-data" in ct
    body = mocked.calls[0].request.body
    assert b"999" in body
    assert b"true" in body


def test_list_article_attachments_kind_filter_inline(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/articles/10/attachments/inline.json",
        json={"article_attachments": []},
        status=200,
    )
    attachments.list_article_attachments(client, article_id=10, kind="inline")
    assert mocked.calls[0].request.url.startswith(
        f"{base_url}/help_center/articles/10/attachments/inline.json"
    )


def test_list_article_attachments_ignores_unknown_kind(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/articles/10/attachments.json",
        json={"article_attachments": []},
        status=200,
    )
    attachments.list_article_attachments(client, article_id=10, kind="nonsense")
    assert mocked.calls[0].request.url.startswith(f"{base_url}/help_center/articles/10/attachments.json")
