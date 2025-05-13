from pydantic import BaseModel, Field
from typing import Optional, Literal


class PushoverRequest(BaseModel):
    token: Optional[str] = Field(None, description="Optional app token override")
    user: Optional[str] = Field(None, description="Optional user key override")
    message: str = Field(..., description="Message body")

    title: Optional[str] = None
    device: Optional[str] = None

    html: Optional[Literal[0, 1]] = Field(
        None, description="Set 1 to enable HTML formatting"
    )
    priority: Optional[Literal[-2, -1, 0, 1, 2]] = Field(
        None, description="Message priority"
    )
    sound: Optional[str] = None
    timestamp: Optional[int] = None
    url: Optional[str] = None
    url_title: Optional[str] = None
    ttl: Optional[int] = None
    attachment_base64: Optional[str] = None
    attachment_type: Optional[str] = None
