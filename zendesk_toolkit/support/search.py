from typing import Optional

from ..client import JsonDict, ZendeskClient


def search(c: ZendeskClient, q: str) -> Optional[JsonDict]:
    return c.get("search.json", params={"query": q})
