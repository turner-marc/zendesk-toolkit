from typing import Any, Optional

from ..client import JsonDict, ZendeskClient


def search_articles(client: ZendeskClient, query: Optional[str] = None, **filters: Any) -> Optional[JsonDict]:
    """Search Help Center articles. Must supply at least one of: query, category, section, label_names.

    Common filters: category (int), section (int), label_names (str), locale (str),
    brand_id (int), multibrand (bool), created_before/after (YYYY-MM-DD),
    updated_before/after, sort_by, sort_order, page, per_page.
    """
    params: dict[str, Any] = {k: v for k, v in filters.items() if v is not None}
    if query is not None:
        params["query"] = query
    return client.get("help_center/articles/search.json", params=params or None)


def unified_search(client: ZendeskClient, query: str, **filters: Any) -> Optional[JsonDict]:
    """Unified search across articles, community posts, and external content."""
    params: dict[str, Any] = {"query": query}
    params.update({k: v for k, v in filters.items() if v is not None})
    return client.get("guide/search.json", params=params)
