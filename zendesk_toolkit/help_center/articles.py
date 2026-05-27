from typing import Any, Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def _scope(locale: Optional[str]) -> str:
    return f"help_center/{locale}" if locale else "help_center"


def list_articles(
    client: ZendeskClient, locale: Optional[str] = None, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/articles.json", params=params)


def get_article(client: ZendeskClient, article_id: int, locale: Optional[str] = None) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/articles/{article_id}.json")


def create_article(
    client: ZendeskClient,
    section_id: int,
    article: JsonDict,
    locale: Optional[str] = None,
    notify_subscribers: Optional[bool] = None,
) -> Optional[JsonDict]:
    payload: dict[str, Any] = {"article": article}
    if notify_subscribers is not None:
        payload["notify_subscribers"] = notify_subscribers
    return client.post(f"{_scope(locale)}/sections/{section_id}/articles.json", json=payload)


def update_article(
    client: ZendeskClient, article_id: int, article: JsonDict, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.put(f"{_scope(locale)}/articles/{article_id}.json", json={"article": article})


def archive_article(
    client: ZendeskClient, article_id: int, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.delete(f"{_scope(locale)}/articles/{article_id}.json")


def update_article_source_locale(
    client: ZendeskClient, article_id: int, source_locale: str
) -> Optional[JsonDict]:
    return client.put(
        f"help_center/articles/{article_id}/source_locale.json",
        json={"article_locale": source_locale},
    )


def list_articles_by_category(
    client: ZendeskClient,
    category_id: int,
    locale: Optional[str] = None,
    params: Optional[ParamsType] = None,
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/categories/{category_id}/articles.json", params=params)


def list_articles_by_section(
    client: ZendeskClient,
    section_id: int,
    locale: Optional[str] = None,
    params: Optional[ParamsType] = None,
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/sections/{section_id}/articles.json", params=params)


def list_articles_by_user(
    client: ZendeskClient, user_id: int, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    return client.get(f"help_center/users/{user_id}/articles.json", params=params)


def incremental_articles(
    client: ZendeskClient, start_time: int, params: Optional[dict[str, Any]] = None
) -> Optional[JsonDict]:
    merged: dict[str, Any] = {"start_time": start_time}
    if params:
        merged.update(params)
    return client.get("help_center/incremental/articles.json", params=merged)
