from typing import Optional

from ..client import JsonDict, ZendeskClient


def list_ticket_fields(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("ticket_fields.json")


def get_ticket_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.get(f"ticket_fields/{fid}.json")


def create_ticket_field(c: ZendeskClient, field: JsonDict) -> Optional[JsonDict]:
    return c.post("ticket_fields.json", json={"ticket_field": field})


def update_ticket_field(c: ZendeskClient, fid: int, field: JsonDict) -> Optional[JsonDict]:
    return c.put(f"ticket_fields/{fid}.json", json={"ticket_field": field})


def delete_ticket_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.delete(f"ticket_fields/{fid}.json")


def list_user_fields(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("user_fields.json")


def get_user_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.get(f"user_fields/{fid}.json")


def create_user_field(c: ZendeskClient, field: JsonDict) -> Optional[JsonDict]:
    return c.post("user_fields.json", json={"user_field": field})


def update_user_field(c: ZendeskClient, fid: int, field: JsonDict) -> Optional[JsonDict]:
    return c.put(f"user_fields/{fid}.json", json={"user_field": field})


def delete_user_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.delete(f"user_fields/{fid}.json")


def list_org_fields(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("organization_fields.json")


def get_org_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.get(f"organization_fields/{fid}.json")


def create_org_field(c: ZendeskClient, field: JsonDict) -> Optional[JsonDict]:
    return c.post("organization_fields.json", json={"organization_field": field})


def update_org_field(c: ZendeskClient, fid: int, field: JsonDict) -> Optional[JsonDict]:
    return c.put(f"organization_fields/{fid}.json", json={"organization_field": field})


def delete_org_field(c: ZendeskClient, fid: int) -> Optional[JsonDict]:
    return c.delete(f"organization_fields/{fid}.json")
