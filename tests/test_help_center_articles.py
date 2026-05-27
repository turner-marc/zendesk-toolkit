import json

from zendesk_toolkit.help_center import articles


def test_list_articles_without_locale_uses_unscoped_path(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/help_center/articles.json", json={"articles": []}, status=200)
    articles.list_articles(client)
    assert mocked.calls[0].request.url.startswith(f"{base_url}/help_center/articles.json")


def test_list_articles_with_locale_injects_locale_in_path(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/en-us/articles.json",
        json={"articles": []},
        status=200,
    )
    articles.list_articles(client, locale="en-us")
    assert mocked.calls[0].request.url.startswith(f"{base_url}/help_center/en-us/articles.json")


def test_create_article_posts_to_section_endpoint(client, base_url, mocked):
    mocked.add(
        mocked.POST,
        f"{base_url}/help_center/en-us/sections/55/articles.json",
        json={"article": {"id": 1}},
        status=201,
    )
    articles.create_article(
        client,
        section_id=55,
        article={"title": "T", "locale": "en-us"},
        locale="en-us",
        notify_subscribers=True,
    )
    body = json.loads(mocked.calls[0].request.body)
    assert body == {
        "article": {"title": "T", "locale": "en-us"},
        "notify_subscribers": True,
    }


def test_archive_article_uses_delete(client, base_url, mocked):
    mocked.add(mocked.DELETE, f"{base_url}/help_center/articles/123.json", body="", status=204)
    result = articles.archive_article(client, article_id=123)
    assert result is None


def test_incremental_articles_passes_start_time(client, base_url, mocked):
    mocked.add(
        mocked.GET,
        f"{base_url}/help_center/incremental/articles.json",
        json={"articles": []},
        status=200,
    )
    articles.incremental_articles(client, start_time=1700000000)
    assert "start_time=1700000000" in mocked.calls[0].request.url
