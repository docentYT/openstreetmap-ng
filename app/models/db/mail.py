from datetime import datetime
from typing import Literal, TypedDict

from app.models.types import MailId, UserId

MailSource = Literal['message', 'diary_comment'] | None  # None: for system/no source


class MailInit(TypedDict):
    id: MailId
    source: MailSource
    from_user_id: UserId | None
    to_user_id: UserId
    subject: str
    body: str
    ref: str | None
    priority: int


class Mail(MailInit):
    processing_counter: int
    created_at: datetime
    scheduled_at: datetime
