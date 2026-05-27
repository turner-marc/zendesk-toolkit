from typing import Optional

from ..client import JsonDict, ZendeskClient


def list_macros(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("macros.json")


def get_macro(c: ZendeskClient, mid: int) -> Optional[JsonDict]:
    return c.get(f"macros/{mid}.json")


def apply_macro(c: ZendeskClient, mid: int, ticket_id: int) -> Optional[JsonDict]:
    return c.get(f"tickets/{ticket_id}/macros/{mid}/apply.json")


def list_macro_definitions(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("macros/definitions.json")
