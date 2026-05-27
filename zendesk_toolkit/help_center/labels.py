from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def list_all_labels(client: ZendeskClient, params: Optional[ParamsType] = None) -> Optional[JsonDict]:
    return client.get("help_center/articles/labels.json", params=params)


def get_label(client: ZendeskClient, label_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/labels/{label_id}.json")


def delete_label(client: ZendeskClient, label_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/articles/labels/{label_id}.json")


def list_article_labels(client: ZendeskClient, article_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/{article_id}/labels.json")


def create_article_label(client: ZendeskClient, article_id: int, name: str) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/labels.json", json={"label": {"name": name}})


def delete_article_label(client: ZendeskClient, article_id: int, label_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/articles/{article_id}/labels/{label_id}.json")
