from typing import Annotated

from fastapi import APIRouter, Form
from starlette.responses import HTMLResponse

from app.lib.auth_context import web_user
from app.lib.render_jinja import render_jinja
from app.lib.rich_text import TextFormat, rich_text
from app.models.db.user import User

router = APIRouter(prefix='/api/web/rich-text')


@router.post('')
async def preview(
    text: Annotated[str, Form()],
    _: Annotated[User, web_user()],
):
    cache_entry = await rich_text(text, None, TextFormat.markdown)
    html = cache_entry.value
    if not html:
        html = render_jinja('rich_text/_empty_preview.jinja2')
    return HTMLResponse(html)
