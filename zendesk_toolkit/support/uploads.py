from typing import Optional

from ..client import JsonDict, ZendeskClient


def upload_file(
    client: ZendeskClient,
    filename: str,
    file_bytes: bytes,
    content_type: str = "application/octet-stream",
    token: Optional[str] = None,
) -> Optional[JsonDict]:
    endpoint = f"uploads.json?filename={filename}"
    if token:
        endpoint += f"&token={token}"
    files = {"file": (filename, file_bytes, content_type)}
    return client.post(endpoint, files=files)
