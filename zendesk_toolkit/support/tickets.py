from typing import Any, Optional

from ..client import JsonDict, ZendeskClient


def create_ticket(client: ZendeskClient, ticket: JsonDict) -> Optional[JsonDict]:
    return client.post("tickets.json", json={"ticket": ticket})


def get_ticket(client: ZendeskClient, ticket_id: int) -> Optional[JsonDict]:
    return client.get(f"tickets/{ticket_id}.json")


def update_ticket(client: ZendeskClient, ticket_id: int, ticket: JsonDict) -> Optional[JsonDict]:
    return client.put(f"tickets/{ticket_id}.json", json={"ticket": ticket})


def delete_ticket(client: ZendeskClient, ticket_id: int) -> Optional[JsonDict]:
    return client.delete(f"tickets/{ticket_id}.json")


def add_comment_with_uploads(
    client: ZendeskClient,
    ticket_id: int,
    body: str,
    upload_tokens: list[str],
    public: bool = True,
    custom_fields: Optional[list[JsonDict]] = None,
    extra_updates: Optional[JsonDict] = None,
) -> Optional[JsonDict]:
    """Add a comment (optionally with uploads) and update custom fields / other ticket properties in one call.

    Args:
        body: Comment text.
        upload_tokens: List of tokens from /uploads.
        public: Whether the comment is public.
        custom_fields: List of {"id": <field_id>, "value": <field_value>}.
        extra_updates: Additional ticket-level updates, e.g. {"status": "open", "priority": "urgent"}.
    """
    ticket_payload: dict[str, Any] = {"comment": {"body": body, "public": public, "uploads": upload_tokens}}
    if custom_fields:
        ticket_payload["custom_fields"] = custom_fields
    if extra_updates:
        ticket_payload.update(extra_updates)
    return client.put(f"tickets/{ticket_id}.json", json={"ticket": ticket_payload})


def bulk_update(client: ZendeskClient, ids: list[int], changes: JsonDict) -> Optional[JsonDict]:
    return client.put("tickets/update_many.json", json={"ids": ",".join(map(str, ids)), "ticket": changes})


def merge_tickets(client: ZendeskClient, target_id: int, source_ids: list[int]) -> Optional[JsonDict]:
    return client.post(f"tickets/{target_id}/merge.json", json={"ids": source_ids})


def list_ticket_audits(client: ZendeskClient, ticket_id: int) -> Optional[JsonDict]:
    return client.get(f"tickets/{ticket_id}/audits.json")


def list_ticket_metrics(client: ZendeskClient, ticket_id: int) -> Optional[JsonDict]:
    return client.get(f"tickets/{ticket_id}/metrics.json")


def incremental_tickets_cursor(
    client: ZendeskClient,
    start_time: Optional[int] = None,
    cursor: Optional[str] = None,
    include: Optional[str] = None,
) -> Optional[JsonDict]:
    if cursor:
        endpoint = f"incremental/tickets/cursor.json?cursor={cursor}"
    else:
        endpoint = "incremental/tickets/cursor.json"
        if start_time is not None:
            endpoint += f"?start_time={start_time}"
    params: dict[str, Any] = {}
    if include:
        params["include"] = include
    return client.get(endpoint, params=params or None)
