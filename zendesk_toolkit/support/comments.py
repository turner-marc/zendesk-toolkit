from typing import Optional

from ..client import JsonDict, ZendeskClient


def get_ticket_comments(
    client: ZendeskClient, ticket_id: int, include_users: bool = False
) -> Optional[JsonDict]:
    params = {"include": "users"} if include_users else None
    return client.get(f"tickets/{ticket_id}/comments.json", params=params)
