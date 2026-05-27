from typing import Optional

from ..client import JsonDict, ParamsType, ZendeskClient


def list_article_comments(
    client: ZendeskClient, article_id: int, params: Optional[ParamsType] = None
) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/{article_id}/comments.json", params=params)


def get_article_comment(client: ZendeskClient, article_id: int, comment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/{article_id}/comments/{comment_id}.json")


def create_article_comment(client: ZendeskClient, article_id: int, comment: JsonDict) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/comments.json", json={"comment": comment})


def update_article_comment(
    client: ZendeskClient, article_id: int, comment_id: int, comment: JsonDict
) -> Optional[JsonDict]:
    return client.put(
        f"help_center/articles/{article_id}/comments/{comment_id}.json", json={"comment": comment}
    )


def delete_article_comment(client: ZendeskClient, article_id: int, comment_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/articles/{article_id}/comments/{comment_id}.json")


def upvote_article_comment(client: ZendeskClient, article_id: int, comment_id: int) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/comments/{comment_id}/up.json")


def downvote_article_comment(client: ZendeskClient, article_id: int, comment_id: int) -> Optional[JsonDict]:
    return client.post(f"help_center/articles/{article_id}/comments/{comment_id}/down.json")


def list_article_comment_votes(client: ZendeskClient, article_id: int, comment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/{article_id}/comments/{comment_id}/votes.json")


def list_comments_by_user(client: ZendeskClient, user_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/users/{user_id}/comments.json")
