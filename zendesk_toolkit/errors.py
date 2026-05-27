from typing import Any, Optional


class ZendeskError(Exception):
    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        request_id: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.request_id = request_id
        self.payload: dict[str, Any] = payload or {}

    def __str__(self) -> str:
        base = super().__str__()
        if self.status or self.request_id:
            base += f" (status={self.status}, request_id={self.request_id})"
        return base
