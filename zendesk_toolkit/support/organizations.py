from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def list_organizations(c: ZendeskClient, params: Optional[ParamsType] = None) -> Optional[JsonDict]:
    return c.get("organizations.json", params=params)


def get_organization(c: ZendeskClient, oid: int) -> Optional[JsonDict]:
    return c.get(f"organizations/{oid}.json")


def create_organization(c: ZendeskClient, org: JsonDict) -> Optional[JsonDict]:
    return c.post("organizations.json", json={"organization": org})


def update_organization(c: ZendeskClient, oid: int, org: JsonDict) -> Optional[JsonDict]:
    return c.put(f"organizations/{oid}.json", json={"organization": org})


def delete_organization(c: ZendeskClient, oid: int) -> Optional[JsonDict]:
    return c.delete(f"organizations/{oid}.json")


def search_organizations(c: ZendeskClient, name: str) -> Optional[JsonDict]:
    return c.get("organizations/search.json", params={"name": name})


def list_org_memberships(c: ZendeskClient, oid: int) -> Optional[JsonDict]:
    return c.get(f"organizations/{oid}/organization_memberships.json")
