from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient

_PARENTS = {"articles", "sections", "categories"}


def _validate(parent: str) -> None:
    if parent not in _PARENTS:
        raise ValueError(f"parent must be one of {sorted(_PARENTS)}")


def list_translations(
    client: ZendeskClient, parent: str, parent_id: int, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    _validate(parent)
    return client.get(f"help_center/{parent}/{parent_id}/translations.json", params=params)


def list_missing_translations(client: ZendeskClient, parent: str, parent_id: int) -> Optional[JsonDict]:
    _validate(parent)
    return client.get(f"help_center/{parent}/{parent_id}/translations/missing.json")


def get_translation(client: ZendeskClient, parent: str, parent_id: int, locale: str) -> Optional[JsonDict]:
    _validate(parent)
    return client.get(f"help_center/{parent}/{parent_id}/translations/{locale}.json")


def create_translation(
    client: ZendeskClient, parent: str, parent_id: int, translation: JsonDict
) -> Optional[JsonDict]:
    _validate(parent)
    return client.post(
        f"help_center/{parent}/{parent_id}/translations.json",
        json={"translation": translation},
    )


def update_translation(
    client: ZendeskClient, parent: str, parent_id: int, locale: str, translation: JsonDict
) -> Optional[JsonDict]:
    _validate(parent)
    return client.put(
        f"help_center/{parent}/{parent_id}/translations/{locale}.json",
        json={"translation": translation},
    )


def delete_translation(client: ZendeskClient, translation_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/translations/{translation_id}.json")
