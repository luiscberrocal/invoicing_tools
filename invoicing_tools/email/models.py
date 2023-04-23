from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel


class SenderConfig(BaseModel):
    email: str
    password: str


class EmailMessage(BaseModel):
    recipients: List[str]
    subject: str
    content: str
    sender_config: SenderConfig
    attachments: Optional[List[Path] | None]

