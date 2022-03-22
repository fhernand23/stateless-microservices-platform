"""
Platform Setup: test-errors
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.http import Dto, HttpRespInfo

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('id', str, "Code")
    ],
    responses={
        200: (Dto, "OK"),
        400: (str, "Bad request"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, err_code: str) -> Union[Dto, HttpRespInfo]:
    if err_code == '200':
        return Dto(o={'id': 999, 'info': 'some info'})
    if err_code == '403':
        return HttpRespInfo(403, 'this request is forbidden')
    if err_code == '404':
        return HttpRespInfo(404, 'this request has not found status')

    return HttpRespInfo(400, 'this is a bad request')


async def __postprocess__(payload: Union[Dto, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[Dto, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
