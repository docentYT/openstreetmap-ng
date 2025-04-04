from datetime import datetime
from typing import NotRequired, TypedDict

from shapely import Point

from app.lib.rich_text import resolve_rich_text
from app.models.db.user import UserDisplay
from app.models.types import DiaryId, LocaleCode, UserId


class DiaryInit(TypedDict):
    user_id: UserId
    title: str
    body: str  # TODO: validate size
    language: LocaleCode
    point: Point | None


class Diary(DiaryInit):
    id: DiaryId
    body_rich_hash: bytes | None
    created_at: datetime
    updated_at: datetime

    # runtime
    user: NotRequired[UserDisplay]
    body_rich: NotRequired[str]
    num_comments: NotRequired[int]
    location_name: NotRequired[str]


async def diaries_resolve_rich_text(objs: list[Diary]) -> None:
    await resolve_rich_text(objs, 'diary', 'body', 'markdown')
