from typing import Optional

from ..client import JsonDict, ZendeskClient


def list_locales(client: ZendeskClient) -> Optional[JsonDict]:
    return client.get("help_center/locales.json")
