from typing import Any, Optional

from ..client import JsonDict, ZendeskClient


def create_child_ticket(
    client: ZendeskClient,
    parent_ticket: int,
    subject: str,
    body: str,
    assigned_group: int,
    html: bool = False,
    custom_fields: Optional[list[JsonDict]] = None,
) -> Optional[JsonDict]:
    endpoint = f"tickets/{parent_ticket}/side_conversations/"
    message: dict[str, Any] = {
        "subject": subject,
        ("html_body" if html else "body"): body,
        "to": [{"support_group_id": assigned_group}],
    }
    if custom_fields:
        message["custom_fields"] = custom_fields
    return client.post(endpoint, json={"message": message})
