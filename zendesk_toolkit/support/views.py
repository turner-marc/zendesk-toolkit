from typing import Any, Optional

from ..client import JsonDict, ZendeskClient


def list_views(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("views.json")


def get_view(c: ZendeskClient, vid: int) -> Optional[JsonDict]:
    return c.get(f"views/{vid}.json")


def execute_view(c: ZendeskClient, vid: int) -> Optional[JsonDict]:
    return c.get(f"views/{vid}/execute.json")


def view_count(c: ZendeskClient, vid: int) -> Optional[JsonDict]:
    return c.get(f"views/{vid}/count.json")


def preview_view(c: ZendeskClient, criteria: list[Any]) -> Optional[JsonDict]:
    return c.post("views/preview.json", json={"view": {"conditions": criteria}})
