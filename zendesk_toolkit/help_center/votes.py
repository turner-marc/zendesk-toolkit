from typing import Optional

from ..client import JsonDict, ZendeskClient


def get_vote(client: ZendeskClient, vote_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/votes/{vote_id}.json")


def delete_vote(client: ZendeskClient, vote_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/votes/{vote_id}.json")


def list_article_votes(client: ZendeskClient, article_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/{article_id}/votes.json")


def upvote_article(client: ZendeskClient, article_id: int) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/up.json")


def downvote_article(client: ZendeskClient, article_id: int) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/down.json")


def list_user_votes(client: ZendeskClient, user_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/users/{user_id}/votes.json")
