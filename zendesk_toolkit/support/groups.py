from typing import Optional

from ..client import JsonDict, ZendeskClient


def list_groups(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("groups.json")


def get_group(c: ZendeskClient, gid: int) -> Optional[JsonDict]:
    return c.get(f"groups/{gid}.json")


def create_group(c: ZendeskClient, group: JsonDict) -> Optional[JsonDict]:
    return c.post("groups.json", json={"group": group})


def update_group(c: ZendeskClient, gid: int, group: JsonDict) -> Optional[JsonDict]:
    return c.put(f"groups/{gid}.json", json={"group": group})


def delete_group(c: ZendeskClient, gid: int) -> Optional[JsonDict]:
    return c.delete(f"groups/{gid}.json")


def list_group_memberships(c: ZendeskClient, gid: int) -> Optional[JsonDict]:
    return c.get(f"groups/{gid}/memberships.json")


def list_assignable_groups(c: ZendeskClient) -> Optional[JsonDict]:
    return c.get("groups/assignable.json")
