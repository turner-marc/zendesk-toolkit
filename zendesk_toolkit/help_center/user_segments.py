from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def list_user_segments(client: ZendeskClient, params: Optional[ParamsType] = None) -> Optional[JsonDict]:
    return client.get("help_center/user_segments.json", params=params)


def list_applicable_segments(client: ZendeskClient) -> Optional[JsonDict]:
    return client.get("help_center/user_segments/applicable.json")


def get_user_segment(client: ZendeskClient, segment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/user_segments/{segment_id}.json")


def create_user_segment(client: ZendeskClient, segment: JsonDict) -> Optional[JsonDict]:
    return client.post("help_center/user_segments.json", json={"user_segment": segment})


def update_user_segment(client: ZendeskClient, segment_id: int, segment: JsonDict) -> Optional[JsonDict]:
    return client.put(f"help_center/user_segments/{segment_id}.json", json={"user_segment": segment})


def delete_user_segment(client: ZendeskClient, segment_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/user_segments/{segment_id}.json")


def list_segment_sections(client: ZendeskClient, segment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/user_segments/{segment_id}/sections.json")


def list_segment_topics(client: ZendeskClient, segment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/user_segments/{segment_id}/topics.json")


def list_segments_by_user(client: ZendeskClient, user_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/users/{user_id}/user_segments.json")
