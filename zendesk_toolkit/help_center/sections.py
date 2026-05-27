from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def _scope(locale: Optional[str]) -> str:
    return f"help_center/{locale}" if locale else "help_center"


def list_sections(
    client: ZendeskClient, locale: Optional[str] = None, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/sections.json", params=params)


def get_section(client: ZendeskClient, section_id: int, locale: Optional[str] = None) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/sections/{section_id}.json")


def create_section(
    client: ZendeskClient, category_id: int, section: JsonDict, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.post(f"{_scope(locale)}/categories/{category_id}/sections.json", json={"section": section})


def update_section(
    client: ZendeskClient, section_id: int, section: JsonDict, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.put(f"{_scope(locale)}/sections/{section_id}.json", json={"section": section})


def delete_section(
    client: ZendeskClient, section_id: int, locale: Optional[str] = None
) -> Optional[JsonDict]:
    return client.delete(f"{_scope(locale)}/sections/{section_id}.json")


def list_sections_by_category(
    client: ZendeskClient,
    category_id: int,
    locale: Optional[str] = None,
    params: Optional[ParamsType] = None,
) -> Optional[JsonDict]:
    return client.get(f"{_scope(locale)}/categories/{category_id}/sections.json", params=params)


def update_section_source_locale(
    client: ZendeskClient, section_id: int, source_locale: str
) -> Optional[JsonDict]:
    return client.put(
        f"help_center/sections/{section_id}/source_locale.json",
        json={"section_locale": source_locale},
    )
