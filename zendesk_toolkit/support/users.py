from typing import Optional

from ..client import JsonDict, ZendeskClient


def create_user(c: ZendeskClient, user: JsonDict) -> Optional[JsonDict]:
    return c.post("users.json", json={"user": user})


def get_user(c: ZendeskClient, uid: int) -> Optional[JsonDict]:
    return c.get(f"users/{uid}.json")


def update_user(c: ZendeskClient, uid: int, user: JsonDict) -> Optional[JsonDict]:
    return c.put(f"users/{uid}.json", json={"user": user})


def delete_user(c: ZendeskClient, uid: int) -> Optional[JsonDict]:
    return c.delete(f"users/{uid}.json")


def get_agents(c: ZendeskClient, include_admin: bool = False) -> Optional[JsonDict]:
    roles = ["agent"] + (["admin"] if include_admin else [])
    params = [("role[]", r) for r in roles]
    return c.get("users.json", params=params)


def search_users(c: ZendeskClient, query: str) -> Optional[JsonDict]:
    return c.get("search.json", params={"query": query})


def search_users_by_email(c: ZendeskClient, email: str) -> Optional[JsonDict]:
    return search_users(c, f'type:user email:"{email}"')


def list_user_identities(c: ZendeskClient, uid: int) -> Optional[JsonDict]:
    return c.get(f"users/{uid}/identities.json")
