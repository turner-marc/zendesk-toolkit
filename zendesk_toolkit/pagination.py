from collections.abc import Iterator
from typing import Any, Optional

from .client import JsonDict, ZendeskClient


def paginate_offset(
    client: ZendeskClient, endpoint: str, params: Optional[dict[str, Any]] = None
) -> Iterator[JsonDict]:
    p: dict[str, Any] = dict(params or {})
    p.setdefault("page", 1)
    p.setdefault("per_page", 100)
    while True:
        data = client.get(endpoint, params=p)
        if data is None:
            break
        yield data
        if not data.get("next_page"):
            break
        p["page"] += 1


def paginate_cursor(
    client: ZendeskClient, endpoint: str, params: Optional[dict[str, Any]] = None
) -> Iterator[JsonDict]:
    p: Optional[dict[str, Any]] = dict(params or {})
    if p is not None:
        p.setdefault("page[size]", 100)
    url = endpoint
    while True:
        data = client.get(url, params=p if url == endpoint else None)
        if data is None:
            break
        yield data
        links = data.get("links") or {}
        nxt = links.get("next") or links.get("next_page")
        if not nxt:
            break
        url = nxt.replace(client.base_url + "/", "")
        p = None
