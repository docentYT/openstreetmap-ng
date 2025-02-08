from base64 import urlsafe_b64encode
from typing import Any

from shapely import get_coordinates
from starlette.responses import HTMLResponse

from app.config import (
    API_URL,
    FORCE_CRASH_REPORTING,
    SENTRY_DSN,
    SENTRY_TRACES_SAMPLE_RATE,
    VERSION,
)
from app.lib.auth_context import auth_user
from app.lib.locale import map_i18next_files
from app.lib.render_jinja import render_jinja
from app.lib.translation import translation_locales
from app.limits import MAP_QUERY_AREA_MAX_SIZE, NOTE_QUERY_AREA_MAX_SIZE
from app.middlewares.parallel_tasks_middleware import ParallelTasksMiddleware
from app.middlewares.request_context_middleware import get_request
from app.models.db.user import Editor
from app.models.proto.shared_pb2 import WebConfig

_DEFAULT_EDITOR = Editor.get_default().value
_CONFIG_BASE = WebConfig(
    sentry_config=(
        WebConfig.SentryConfig(
            dsn=SENTRY_DSN,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        )
        if SENTRY_DSN
        else None
    ),
    version=VERSION,
    force_crash_reporting=FORCE_CRASH_REPORTING,
    api_url=API_URL,
    map_query_area_max_size=MAP_QUERY_AREA_MAX_SIZE,
    note_query_area_max_size=NOTE_QUERY_AREA_MAX_SIZE,
)
_CONFIG_DEFAULT = urlsafe_b64encode(_CONFIG_BASE.SerializeToString()).decode()


async def render_response(
    template_name: str,
    template_data: dict[str, Any] | None = None,
    *,
    status: int = 200,
) -> HTMLResponse:
    """Render the given Jinja2 template with translation, returning an HTMLResponse."""
    data = {
        'request': get_request(),
        'I18NEXT_FILES': map_i18next_files(translation_locales()),
        'DEFAULT_EDITOR': _DEFAULT_EDITOR,
        'WEB_CONFIG': _CONFIG_DEFAULT,
    }

    user = auth_user()
    if user is not None:
        user_config = WebConfig.UserConfig(
            id=user.id,
            activity_tracking=user.activity_tracking,
            crash_reporting=user.crash_reporting,
        )
        user_home_point = user.home_point
        if user_home_point is not None:
            x, y = get_coordinates(user_home_point)[0].tolist()
            user_config.home_point = WebConfig.UserConfig.HomePoint(lon=x, lat=y)

        web_config = WebConfig(user_config=user_config)
        web_config.MergeFrom(_CONFIG_BASE)
        data['WEB_CONFIG'] = urlsafe_b64encode(web_config.SerializeToString()).decode()

        messages_count_unread = await ParallelTasksMiddleware.messages_count_unread()
        if messages_count_unread is not None:
            data['MESSAGES_COUNT_UNREAD'] = messages_count_unread

    if template_data is not None:
        data.update(template_data)
    return HTMLResponse(render_jinja(template_name, data), status_code=status)
