from collections.abc import Iterable
from typing import Optional

from ..client import JsonDict, ZendeskClient


def list_article_attachments(
    client: ZendeskClient, article_id: int, kind: Optional[str] = None
) -> Optional[JsonDict]:
    """List attachments on an article. `kind` may be None, "block", or "inline"."""
    suffix = f"/{kind}" if kind in ("block", "inline") else ""
    return client.get(f"help_center/articles/{article_id}/attachments{suffix}.json")


def get_article_attachment(client: ZendeskClient, attachment_id: int) -> Optional[JsonDict]:
    return client.get(f"help_center/articles/attachments/{attachment_id}.json")


def delete_article_attachment(client: ZendeskClient, attachment_id: int) -> Optional[JsonDict]:
    return client.delete(f"help_center/articles/attachments/{attachment_id}.json")


def create_article_attachment(
    client: ZendeskClient, article_id: int, guide_media_id: int, inline: bool = False
) -> Optional[JsonDict]:
    """Create an article attachment from an existing Guide media object id (multipart form)."""
    files = {
        "guide_media_id": (None, str(guide_media_id)),
        "inline": (None, "true" if inline else "false"),
    }
    return client.post(f"help_center/articles/{article_id}/attachments.json", files=files)


def bulk_attachments(
    client: ZendeskClient, article_id: int, attachment_ids: Iterable[int]
) -> Optional[JsonDict]:
    return client.post(
        f"help_center/articles/{article_id}/bulk_attachments.json",
        json={"attachment_ids": list(attachment_ids)},
    )
