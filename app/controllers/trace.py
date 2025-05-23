from asyncio import TaskGroup
from typing import Annotated

from fastapi import APIRouter, Response
from polyline_rs import encode_lonlat
from starlette import status
from starlette.responses import RedirectResponse

from app.config import API_URL
from app.lib.auth_context import web_user
from app.lib.render_response import render_response
from app.models.db.user import User
from app.models.types import TraceId
from app.queries.trace_query import TraceQuery
from app.queries.user_query import UserQuery

router = APIRouter(prefix='/trace')


@router.get('/upload')
async def upload(_: Annotated[User, web_user()]):
    return await render_response('traces/upload')


@router.get('/{trace_id:int}')
async def details(trace_id: TraceId):
    trace = await TraceQuery.get_one_by_id(trace_id)

    async with TaskGroup() as tg:
        items = [trace]
        tg.create_task(UserQuery.resolve_users(items))
        tg.create_task(
            TraceQuery.resolve_coords(items, limit_per_trace=500, resolution=None)
        )

    trace_line = encode_lonlat(trace['coords'].tolist(), 6)  # type: ignore
    return await render_response(
        'traces/details',
        {
            'trace': trace,
            'trace_line': trace_line,
            'base_url_notag': '/traces',
        },
    )


@router.get('/{trace_id:int}/edit')
async def edit(
    trace_id: TraceId,
    user: Annotated[User, web_user()],
):
    trace = await TraceQuery.get_one_by_id(trace_id)
    if trace['user_id'] != user['id']:
        # TODO: this could be nicer?
        return Response(None, status.HTTP_403_FORBIDDEN)

    await TraceQuery.resolve_coords([trace], limit_per_trace=500, resolution=None)

    trace_line = encode_lonlat(trace['coords'].tolist(), 6)  # type: ignore
    return await render_response(
        'traces/edit',
        {
            'trace': trace,
            'trace_line': trace_line,
        },
    )


@router.get('/{trace_id:int}/data{suffix:path}')
async def legacy_data(trace_id: TraceId, suffix: str):
    return RedirectResponse(
        f'{API_URL}/api/0.6/gpx/{trace_id}/data{suffix}', status.HTTP_302_FOUND
    )
