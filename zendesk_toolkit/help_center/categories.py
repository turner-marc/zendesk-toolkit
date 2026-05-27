from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def _scope(locale: Optional[str]) -> str:
    return f"help_center/{locale}" if locale else "help_center"


def list_categories(
    client: ZendeskClient, locale: Optional[str] = None, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/categories.json", params=params)


def get_category(client: ZendeskClient, category_id: int, locale: Optional[str] = None) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/categories/{category_id}.json")


def create_category(
    client: ZendeskClient, category: JsonDict, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.post(f"{_scope(locale)}/categories.json", json={"category": category})


def update_category(
    client: ZendeskClient, category_id: int, category: JsonDict, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.put(f"{_scope(locale)}/categories/{category_id}.json", json={"category": category})


def delete_category(
    client: ZendeskClient, category_id: int, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.delete(f"{_scope(locale)}/categories/{category_id}.json")


def update_category_source_locale(
    client: ZendeskClient, category_id: int, source_locale: str
) -> Optional[JsonDict]:
    return client.put(
        f"help_center/categories/{category_id}/source_locale.json",
        json={"category_locale": source_locale},
    )
